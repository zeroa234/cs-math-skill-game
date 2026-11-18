"""H.3.1 单片机与微控制器：GPIO 位掩码、定时分频、UART/ADC/PWM/输入捕获、平均功耗与 WSL gcc 真实 C 代码实测。"""
from fractions import Fraction as F
from pathlib import Path
import re
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[2]
PACK = (ROOT / "data/content/H.3.1.yaml").read_text(encoding="utf-8")


def debounce(samples: list[int], stable: int = 1, threshold: int = 3):
    cnt = 0
    for idx, raw in enumerate(samples, 1):
        if raw != stable:
            cnt += 1
            if cnt >= threshold:
                stable = raw
                cnt = 0
                yield idx, stable
        else:
            cnt = 0


def test_gpio_and_ram_math() -> None:
    assert (1 << 5) == 32
    assert (2 | 32, 4 | 32, 8 | 32) == (34, 36, 40)
    assert (34 & ~(1 << 5)) == 2
    assert 8 - 3 - 2 == 3

    assert list(debounce([0, 0, 1, 0, 0, 0], stable=1, threshold=3)) == [(6, 0)]
    assert list(debounce([0, 1, 0, 0, 0], stable=1, threshold=3)) == [(5, 0)]


def test_timer_uart_adc_pwm_sleep() -> None:
    # 16 MHz / 64 = 250 kHz -> 1 ms = 250 counts -> compare 249 (C4 Q2)
    f_cnt = 16_000_000 // 64
    assert f_cnt == 250_000
    assert f_cnt * F(1, 1000) - 1 == 249
    assert (249 + 1) * F(1000, f_cnt) == 1  # 1 ms

    # 8 MHz / 8 = 1 MHz -> 500 us = 500 counts -> compare 499
    assert (8_000_000 // 8) * F(500, 1_000_000) - 1 == 499

    # UART 8N1 (C4 Q5)
    assert F(115200, 1 + 8 + 1) == 11520
    assert F(9600, 1 + 8 + 1) == 960

    # ADC & PWM & Input Capture
    step_8b = F("2.56") / 256
    assert step_8b == F("0.01")
    assert F("1.28") / step_8b == 128
    assert F("0.91") / step_8b == 91
    assert 12 * F("0.25") == 3
    assert F(3, 10) * 100 == 30
    assert (14 - 250) % 256 == 20

    # Average sleep current
    assert F("0.1") * 11 + F("0.9") * F("0.9") == F("1.91")
    assert F("0.1") * 11 + F("0.9") * 1 == 2
    assert F("0.2") * 9 + F("0.8") * 1 == F("2.6")


def test_embedded_c_with_wsl_gcc() -> None:
    c_blocks = [m.group(1).strip() for m in re.finditer(r"```c\n(.*?)```", PACK, re.S)]
    assert len(c_blocks) >= 3, f"Expected >= 3 C snippets in H.3.1.yaml, found {len(c_blocks)}"
    debounce_fn = next((b for b in c_blocks if "every_1ms" in b), None)
    assert debounce_fn, "Missing every_1ms debounce C snippet"

    c_prog = f"""
#include <stdio.h>
#include <stdint.h>
#include <assert.h>

/* Extracted verbatim debounce function + declarations from H.3.1.yaml */
{debounce_fn}

static uint32_t fake_gpio_dir = 0u;
static uint32_t fake_gpio_out = 2u; /* pin 1 initially high */

#define TEST_GPIO_DIR (*(volatile uint32_t *)&fake_gpio_dir)
#define TEST_GPIO_OUT (*(volatile uint32_t *)&fake_gpio_out)

int main(void) {{
    TEST_GPIO_DIR |= (1u << 5);
    TEST_GPIO_OUT |= (1u << 5);
    assert(fake_gpio_dir == 32u);
    assert(fake_gpio_out == 34u);
    TEST_GPIO_OUT &= ~(1u << 5);
    assert(fake_gpio_out == 2u);

    /* Run exact every_1ms for 19 zeros -> stable must stay 1, on 20th zero -> flips to 0 */
    for (int i = 0; i < 19; i++) {{
        every_1ms(0);
        assert(stable == 1);
    }}
    every_1ms(0);
    assert(stable == 0 && cnt == 0);

    /* Wraparound 8-bit uint8_t input capture arithmetic */
    uint8_t start = 250u, end = 14u;
    uint8_t width = (uint8_t)(end - start);
    assert(width == 20u);

    printf("PASS_EMBEDDED_C\\n");
    return 0;
}}
"""
    work_dir = ROOT / "temp" / f"h31-gcc-{uuid.uuid4().hex[:8]}"
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        (work_dir / "test_fw.c").write_text(c_prog, encoding="utf-8")
        wsl_dir = f"/mnt/d/agent/projects/cs-math-skill-game/temp/{work_dir.name}"
        res = subprocess.run(
            ["wsl", "bash", "-c", f"gcc -std=c11 -O2 -Wall -Wextra -Werror {wsl_dir}/test_fw.c -o {wsl_dir}/test_fw && {wsl_dir}/test_fw"],
            capture_output=True, text=True, encoding="utf-8", check=False, timeout=15,
        )
        assert res.returncode == 0, (res.returncode, res.stdout, res.stderr)
        assert "PASS_EMBEDDED_C" in res.stdout, res.stdout
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    test_gpio_and_ram_math()
    test_timer_uart_adc_pwm_sleep()
    test_embedded_c_with_wsl_gcc()
    print("ok  H.3.1.verify.py: GPIO/debounce + Timer 249/499 + UART 11520 + ADC/PWM + WSL gcc -O2 C check")