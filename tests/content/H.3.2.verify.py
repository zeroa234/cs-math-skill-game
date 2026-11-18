"""H.3.2 嵌入式系统、驱动与 RTOS：核对内容包里的每个数值、程序输出和真实系统的读数。

三类核对：
1. Python 计算和模拟：时间线（固定优先级抢占 + 互斥锁，有/无优先级继承）、周期漂移、利用率与响应时间分析、
   队列长度、地址翻译、碎片、看门狗超时、电流、抖动、位掩码……并和包里每道题的 answer 逐个比较。
2. WSL 里 gcc 实际编译运行：nm/size 看变量分段（与卡片里贴的输出逐行比较）、驱动 read 函数的逻辑
   （copy_to_user 换成用户态桩函数）、FreeRTOS 风格代码的语法（API 用桩声明，pdMS_TO_TICKS 照抄 projdefs.h）、
   POSIX 优先级继承属性、无权限创建 SCHED_FIFO 线程、消息队列出队顺序、sigwait、clock_nanosleep 绝对时间周期。
3. 读真实系统（只在 WSL 内核上检查）：chrt -m、sched_rr_timeslice_ms、getconf PAGESIZE、/proc/config.gz。

内核模块本身没有加载运行：WSL 没有内核头文件也没有免密 root。内核 API 的语义以 Linux 源码和文档为准。
运行：python -I tests/content/H.3.2.verify.py
"""
from fractions import Fraction as F
from math import ceil, log
from pathlib import Path
import json
import re
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[2]
PACK_FILE = ROOT / "data/content/H.3.2.yaml"


def load_pack() -> dict:
    js = (
        "const y=require('js-yaml');const fs=require('fs');"
        "process.stdout.write(JSON.stringify(y.load(fs.readFileSync(process.argv[1],'utf8'))));"
    )
    out = subprocess.run(["node", "-e", js, str(PACK_FILE)], cwd=ROOT, capture_output=True,
                         text=True, encoding="utf-8", check=True)
    return json.loads(out.stdout)


PACK = load_pack()
ITEMS = {}
CARDS = []
for lesson in PACK["lessons"]:
    for step in lesson["flow"]:
        for kind in ("guess", "item"):
            if kind in step:
                ITEMS[step[kind]["id"] if kind == "item" else lesson["id"] + "/guess"] = step[kind]
        if "card" in step:
            CARDS.append(step["card"])
for it in PACK["boss"]["items"]:
    ITEMS[it["id"]] = it


def answer(item_id: str):
    return ITEMS[item_id]["answer"]


CHECKED: set[str] = set()


def check(item_id: str, value) -> None:
    CHECKED.add(item_id)
    want = answer(item_id)
    tol = ITEMS[item_id].get("tolerance", abs(want) * 1e-6)
    assert abs(float(value) - float(want)) <= tol, (item_id, value, want)


def card(title: str) -> dict:
    hits = [c for c in CARDS if c.get("title") == title]
    assert len(hits) == 1, title
    return hits[0]


def code_blocks(text: str, lang: str = "") -> list[str]:
    return [m.group(1) for m in re.finditer(r"```" + lang + r"\n(.*?)```", text, re.S)]


# ------------------------------------------------------------------ 1. 计算和模拟
def test_startup_math() -> None:
    # 例题：_sdata..._edata 24 字节，_sbss..._ebss 544 字节，共 568
    assert 0x20000018 - 0x20000000 == 24
    assert 0x20000238 - 0x20000018 == 0x220 == 2 * 256 + 2 * 16 == 544
    assert 24 + 544 == 568
    check("bss-bytes", 0x20000440 - 0x20000040)
    check("startup-total", (0x20000040 - 0x20000000) + (0x20000440 - 0x20000040))
    check("boss-bss", 0x20000280 - 0x20000080)
    # bss-align：counter 0..4，zero_init 4..8，rx_buf 从 0x20 开始，512 字节
    assert 0x20 - 8 == 24 and 0x20 + 512 == 544


def test_device_tree_math() -> None:
    assert 0x4000 == 4 * 4096 == 16384
    check("reg-size", 0x400)


def test_loop_and_rtos_math() -> None:
    assert F("0.2") + 30 + 5 == F("35.2")
    check("loop-worst", F("0.5") + 12 + 3)
    check("stack-bytes", 512 * 4)
    assert 256 * 4 == 1024
    # pdMS_TO_TICKS：( ms * configTICK_RATE_HZ ) / 1000，整数除法（FreeRTOS projdefs.h）
    check("ticks-250", (10 * 250) // 1000)
    assert (10 * 1000) // 1000 == 10
    assert 1000 // 250 == 4  # 节拍周期 4 ms

    def samples(period: int, window: int = 1000) -> int:
        return len(range(0, window, period))

    assert samples(2 + 10) == 84 and samples(10) == 100 and 100 - 84 == 16
    assert samples(12, 60000) == 5000 and samples(10, 60000) == 6000
    check("drift-count", samples(3 + 20))
    assert 23 * 43 == 989 and 23 * 44 == 1012


def run_fp(tasks: dict, inherit: bool) -> dict:
    """单核固定优先级抢占，1 ms 一步。每个任务：release、prio、pre（加锁前）、cs（持锁运行）、post（解锁后）。
    cs > 0 的任务在 pre 跑完时去拿唯一的那把锁。返回每个任务的完成时刻。"""
    st = {n: dict(t, phase="pre", left=t.get("pre", 0)) for n, t in tasks.items()}
    owner = None
    done = {}
    t = 0

    def advance(n: str) -> None:
        nonlocal owner
        s = st[n]
        while s["left"] == 0 and s["phase"] != "done":
            if s["phase"] == "pre":
                if s.get("cs", 0) == 0:
                    s["phase"], s["left"] = "post", s.get("post", 0)
                elif owner is None:
                    owner = n
                    s["phase"], s["left"] = "cs", s["cs"]
                else:
                    return  # 等锁
            elif s["phase"] == "cs":
                owner = None
                s["phase"], s["left"] = "post", s.get("post", 0)
            elif s["phase"] == "post":
                s["phase"] = "done"
                done[n] = t

    while len(done) < len(tasks):
        for n in st:
            if st[n]["release"] <= t:
                advance(n)
        ready = [n for n, s in st.items() if s["release"] <= t and s["phase"] != "done"
                 and not (s["phase"] == "pre" and s["left"] == 0)]
        blocked = [n for n, s in st.items() if s["release"] <= t and s["phase"] == "pre"
                   and s["left"] == 0 and s.get("cs", 0) > 0]

        def eff(n: str) -> int:
            p = st[n]["prio"]
            if inherit and n == owner and blocked:
                p = max([p] + [st[b]["prio"] for b in blocked])
            return p

        if ready:
            run = max(ready, key=eff)
            st[run]["left"] -= 1
        t += 1
        for n in st:
            if st[n]["release"] <= t:
                advance(n)
        assert t < 1000
    return done


def test_timelines() -> None:
    d = run_fp({"H": dict(prio=3, release=2, post=2), "M": dict(prio=2, release=0, post=3),
                "L": dict(prio=1, release=0, post=4)}, inherit=False)
    assert d == {"H": 4, "M": 5, "L": 9}, d
    d = run_fp({"H": dict(prio=3, release=1, post=1), "M": dict(prio=2, release=0, post=3),
                "L": dict(prio=1, release=0, post=4)}, inherit=False)
    check("timeline-l", d["L"])
    check("timeline-m", d["M"])

    def inversion(cs_l: int, h_run: int, m_run: int, inherit: bool) -> int:
        done = run_fp({"L": dict(prio=1, release=0, cs=cs_l), "H": dict(prio=3, release=1, cs=h_run),
                       "M": dict(prio=2, release=2, post=m_run)}, inherit)
        return done["H"] - 1

    assert inversion(3, 1, 5, False) == 8  # 例题：9 ms 完成
    check("inversion-long", inversion(3, 1, 10, False))
    check("inheritance-time", inversion(3, 1, 5, True))
    check("boss-inversion", inversion(4, 2, 6, False))
    assert inversion(4, 2, 6, True) == 5


def rta(tasks: list[tuple[int, int]]) -> list[tuple[int, list[int]]]:
    """tasks 按优先级从高到低：(C, T)。返回每个任务的 (R, 迭代过程)。"""
    out = []
    for i, (c, t) in enumerate(tasks):
        r, trace = c, [c]
        while True:
            nxt = c + sum(ceil(r / tj) * cj for cj, tj in tasks[:i])
            if nxt == r:
                break
            r = nxt
            trace.append(r)
            assert r <= 10 * t
        out.append((r, trace))
    return out


def test_schedulability() -> None:
    check("util-sum", F(1, 4) + F(2, 10) + F(3, 20))
    bound = lambda n: n * (2 ** (1 / n) - 1)
    assert round(bound(1), 3) == 1.0 and round(bound(2), 3) == 0.828 and round(bound(3), 3) == 0.780
    assert abs(bound(10 ** 6) - log(2)) < 1e-6 and round(log(2), 3) == 0.693
    assert 0.75 <= bound(3) < 0.85

    r = rta([(1, 4), (2, 6), (3, 12)])
    assert [x[0] for x in r] == [1, 3, 10] and r[1][1] == [2, 3] and r[2][1] == [3, 6, 7, 9, 10], r
    assert round(float(F(1, 4) + F(2, 6) + F(3, 12)), 3) == 0.833
    r = rta([(1, 4), (2, 6), (4, 12)])
    assert r[2][1] == [4, 7, 10, 11]
    check("rta-r3", r[2][0])
    r = rta([(1, 4), (2, 6), (5, 12)])
    assert r[2] == (12, [5, 9, 12]) and F(1, 4) + F(2, 6) + F(5, 12) == 1
    r = rta([(1, 5), (2, 8), (5, 20)])
    assert r[2][1] == [5, 8, 9, 11, 12]
    check("boss-rta", r[2][0])
    check("deadline-bw", F(2, 10))


def test_queue_math() -> None:
    assert 200 // 10 == 20 and 32 * 2 == 64
    check("queue-len", 120 // 5)
    check("queue-bytes", 24 * 4)


def test_latency_math() -> None:
    s = [12, 9, 15, 11, 140, 10]
    assert (min(s), max(s), sum(s)) == (9, 140, 197)
    assert round(197 / 6, 1) == 32.8
    assert F(sum(x for x in s if x != 140), 5) == F("11.4")
    assert max(s) - min(s) == 131
    s2 = [20, 25, 18, 22, 95, 21]
    check("jitter-range", max(s2) - min(s2))
    check("affinity-mask", (1 << 0) | (1 << 1) | (1 << 2))


def test_memory_math() -> None:
    vpn, off = divmod(9029, 4096)
    assert (vpn, off, [5, None, 7][vpn] * 4096 + off) == (2, 837, 29509)
    item = ITEMS["paging-sim"]
    vpn, off = divmod(item["params"]["vaddr"], item["params"]["pageSize"])
    frame = item["params"]["table"][vpn]
    assert item["solution"] == {"vpn": vpn, "offset": off, "paddr": frame * 4096 + off} == \
        {"vpn": 1, "offset": 904, "paddr": 25480}

    def order_for(kb: int, page_kb: int = 4) -> int:
        pages = -(-kb // page_kb)
        o = 0
        while (1 << o) < pages:
            o += 1
        return o

    check("page-order", order_for(20))
    assert (1 << 3) * 4 - 20 == 12
    check("boss-order", order_for(40))

    def largest_free(size: int, allocs: list[tuple[str, int]], frees: set[str], coalesce: bool) -> int:
        blocks, pos = [], 0
        for name, n in allocs:
            blocks.append([name, pos, n])
            pos += n
        blocks.append([None, pos, size - pos])
        for b in blocks:
            if b[0] in frees:
                b[0] = None
        runs, cur = [], 0
        for b in blocks:
            if b[0] is None:
                cur = cur + b[2] if coalesce else b[2]
                runs.append(cur)
            else:
                cur = 0
        return max(runs)

    a = [("A", 300), ("B", 300), ("C", 300)]
    assert largest_free(1000, a, {"A", "B"}, coalesce=False) == 300
    assert 300 + 300 + 100 == 700
    assert largest_free(1000, a, {"A", "B"}, coalesce=True) == 600
    check("frag-largest", largest_free(1200, [("A", 400), ("B", 200), ("C", 400)], {"A", "C"}, coalesce=True))
    check("stack-used", (256 - 40) * 4)


def test_power_and_watchdog() -> None:
    avg = F(20) * F(10, 1000) + F("0.010") * F(990, 1000)
    assert avg == F("0.2099")
    hours = F(1000) / avg
    assert round(float(hours)) == 4764 and round(float(hours) / 24, 1) == 198.5
    assert F("0.0099") / avg < F(5, 100)
    check("avg-current", F(20) * F(5, 1000) + F("0.010") * F(995, 1000))
    assert F(20) * F(5, 1000) + F("0.010") * F(995, 1000) == F("0.10995")
    # 猜一猜：0.2 + 0.0099 ≈ 0.21
    assert round(float(avg), 2) == 0.21

    def iwdg_ms(presc: int, rlr: int, lsi: int = 32000) -> F:
        return F(rlr + 1) * presc * 1000 / lsi

    assert iwdg_ms(64, 999) == 2000
    assert iwdg_ms(4, 0) * 1000 == 125  # 125 us：ST HAL 注释写的最小值 ~125us
    assert round(float(iwdg_ms(256, 4095)) / 1000, 1) == 32.8  # 32.768 s：注释写 ~32.7s
    check("wdt-timeout", iwdg_ms(32, 4095))
    check("boss-wdt", iwdg_ms(128, 2499) / 1000)


def test_sims_and_texts() -> None:
    race = ITEMS["race-sim"]
    assert race["goal"] == {"final": {"x": 1}} and race["solution"] == [0, 1, 0, 0, 1, 1]
    dl = ITEMS["deadlock-sim"]
    assert dl["goal"] == {"deadlock": True} and dl["solution"] == [0, 1]
    # POSIX 消息队列的答案选项（与下面 gcc 实测一致）
    assert next(o["text"] for o in ITEMS["mq-order"]["options"] if o.get("correct")) == "b、a、c"


# ------------------------------------------------------------------ 2. WSL gcc
def wsl(cmd: str, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(["wsl", "bash", "-lc", cmd], capture_output=True, text=True,
                          encoding="utf-8", check=False, timeout=timeout)


def with_workdir(fn):
    work = ROOT / "temp" / f"h32-verify-{uuid.uuid4().hex[:8]}"
    work.mkdir(parents=True, exist_ok=True)
    try:
        return fn(work, f"/mnt/d/agent/projects/cs-math-skill-game/temp/{work.name}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def test_sections_with_gcc() -> None:
    c_src = code_blocks(card("你的变量落在哪一段")["body"], "c")[0]
    shown = code_blocks(card("nm 的实际输出")["body"])[0].strip().splitlines()

    def go(work: Path, w: str):
        (work / "sections.c").write_text(c_src, encoding="utf-8")
        r = wsl(f"cd {w} && gcc -O0 -c sections.c -o sections.o && nm -S sections.o && echo --- && size -A sections.o")
        assert r.returncode == 0, r.stderr
        nm_out, size_out = r.stdout.split("---")
        assert nm_out.strip().splitlines() == shown, (nm_out, shown)
        sizes = {m.group(1): int(m.group(2)) for m in re.finditer(r"^(\.\w+)\s+(\d+)", size_out, re.M)}
        assert (sizes[".data"], sizes[".bss"], sizes[".rodata"]) == (8, 544, 16), sizes
        letters = {line.split()[3]: line.split()[2] for line in shown}
        assert letters == {"cfg": "D", "counter": "B", "main": "T", "rx_buf": "b", "table": "R",
                           "threshold": "D", "zero_init": "B"}

    with_workdir(go)


def test_char_driver_read_with_gcc() -> None:
    fn = next(b for b in code_blocks(card("read 怎么写：copy_to_user")["body"], "c") if "hello_read" in b)
    prog = f"""
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#define __user
struct file;
static int fail_copy;
static unsigned long copy_to_user(void *to, const void *from, unsigned long n)
{{ if (fail_copy) return n; memcpy(to, from, n); return 0; }}
{fn}
int main(void) {{
    char buf[4096]; loff_t off = 0;
    long a = hello_read(NULL, buf, 4096, &off), b = hello_read(NULL, buf, 4096, &off);
    printf("cat %ld %ld %.2s\\n", a, b, buf);
    off = 0;
    long c = hello_read(NULL, buf, 2, &off), d = hello_read(NULL, buf, 2, &off), e = hello_read(NULL, buf, 2, &off);
    printf("two %ld %ld %ld\\n", c, d, e);
    fail_copy = 1; off = 0;
    printf("fault %ld %d\\n", (long)hello_read(NULL, buf, 8, &off), -EFAULT);
    return 0;
}}
"""
    read_twice = ITEMS["read-twice"]["code"]

    def go(work: Path, w: str):
        (work / "drv.c").write_text(prog, encoding="utf-8")
        (work / "drv2.c").write_text(prog.replace(fn, read_twice), encoding="utf-8")
        r = wsl(f"cd {w} && gcc -std=gnu11 -Wall -Werror drv.c -o drv && ./drv && gcc -std=gnu11 -Wall -Werror drv2.c -o drv2 && ./drv2")
        assert r.returncode == 0, (r.stdout, r.stderr)
        lines = r.stdout.splitlines()
        assert lines[0] == "cat 3 0 hi", lines
        assert lines[1] == "two 2 1 0" and lines[2] == "fault -14 -14", lines
        assert lines[3:] == lines[:3], lines  # 题目里贴的代码和卡片里的行为一样
        check("read-twice", int(lines[1].split()[2]))

    with_workdir(go)


FREERTOS_STUB = r"""
#include <stdint.h>
#include <stddef.h>
typedef void *QueueHandle_t; typedef uint32_t TickType_t; typedef long BaseType_t; typedef unsigned long UBaseType_t;
#define pdPASS ( 1 )
#define pdFALSE ( 0 )
#define portMAX_DELAY ( ( TickType_t ) 0xffffffffUL )
#ifndef configTICK_RATE_HZ
#define configTICK_RATE_HZ ( ( TickType_t ) 1000 )
#endif
/* FreeRTOS-Kernel include/projdefs.h */
#define pdMS_TO_TICKS( xTimeInMs ) ( ( TickType_t ) ( ( ( uint64_t ) ( xTimeInMs ) * ( uint64_t ) configTICK_RATE_HZ ) / ( uint64_t ) 1000U ) )
TickType_t xTaskGetTickCount(void);
QueueHandle_t xQueueCreate(UBaseType_t len, UBaseType_t item_size);
BaseType_t xQueueSend(QueueHandle_t q, const void *item, TickType_t wait);
BaseType_t xQueueReceive(QueueHandle_t q, void *item, TickType_t wait);
BaseType_t xQueueSendFromISR(QueueHandle_t q, const void *item, BaseType_t *woken);
#define portYIELD_FROM_ISR( x ) ( ( void ) ( x ) )
void vTaskDelayUntil(TickType_t *prev, TickType_t inc);
BaseType_t xTaskCreate(void (*fn)(void *), const char *name, uint32_t depth, void *arg, UBaseType_t prio, void *handle);
void vTaskStartScheduler(void);
int16_t read_sensor(void); void process(int16_t v); void send_packet(const void *p, size_t n);
struct uart_regs { volatile uint32_t DR; }; extern struct uart_regs *UART; extern QueueHandle_t rx_q;
"""


def test_freertos_code_with_gcc() -> None:
    blocks = [b for c in CARDS for b in code_blocks(c.get("body", ""), "c")]
    full = next(b for b in blocks if "void comm_task" in b)
    periodic = next(b for b in blocks if "process(v);" in b and "vTaskDelayUntil" in b)
    isr = next(b for b in blocks if "UART_IRQHandler" in b)
    create = next(b for b in blocks if "xTaskCreate(sample_task" in b)
    head, _, rest = create.partition("\n")
    create_tu = head + "\nint main(void)\n{\n" + rest + "\n}\n"
    main_q = ("\nint main(void)\n{\n    q = xQueueCreate(32, sizeof(int16_t));\n"
              "    xTaskCreate(sample_task, \"sample\", 256, NULL, 3, NULL);\n"
              "    xTaskCreate(comm_task, \"comm\", 512, NULL, 2, NULL);\n    vTaskStartScheduler();\n}\n")
    ticks = "\n#include <stdio.h>\nint main(void) { printf(\"%u %u\\n\", (unsigned)pdMS_TO_TICKS(10), (unsigned)(1000 / configTICK_RATE_HZ)); }\n"

    def go(work: Path, w: str):
        units = {"full.c": full + main_q, "periodic.c": periodic, "isr.c": isr, "create.c": create_tu}
        for name, body in units.items():
            (work / name).write_text(FREERTOS_STUB + body, encoding="utf-8")
        (work / "ticks.c").write_text("#define configTICK_RATE_HZ ( ( TickType_t ) 250 )\n" + FREERTOS_STUB + ticks, encoding="utf-8")
        cmds = " && ".join(f"gcc -std=c11 -Wall -Wextra -Wno-unused-parameter -Werror -fsyntax-only {n}" for n in units)
        r = wsl(f"cd {w} && {cmds} && gcc -std=c11 -Wall -Werror ticks.c -o ticks && ./ticks")
        assert r.returncode == 0, (r.stdout, r.stderr)
        assert r.stdout.split() == ["2", "4"], r.stdout  # 250 Hz：pdMS_TO_TICKS(10) = 2，节拍 4 ms

    with_workdir(go)


def test_posix_with_gcc() -> None:
    nano = next(b for c in CARDS for b in code_blocks(c.get("body", ""), "c") if "TIMER_ABSTIME" in b)
    loop = nano.replace("for (;;)", "for (int it = 0; it < 20; it++)")
    prog = r"""
#define _GNU_SOURCE
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <errno.h>
#include <mqueue.h>
#include <fcntl.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
static void *noop(void *a) { return a; }
static double now_ms(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e3 + t.tv_nsec / 1e6; }
static void do_sample(void) { double s = now_ms(); while (now_ms() - s < 2.0) { } }  /* 2 ms 的工作 */
static double run_abs(void) {
    double start = now_ms();
LOOP
    return now_ms() - start;
}
int main(void) {
    pthread_mutexattr_t at; int p;
    pthread_mutexattr_init(&at);
    pthread_mutexattr_getprotocol(&at, &p);
    printf("default %s\n", p == PTHREAD_PRIO_NONE ? "PTHREAD_PRIO_NONE" : "other");
    pthread_mutexattr_setprotocol(&at, PTHREAD_PRIO_INHERIT);
    pthread_mutexattr_getprotocol(&at, &p);
    printf("set %s\n", p == PTHREAD_PRIO_INHERIT ? "PTHREAD_PRIO_INHERIT" : "other");
    pthread_mutexattr_setprotocol(&at, PTHREAD_PRIO_PROTECT);
    pthread_mutexattr_getprotocol(&at, &p);
    printf("protect %s\n", p == PTHREAD_PRIO_PROTECT ? "ok" : "other");

    pthread_attr_t a; pthread_t tid;
    struct sched_param sp = { .sched_priority = 80 };
    pthread_attr_init(&a);
    pthread_attr_setinheritsched(&a, PTHREAD_EXPLICIT_SCHED);
    pthread_attr_setschedpolicy(&a, SCHED_FIFO);
    pthread_attr_setschedparam(&a, &sp);
    int err = pthread_create(&tid, &a, noop, NULL);
    if (!err) pthread_join(tid, NULL);
    printf("create %d euid %d EPERM %d\n", err, (int)geteuid(), EPERM);

    struct mq_attr ma = { .mq_maxmsg = 8, .mq_msgsize = 16 };
    mq_unlink("/h32verify");
    mqd_t q = mq_open("/h32verify", O_CREAT | O_RDWR, 0600, &ma);
    if (q == (mqd_t)-1) { perror("mq_open"); return 1; }
    mq_send(q, "a", 2, 1); mq_send(q, "b", 2, 5); mq_send(q, "c", 2, 1);
    char buf[16]; unsigned pr;
    printf("mq");
    for (int i = 0; i < 3; i++) { mq_receive(q, buf, sizeof buf, &pr); printf(" %s", buf); }
    printf("\n");
    mq_close(q); mq_unlink("/h32verify");

    sigset_t s; int sig;
    sigemptyset(&s); sigaddset(&s, SIGUSR1);
    pthread_sigmask(SIG_BLOCK, &s, NULL);
    raise(SIGUSR1);
    sigwait(&s, &sig);
    printf("sigwait %s\n", sig == SIGUSR1 ? "SIGUSR1" : "other");

    printf("abs %.1f\n", run_abs());
    return 0;
}
""".replace("LOOP", loop)

    def go(work: Path, w: str):
        (work / "posix.c").write_text(prog, encoding="utf-8")
        r = wsl(f"cd {w} && gcc -std=gnu11 -Wall -Werror -pthread posix.c -o posix -lrt && ./posix")
        assert r.returncode == 0, (r.stdout, r.stderr)
        out = dict(line.split(" ", 1) for line in r.stdout.strip().splitlines())
        assert out["default"] == "PTHREAD_PRIO_NONE" and out["set"] == "PTHREAD_PRIO_INHERIT" and out["protect"] == "ok"
        err, _, euid, _, eperm = out["create"].split()
        if euid != "0":
            assert err == eperm == "1", out["create"]  # 普通用户：EPERM（值为 1）
        assert out["mq"] == "b a c"
        assert out["sigwait"] == "SIGUSR1"
        # 20 圈，每圈 2 ms 工作，绝对时间每 10 ms：约 200 ms；若按相对时间睡会到 240 ms 左右
        assert 195 <= float(out["abs"]) < 225, out["abs"]

    with_workdir(go)


# ------------------------------------------------------------------ 3. 真实系统读数
def test_system_readings() -> None:
    r = wsl("uname -r; chrt -m; cat /proc/sys/kernel/sched_rr_timeslice_ms; getconf PAGESIZE; "
            "zcat /proc/config.gz | grep -E '^CONFIG_PREEMPT_NONE=|^# CONFIG_PREEMPT_RT is not set'")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    if "microsoft" not in lines[0].lower():
        print("skip system readings: not a WSL kernel")
        return
    text = r.stdout
    assert "SCHED_FIFO min/max priority\t: 1/99" in text and "SCHED_RR min/max priority\t: 1/99" in text
    assert "SCHED_DEADLINE min/max priority\t: 0/0" in text
    assert "\n100\n" in text and "\n4096\n" in text
    assert "CONFIG_PREEMPT_NONE=y" in text and "# CONFIG_PREEMPT_RT is not set" in text


if __name__ == "__main__":
    tests = [test_startup_math, test_device_tree_math, test_loop_and_rtos_math, test_timelines,
             test_schedulability, test_queue_math, test_latency_math, test_memory_math,
             test_power_and_watchdog, test_sims_and_texts, test_sections_with_gcc,
             test_char_driver_read_with_gcc, test_freertos_code_with_gcc, test_posix_with_gcc,
             test_system_readings]
    for t in tests:
        t()
    # 文档事实：pr_err 是 KERN_ERR，Documentation/core-api/printk-basics.rst 的表格里是 "3"
    check("err-level", 3)
    numeric = [k for k, v in ITEMS.items() if v.get("type") == "number"]
    missing = sorted(set(numeric) - CHECKED)
    assert not missing, f"number items without a check: {missing}"
    print(f"ok  H.3.2.verify.py: {len(tests)} checks, {len(numeric)} number items, nm/size + driver read + "
          "FreeRTOS syntax + POSIX (PI, EPERM, mq, sigwait, abs sleep) under WSL gcc, chrt/sysctl/config readings")
