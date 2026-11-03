# Checks every output, number and error that data/content/C.2.1.yaml states.
# C programs (fork, exec, wait, threads, locks, semaphores, files, links, permissions) are compiled with gcc and run
# on 64-bit Linux; the scheduling, paging, TLB, page-replacement and file-system numbers are recomputed here in
# Python with small simulations written independently of the game's sim code (src/game/sims/logic/os.js).
# Facts quoted from OSTEP (v1.10) and CS:APP 12.4 were checked against the text (reports/coverage/C.2.1.md).
# usage: python -I tests/content/C.2.1.verify.py   (prints "N/N claims hold"; exit code 1 on any mismatch)
# Uses gcc on PATH if it is there, otherwise WSL's gcc (wsl.exe -e ...). Scratch files go to temp/c21-verify.
import os, shutil, subprocess, sys
from fractions import Fraction as F

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORK = os.path.join(ROOT, "temp", "c21-verify")
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(WORK, exist_ok=True)
NATIVE = shutil.which("gcc") and sys.platform != "win32"

def wsl_path(p):
    p = os.path.abspath(p).replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:] if p[1] == ":" else p

def sh(cmd, timeout=120):
    """Run a shell command in the work directory; returns (exit code, stdout, stderr)."""
    if NATIVE:
        r = subprocess.run(["sh", "-c", cmd], cwd=WORK, capture_output=True, timeout=timeout)
    else:
        r = subprocess.run(["wsl.exe", "-e", "sh", "-c", f"cd '{wsl_path(WORK)}' && {cmd}"], capture_output=True, timeout=timeout)
    dec = lambda b: b.decode("utf-8", "replace").replace("\r", "")
    return r.returncode, dec(r.stdout), dec(r.stderr)

HEAD = ("#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <unistd.h>\n#include <fcntl.h>\n"
        "#include <errno.h>\n#include <sys/wait.h>\n#include <sys/stat.h>\n#include <pthread.h>\n#include <semaphore.h>\n#include <dirent.h>\n")
n = 0
def write(name, text):
    with open(os.path.join(WORK, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def build(src):
    global n
    n += 1
    name = f"t{n}"
    write(name + ".c", HEAD + src)
    rc, _, err = sh(f"gcc -w -O0 -pthread -o {name} {name}.c")
    if rc:
        raise SystemExit(f"compile error in {name}.c:\n{err}")
    return name

def run(src, before="", args=""):
    """Compile a whole program and run it (after an optional shell prelude); returns (stdout, exit code)."""
    name = build(src)
    rc, out, _ = sh(f"{before} ./{name} {args}")
    return out, rc

checks = []
add = lambda got, want, what="": checks.append((got, want, what))

# ======================================================================== C programs
# ---------------- fork-wait-exec
HELLO_BYE = 'int main(void) { printf("hello\\n"); fork(); printf("bye\\n"); return 0; }\n'
name = build(HELLO_BYE)
_, tty, _ = sh(f"script -qc ./{name} /dev/null")                       # a terminal: line-buffered stdout
add((tty.count("hello"), tty.count("bye")), (1, 2), "guess: hello once, bye twice in a terminal")
FORK_BUF = 'int main(void) { printf("hello\\n"); fork(); return 0; }\n'
name = build(FORK_BUF)
sh(f"./{name} > out.txt; sleep 1")                                     # the child may still be flushing when the parent exits
add(sh("cat out.txt")[1].count("hello"), 2, "fork-buffer: redirected to a file the buffer is copied, 2 lines")
_, tty, _ = sh(f"script -qc ./{name} /dev/null")
add(tty.count("hello"), 1, "fork-buffer: in a terminal only 1")
out, _ = run('int main(void) { int rc = fork();\n if (rc == 0) { printf("child %d\\n", (int) getpid()); }\n'
             ' else { wait(NULL); printf("parent %d\\n", rc); } return 0; }\n')
lines = out.split()
add(lines[0] == "child" and lines[2] == "parent" and lines[1] == lines[3], True, "fork returns the child's pid in the parent, 0 in the child")
add(run('int main(void) { int rc = fork(); if (rc == 0) { return 0; } int w = wait(NULL); printf("%d\\n", w == rc); return 0; }\n')[0], "1\n", "wait returns the child's pid")
orders = set()
name = build('int main(void) { int rc = fork(); if (rc == 0) { printf("child\\n"); } else { wait(NULL); printf("parent\\n"); } return 0; }\n')
for _ in range(20): orders.add(sh(f"./{name}")[1])
add(orders, {"child\nparent\n"}, "with wait the child always prints first")
add(run('int main(void) { int x = 1; if (fork() == 0) { x++; printf("child %d\\n", x); }\n else { wait(NULL); printf("parent %d\\n", x); } return 0; }\n')[0],
    "child 2\nparent 1\n", "fork-x: child 2, parent 1 (the skill tree's exercise 1)")
write("p3.c", "one two\nthree\n")
out, _ = run('int main(void) { char *args[3] = { "wc", "p3.c", NULL }; execvp(args[0], args); printf("this shouldn\'t print out"); return 0; }\n')
add(("shouldn" not in out, out.split()[:3]), (True, ["2", "3", "14"]), "exec-return: after a successful exec the old code is gone (wc printed its counts)")
add(run('int main(void) { char *args[2] = { "no-such-program-xyz", NULL }; int r = execvp(args[0], args); printf("%d\\n", r); return 0; }\n')[0], "-1\n",
    "a failed exec returns -1 and the code after it runs")
out, _ = run('int main(void) { int rc = fork(); if (rc == 0) { close(1); int fd = open("newfile.txt", O_CREAT|O_WRONLY|O_TRUNC, 0600);\n'
             ' char *args[3] = { "wc", "p3.c", NULL }; execvp(args[0], args); } else { wait(NULL); printf("fd test done\\n"); } return 0; }\n')
add((out, sh("cat newfile.txt")[1].split()[:3]), ("fd test done\n", ["2", "3", "14"]), "shell-order: close(1), open gets 1, exec wc writes into the file")
add(run('int main(void) { close(1); int fd = open("x.txt", O_CREAT|O_WRONLY|O_TRUNC, 0600); dprintf(2, "%d\\n", fd); return 0; }\n', args="2>&1")[0], "1\n",
    "open returns the lowest free descriptor (1 after close(1))")

# ---------------- threads-intro
name = build('void *mythread(void *arg) { printf("%s\\n", (char *) arg); return NULL; }\n'
             'int main(void) { pthread_t p1, p2; printf("main: begin\\n"); pthread_create(&p1, NULL, mythread, "A");\n'
             ' pthread_create(&p2, NULL, mythread, "B"); pthread_join(p1, NULL); pthread_join(p2, NULL); printf("main: end\\n"); return 0; }\n')
seen = set()
for _ in range(40): seen.add(sh(f"./{name}")[1])
add(seen <= {"main: begin\nA\nB\nmain: end\n", "main: begin\nB\nA\nmain: end\n"}, True, "join-output: main begin first, main end last, A/B in either order")

# ---------------- memory-model (CS:APP sharing.c)
out, _ = run('char **ptr;\nvoid *thread(void *vargp) { long myid = (long) vargp; static int cnt = 0;\n'
             ' printf("[%ld]: %s (cnt=%d)\\n", myid, ptr[myid], ++cnt); return NULL; }\n'
             'int main(void) { long i; pthread_t tid; char *msgs[2] = { "Hello from foo", "Hello from bar" }; ptr = msgs;\n'
             ' for (i = 0; i < 2; i++) pthread_create(&tid, NULL, thread, (void *) i); pthread_exit(NULL); }\n')
add(("Hello from foo" in out and "Hello from bar" in out, sorted(l[-2] for l in out.split("\n") if l)), (True, ["1", "2"]),
    "sharing.c: both peers read main's msgs through ptr, and see one shared cnt (1 then 2)")
out, _ = run('void *t(void *a) { long myid = (long) a; printf("%p\\n", (void *) &myid); sleep(1); return NULL; }\n'
             'int main(void) { pthread_t a, b; pthread_create(&a, NULL, t, (void *) 0); pthread_create(&b, NULL, t, (void *) 1); pthread_join(a, NULL); pthread_join(b, NULL); return 0; }\n')
add(len(set(out.split())), 2, "myid-count: the two myid instances have different addresses")
add(run('int *shared; void *t(void *a) { *shared = 99; return NULL; }\n'
        'int main(void) { int local = 1; shared = &local; pthread_t x; pthread_create(&x, NULL, t, NULL); pthread_join(x, NULL); printf("%d\\n", local); return 0; }\n')[0],
    "99\n", "other-stack: a thread can write another thread's stack through a pointer")

# ---------------- race and locks (nproc >= 2 needed for the race to show)
cores = int(sh("nproc")[1].strip())
RACE = ('static volatile int counter = 0; %s\nvoid *worker(void *arg) { for (int i = 0; i < 10000000; i++) { %s counter = counter + 1; %s } return NULL; }\n'
        'int main(void) { pthread_t a, b; pthread_create(&a, NULL, worker, NULL); pthread_create(&b, NULL, worker, NULL); pthread_join(a, NULL); pthread_join(b, NULL); printf("%%d\\n", counter); return 0; }\n')
name = build(RACE % ("", "", ""))
results = [int(sh(f"./{name}")[1]) for _ in range(5)]
add(cores >= 2 and min(results) < 20000000 and max(results) <= 20000000, True, f"race guess: without a lock the count falls short ({results})")
name = build(RACE % ("pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;", "pthread_mutex_lock(&m);", "pthread_mutex_unlock(&m);"))
add({int(sh(f"./{name}")[1]) for _ in range(3)}, {20000000}, "with pthread_mutex_lock the count is exactly 20000000")
out, _ = run('int main(void) { int flag = 1; int old = __atomic_exchange_n(&flag, 1, __ATOMIC_SEQ_CST); printf("%d %d\\n", old, flag);\n'
             ' flag = 0; old = __atomic_exchange_n(&flag, 1, __ATOMIC_SEQ_CST); printf("%d %d\\n", old, flag); return 0; }\n')
add(out, "1 1\n0 1\n", "tas-held: test-and-set returns the old value (1 while held, 0 when free) and leaves 1")
out, _ = run('int main(void) { int flag = 1; int r = __sync_val_compare_and_swap(&flag, 0, 1); printf("%d %d\\n", r, flag);\n'
             ' flag = 0; r = __sync_val_compare_and_swap(&flag, 0, 1); printf("%d %d\\n", r, flag); return 0; }\n')
add(out, "1 1\n0 1\n", "cas-fail: CAS(&flag, 0, 1) on 1 returns 1 and changes nothing; on 0 returns 0 and sets 1")
out, _ = run('static int c = 0;\nvoid add_one(int *p) { int old; do { old = *p; } while (__sync_val_compare_and_swap(p, old, old + 1) != old); }\n'
             'void *w(void *a) { for (int i = 0; i < 1000000; i++) add_one(&c); return NULL; }\n'
             'int main(void) { pthread_t a, b; pthread_create(&a, NULL, w, NULL); pthread_create(&b, NULL, w, NULL); pthread_join(a, NULL); pthread_join(b, NULL); printf("%d\\n", c); return 0; }\n')
add(out, "2000000\n", "add_one with a CAS loop loses no updates")
add(4 * 10, 40, "spin-waste")
lost = {"counter": 50}; r1 = lost["counter"]; r2 = lost["counter"]; r2 += 1; lost["counter"] = r2; r1 += 1; lost["counter"] = r1
add(lost["counter"], 51, "lost-update: 50 → 51")

# ---------------- semaphores
add(run('sem_t s;\nvoid *child(void *arg) { printf("child\\n"); sem_post(&s); return NULL; }\n'
        'int main(void) { sem_init(&s, 0, 0); pthread_t c; pthread_create(&c, NULL, child, NULL); sem_wait(&s); printf("parent: end\\n"); return 0; }\n')[0],
    "child\nparent: end\n", "sem for ordering (initial value 0)")
out, _ = run('sem_t s;\nvoid *w(void *a) { sem_wait(&s); return NULL; }\n'
             'int main(void) { sem_init(&s, 0, 1); sem_wait(&s); pthread_t t; pthread_create(&t, NULL, w, NULL); sleep(1); int v; sem_getvalue(&s, &v); printf("%d\\n", v); sem_post(&s); pthread_join(t, NULL); return 0; }\n')
add(out, "0\n", "Linux semaphores never go below 0 (a waiter blocks at 0), as the sim shows")
def ostep_sem(init, waits):  # OSTEP's definition: wait decrements, sleeps if negative
    v, sleeping = init, 0
    for _ in range(waits):
        v -= 1
        if v < 0: sleeping += 1
    return v, sleeping
add(ostep_sem(1, 3), (-2, 2), "sem-negative: −2, two waiting")
out, _ = run('#define MAX 8\nint buffer[MAX]; int fill = 0, use = 0; sem_t empty, full, mutex; long total = 0;\n'
             'void put(int v) { buffer[fill] = v; fill = (fill + 1) % MAX; }\nint get(void) { int v = buffer[use]; use = (use + 1) % MAX; return v; }\n'
             'void *producer(void *a) { for (int i = 1; i <= 10000; i++) { sem_wait(&empty); sem_wait(&mutex); put(i); sem_post(&mutex); sem_post(&full); } return NULL; }\n'
             'void *consumer(void *a) { for (int i = 0; i < 10000; i++) { sem_wait(&full); sem_wait(&mutex); total += get(); sem_post(&mutex); sem_post(&empty); } return NULL; }\n'
             'int main(void) { sem_init(&empty, 0, MAX); sem_init(&full, 0, 0); sem_init(&mutex, 0, 1); pthread_t p[2], c[2];\n'
             ' for (int i = 0; i < 2; i++) { pthread_create(&p[i], NULL, producer, NULL); pthread_create(&c[i], NULL, consumer, NULL); }\n'
             ' for (int i = 0; i < 2; i++) { pthread_join(p[i], NULL); pthread_join(c[i], NULL); } printf("%ld\\n", total); return 0; }\n')
add(int(out), 2 * 10000 * 10001 // 2, "bounded buffer (empty = MAX, full = 0, mutex = 1, mutex inside): every item consumed once")
add(round(74 / 105 * 100, 1), 70.5, "lu-share")

# ---------------- files-api
write("foo", "hello\n"); write("hi.txt", "hi\n"); write("f300", "x" * 300); write("f1000", "".join(chr(48 + i % 10) for i in range(1000)))
add(run('int main(void) { char buf[4096]; int fd = open("foo", O_RDONLY); int a = read(fd, buf, 4096); int b = read(fd, buf, 4096); printf("%d %d %d\\n", fd, a, b); return 0; }\n')[0],
    "3 6 0\n", "cat foo: open → 3, read → 6, read → 0")
add(run('int main(void) { char buf[64]; int fd = open("hi.txt", O_RDONLY); int a = read(fd, buf, 64); int b = read(fd, buf, 64); printf("%d %d\\n", a, b); return 0; }\n')[0],
    "3 0\n", "strace-cat: after the 3 bytes the next read returns 0")
add(run('int main(void) { char buf[100]; int fd = open("f300", O_RDONLY); for (int i = 0; i < 4; i++) printf("%d ", (int) read(fd, buf, 100)); printf("\\n"); return 0; }\n')[0],
    "100 100 100 0 \n", "reads-300")
add(run('int main(void) { char buf[50]; int fd = open("f1000", O_RDONLY); lseek(fd, 200, SEEK_SET); read(fd, buf, 50); printf("%d\\n", (int) lseek(fd, 0, SEEK_CUR)); return 0; }\n')[0],
    "250\n", "lseek-read: 200 + 50 = 250")
add(run('int main(void) { char a[100], b[100]; int f1 = open("f1000", O_RDONLY), f2 = open("f1000", O_RDONLY); read(f1, a, 100); read(f2, b, 100);\n'
        ' printf("%d %d %d\\n", f1, f2, memcmp(a, b, 100) == 0 && b[0] == \'0\'); return 0; }\n')[0], "3 4 1\n", "two-opens: separate entries, both read bytes 0–99")
add(run('int main(void) { int fd = open("notes.txt.tmp", O_CREAT|O_WRONLY|O_TRUNC, 0644); write(fd, "new", 3); int s = fsync(fd); close(fd); int r = rename("notes.txt.tmp", "notes.txt"); printf("%d %d\\n", s, r); return 0; }\n')[0],
    "0 0\n", "atomic-update: fsync then rename both succeed")
add(sh("cat notes.txt; ls notes.txt.tmp 2>/dev/null | wc -l")[1], "new0\n", "after rename the temporary name is gone")

# ---------------- file-sharing
write("file.txt", "0123456789abcdef\n")
add(run('int main(void) { int fd = open("file.txt", O_RDONLY); int rc = fork(); if (rc == 0) { rc = lseek(fd, 10, SEEK_SET); printf("child: offset %d\\n", rc); }\n'
        ' else if (rc > 0) { (void) wait(NULL); printf("parent: offset %d\\n", (int) lseek(fd, 0, SEEK_CUR)); } return 0; }\n')[0],
    "child: offset 10\nparent: offset 10\n", "fork-seek: the offset is shared")
add(run('int main(void) { int fd = open("file.txt", O_RDONLY); int fd2 = dup(fd); printf("%d %d\\n", fd, fd2); return 0; }\n')[0], "3 4\n", "dup-number: 4")
run('int main(void) { int fd = open("out2.txt", O_WRONLY|O_CREAT|O_TRUNC, 0644); dup2(fd, 1); close(fd); printf("hi\\n"); return 0; }\n')
add(sh("cat out2.txt")[1], "hi\n", "dup2(fd, 1): printf goes into the file")
add(run('int main(void) { char *args[2] = { "ls", NULL }; int fd = open("list.txt", O_WRONLY|O_CREAT|O_TRUNC, 0644); dup2(fd, 1); close(fd); execvp("ls", args); return 1; }\n')[1], 0,
    "redirect-order: open, dup2, close, exec ls")
add("p3.c" in sh("cat list.txt")[1], True, "ls's output landed in list.txt")
write("f", "")
run('int main(void) { int a = open("f", O_WRONLY); int b = dup(a); write(a, "ab", 2); write(b, "cd", 2); return 0; }\n')
add(sh("cat f")[1], "abcd", "dup shares the offset: abcd")
write("f", "")
run('int main(void) { int a = open("f", O_WRONLY); int b = open("f", O_WRONLY); write(a, "ab", 2); write(b, "cd", 2); return 0; }\n')
add(sh("cat f")[1], "cd", "two opens: cd overwrites ab")
write("f", "")
run('int main(void) { int a = open("f", O_WRONLY); int b = open("f", O_WRONLY); write(a, "xyz", 3); write(b, "Q", 1); return 0; }\n')
add(sh("cat f")[1], "Qyz", "two-opens-write: Qyz")

# ---------------- dirs-metadata
add(sh("echo hello > file && stat -c '%s %h' file")[1], "6 1\n", "stat-size: 6 bytes, 1 link")
add(run('int main(void) { struct stat st; stat("file", &st); printf("%ld %ld\\n", (long) st.st_size, (long) st.st_nlink); return 0; }\n')[0], "6 1\n",
    "stat() fills st_size and st_nlink")
add(run('int main(void) { int r = unlink("file"); printf("%d %d\\n", r, access("file", F_OK)); return 0; }\n')[0], "0 -1\n", "unlink returns 0 and the name is gone")
out, _ = run('int main(void) { mkdir("d", 0777); DIR *dp = opendir("d"); struct dirent *e; int k = 0; while ((e = readdir(dp)) != NULL) { printf("%s\\n", e->d_name); k++; } closedir(dp); printf("%d\\n", k); return 0; }\n')
add(sorted(out.split()), sorted([".", "..", "2"]), "empty-dir: an empty directory has . and ..")
out, _ = run('int main(void) { mkdir("full", 0777); close(open("full/a", O_CREAT|O_WRONLY, 0644)); close(open("full/b", O_CREAT|O_WRONLY, 0644));\n'
             ' int r = rmdir("full"); printf("%d %s\\n", r, strerror(errno)); unlink("full/a"); unlink("full/b"); printf("%d\\n", rmdir("full")); return 0; }\n')
add(out, "-1 Directory not empty\n0\n", "rmdir-nonempty fails; after unlinking the files it works")
add(run('int main(void) { int fd = open(".", O_WRONLY); printf("%d %s\\n", fd, strerror(errno)); return 0; }\n')[0], "-1 Is a directory\n",
    "no-write-dir: a directory cannot be opened for writing")

# ---------------- links-permissions
# These run in a directory on a native Linux file system: on WSL the project lives on DrvFs (/mnt/d), where chmod has
# no effect. Under WSL this is /tmp inside the distro (a few small files, removed at the end).
L = "/tmp/c21-verify-links"
lsh = lambda cmd: sh(f"rm -rf {L} 2>/dev/null; mkdir -p {L} && cd {L} && {cmd}")
HERE = WORK if NATIVE else wsl_path(WORK)
add(lsh("echo hello > file && ln file file2 && rm file && cat file2")[1], "hello\n", "guess: after rm file, file2 still reads hello")
add(len(set(lsh("echo hello > a.txt && ln a.txt b.txt && stat -c %i a.txt b.txt")[1].split())), 1, "hard-link-inode: same inode number")
add(lsh("echo hello > file && stat -c %h file && ln file file2 && stat -c %h file && ln file2 file3 && stat -c %h file && rm file && stat -c %h file2")[1].split(),
    ["1", "2", "3", "2"], "link counts 1, 2, 3, 2 (OSTEP's example)")
add(lsh("touch a && ln a b && ln a c && rm b && ln c d && stat -c %h a")[1], "3\n", "link-count: 3")
add(lsh("touch x && ln x y && ln y z && rm x && rm y && stat -c %h z")[1], "1\n", "link-boss: 1")
add(lsh("ln -s /tmp/data.txt link && stat -c %s link")[1], "13\n", "symlink-size: 13")
add(lsh("echo hello > file && ln -s file file2 && stat -c %s file2 && echo hello > alongerfilename && ln -s alongerfilename file3 && stat -c %s file3")[1].split(),
    ["4", "15"], "symlink sizes 4 and 15 (OSTEP's examples)")
name = build('int main(void) { int fd = open("file2", O_RDONLY); printf("%d %s\\n", fd, strerror(errno)); return 0; }\n')
add(lsh(f"echo hello > file && ln -s file file2 && rm file && {HERE}/{name}")[1], "-1 No such file or directory\n", "dangling symlink: No such file or directory")
add(lsh("mkdir d && ln -s d dlink && (ln d hlink 2>/dev/null; echo $?) && [ -L dlink ] && echo sym")[1], "1\nsym\n",
    "hard links to a directory are refused, symbolic links to it work")
add(lsh("touch foo.txt && chmod 600 foo.txt && stat -c %A foo.txt && chmod 750 foo.txt && stat -c %A foo.txt && chmod 644 foo.txt && stat -c %A foo.txt")[1].split(),
    ["-rw-------", "-rwxr-x---", "-rw-r--r--"], "chmod 600 / 750 / 644")
out = lsh("printf '#!/bin/sh\\necho hello, from shell world.\\n' > hello.sh && chmod 700 hello.sh && ./hello.sh && chmod 600 hello.sh && (./hello.sh 2>&1; true)")[1]
add((out.count("hello, from shell world."), out.count("Permission denied")), (1, 1), "chmod 600 removes the execute bit: Permission denied")
name = build('int main(void) { int r = chdir("nox"); printf("%d %s\\n", r, strerror(errno)); return 0; }\n')
add(lsh(f"mkdir nox && chmod 600 nox && {HERE}/{name}; chmod 700 nox")[1], "-1 Permission denied\n", "dir-x: without x on a directory chdir fails")
add(sorted(lsh("mkdir d && touch f && ln -s f l && ls -ld d f l | cut -c1")[1].split()), ["-", "d", "l"], "ls-type: d, l, -")
sh(f"rm -rf {L}")

# ---------------- boss
add(run('int main(void) { int x = 5; if (fork() == 0) { x = x * 2; printf("child %d\\n", x); } else { wait(NULL); printf("parent %d\\n", x); } return 0; }\n')[0],
    "child 10\nparent 5\n", "fork-boss")

# ======================================================================== numbers
# ---------------- scheduling: an independent simulator with the conventions the lessons state
def schedule(procs, algo, q=None):
    procs = [dict(name=a, arrive=b, burst=c, left=c, i=i) for i, (a, b, c) in enumerate(procs)]
    t, run, slice_, queue, tl = 0, None, 0, [], []
    key_arr = lambda p: (p["arrive"], p["i"])
    if algo == "RR": queue = sorted([p for p in procs if p["arrive"] == 0], key=key_arr)
    while any(p["left"] for p in procs):
        ready = [p for p in procs if p["arrive"] <= t and p["left"]]
        if algo == "FCFS": pick = run if run and run["left"] else min(ready, key=key_arr, default=None)
        elif algo == "SJF": pick = run if run and run["left"] else min(ready, key=lambda p: (p["burst"],) + key_arr(p), default=None)
        elif algo == "SRTF":
            best = min(ready, key=lambda p: (p["left"],) + key_arr(p), default=None)
            pick = run if run and run["left"] and best and run["left"] <= best["left"] else best
        else:
            pick = run if run and run["left"] and slice_ < q else (queue.pop(0) if queue else None)
            if pick is not run: slice_ = 0
        tl.append(pick["name"] if pick else None)
        if pick:
            pick["left"] -= 1; slice_ += 1
            if not pick["left"]: pick["end"] = t + 1
        run = pick; t += 1
        if algo == "RR":
            queue += sorted([p for p in procs if p["arrive"] == t], key=key_arr)
            if run and run["left"] and slice_ >= q: queue.append(run); run = None
            elif run and not run["left"]: run = None
    turn = {p["name"]: p["end"] - p["arrive"] for p in procs}
    wait = {p["name"]: p["end"] - p["arrive"] - p["burst"] for p in procs}
    first = {p["name"]: tl.index(p["name"]) - p["arrive"] for p in procs}
    avg = lambda d: F(sum(d.values()), len(d))
    return "".join(x or "." for x in tl), avg(turn), avg(wait), avg(first)

add(schedule([("A", 0, 10), ("B", 0, 10), ("C", 0, 10)], "FCFS")[1], 20, "FIFO A, B, C of 10 s: 20")
add(schedule([(c, 0, 5) for c in "ABCD"], "FCFS")[1], F(25, 2), "fifo-four: 12.5")
add(schedule([("A", 0, 100), ("B", 0, 10), ("C", 0, 10)], "FCFS")[1], 110, "convoy: 110")
add(round(float(schedule([("A", 0, 60), ("B", 0, 10), ("C", 0, 20)], "FCFS")[1]), 2), 73.33, "convoy item: 73.33")
add(30 - 9, 21, "turnaround-one"); add(12 - 1 - 4, 7, "waiting-time example")
EX = [("1", 0, 8), ("2", 1, 4), ("3", 2, 9), ("4", 3, 5)]
add([schedule(EX, a, 4)[2] for a in ("FCFS", "SJF", "RR")], [F(35, 4), F(31, 4), F(47, 4)], "the skill tree's exercise 2: 8.75, 7.75, 11.75")
add(schedule(EX, "RR", 4)[0], "11112222333344441111333343", "RR q = 4 timeline as the worked example lists it")
add(schedule([("A", 0, 4), ("B", 1, 3), ("C", 2, 2)], "FCFS")[0], "AAAABBBCC", "fcfs-sim")
add(schedule([("X", 0, 6), ("Y", 2, 3), ("Z", 4, 1)], "FCFS")[2], 3, "fcfs-wait: 3")
add(schedule([("B", 0, 10), ("C", 0, 10), ("A", 0, 100)], "FCFS")[1], 50, "sjf guess: B, C, A → 50")
add(schedule([("a", 0, 8), ("b", 0, 4), ("c", 0, 2)], "SJF")[1], F(22, 3), "sjf-three: 22/3")
add(round(float(schedule([("A", 0, 100), ("B", 10, 10), ("C", 10, 10)], "SJF")[1]), 2), 103.33, "SJF with late arrivals: 103.33")
add(schedule([("A", 0, 100), ("B", 10, 10), ("C", 10, 10)], "SRTF")[1], 50, "stcf-avg: 50")
P4 = [("A", 0, 7), ("B", 2, 4), ("C", 4, 1), ("D", 5, 4)]
add(schedule(P4, "SJF")[0], "AAAAAAACBBBBDDDD", "sjf-sim")
add(schedule(P4, "SRTF")[0], "AABBCBBDDDDAAAAA", "STCF demo timeline A 0–2, B 2–4, C 4–5, B 5–7, D 7–11, A 11–16")
add(schedule(P4, "SRTF")[2], 3, "stcf-wait: 3")
add(schedule([("A", 0, 5), ("B", 0, 5), ("C", 0, 5)], "SJF")[3], 5, "sjf-response: 5")
add(schedule([("A", 0, 5), ("B", 0, 5), ("C", 0, 5)], "RR", 1)[3], 1, "RR slice 1 response: 1")
add(schedule([("A", 0, 5), ("B", 0, 5), ("C", 0, 5)], "RR", 2)[3], 2, "rr-response: 2")
add(schedule([("A", 0, 5), ("B", 0, 5), ("C", 0, 5)], "RR", 1)[1], 14, "RR turnaround 13, 14, 15 → 14")
add(schedule([("A", 0, 5), ("B", 0, 5), ("C", 0, 5)], "FCFS")[1], 10, "FIFO for the same three: 10")
add(schedule([("A", 0, 3), ("B", 0, 3)], "RR", 1)[1], F(11, 2), "rr-turnaround: 5.5")
add(round(1 / 51 * 100, 2), 1.96, "amortize: 1.96 %"); add((round(1 / 11 * 100), round(1 / 101 * 100, 2)), (9, 0.99), "≈10 % and < 1 % (OSTEP)")
add(schedule([("A", 0, 5), ("B", 1, 3), ("C", 2, 1)], "RR", 2)[0], "AABBCAABA", "rr-sim")
add(schedule([("A", 0, 5), ("B", 1, 3), ("C", 2, 1)], "RR", 2)[2], F(10, 3), "rr-wait: 10/3")
add(schedule([("A", 0, 100), ("B", 10, 10), ("C", 10, 10)], "SRTF")[3], F(10, 3), "STCF response 0, 0, 10 → 3.33 (OSTEP: A at 0, B and C at 10)")
add(schedule([("P1", 0, 5), ("P2", 1, 3), ("P3", 2, 8), ("P4", 3, 6)], "SJF")[2], F(21, 4), "sjf-boss: 5.25")
add(3 * 10, 30, "drop-time: three drops of 10 ms")

# ---------------- base and bounds, paging
add((32768 + 1000, 16384 + 3000, 4400 >= 4096, 16384 + 1024, 128 + 32768, 15 * 1024 + 32768, 47 * 1024), (33768, 19384, True, 17408, 32896, 48128, 48128),
    "base-bounds numbers")
add(16 - (1 + 2 + 1), 12, "internal-frag")
def tr(va, page, table):
    vpn, off = divmod(va, page); return table[vpn] * page + off
add((tr(21, 16, [3, 7, 5, 2]), divmod(21, 16), format(21, "06b"), format(117, "07b")), (117, (1, 5), "010101", "1110101"), "21 → 117")
add((tr(50, 16, [3, 7, 5, 2]), divmod(50, 16)), (34, (3, 2)), "translate-50")
add((divmod(9029, 4096), tr(9029, 4096, [5, None, 7])), ((2, 837), 29509), "translate-fault: 9029 → 29509")
add((32 - 12, 2 ** 20 * 4 // 2 ** 20, 100 * 4), (20, 4, 400), "pt-size: 4 MB, 400 MB for 100 processes")
add((hex(0x00403ABC >> 12), hex(0x00403ABC & 0xFFF)), ("0x403", "0xabc"), "vpn-hex")
add(4096 + 5 * 4, 4116, "pte-addr")
# ---------------- TLB: an LRU TLB over the array accesses
def tlb_run(addrs, page, entries=16):
    tlb, res = [], []
    for a in addrs:
        v = a // page
        if v in tlb: res.append("hit"); tlb.remove(v)
        else:
            res.append("miss")
            if len(tlb) == entries: tlb.pop(0)
        tlb.append(v)
    return res
arr = [100 + 4 * i for i in range(10)]
r16 = tlb_run(arr, 16)
add(([a // 16 for a in (arr[0], arr[2], arr[3], arr[6], arr[7], arr[9])], r16, r16.count("hit") * 10), ([6, 6, 7, 7, 8, 8], ["miss", "hit", "hit", "miss", "hit", "hit", "hit", "miss", "hit", "hit"], 70),
    "OSTEP's array: pages 6, 7, 8 and a 70 % hit rate")
add(tlb_run(arr, 32).count("hit") * 10, 80, "tlb-32: 80 %")
add(tlb_run(arr + arr, 16)[10:].count("hit"), 10, "second-pass: 10 hits")
add(tlb_run([1, 2, 3, 4, 5] * 4, 1, entries=4)[5:].count("hit"), 0, "lru-loop: 0 hits")
add((64 * 4, 64 * 4), (256, 256), "coverage: 256 KB; with 4 MB pages 256 MB")
# ---------------- multi-level page tables
add((2 ** 18 * 4 // 2 ** 20, 2 ** 16 * 4 // 1024), (1, 256), "16 KB pages → 1 MB; big-pages (64 KB) → 256 KB")
add((14 - 6, 256 * 4, 1024 // 64, 64 // 4, 16 .bit_length() - 1), (8, 1024, 16, 16, 4), "16 KB space, 64-byte pages: 8-bit VPN, 1 KB table, 16 pages of 16 PTEs, 4-bit directory index")
va = 0x3F80
add(((va >> 6), (va >> 6) >> 4, (va >> 6) & 0xF, hex(55 * 64 + (va & 63))), (254, 15, 14, "0xdc0"), "0x3F80 → VPN 254, PD 15, PT 14, 0x0DC0")
add((55 * 64 + (0x3F85 & 63), hex(55 * 64 + 5)), (3525, "0xdc5"), "ml-translate: 3525")
add((30 - 9, 512 // 4, 21 - 7, 2 ** 14 * 4 // 512, 4096 // 4), (21, 128, 14, 128, 1024), "512-byte pages: 21-bit VPN, 128 PTEs per page, a 2^14-entry directory spans 128 pages; 4 KB / 4 = 1024")
# ---------------- swapping and AMAT
T_M, T_D = 100e-9, 10e-3
add((round((T_M + 0.1 * T_D) * 1e3, 4), round((T_M + 0.001 * T_D) * 1e6, 1), round((T_M + 0.01 * T_D) * 1e6, 1)), (1.0001, 10.1, 100.1), "AMAT: 1.0001 ms, 10.1 µs, 100.1 µs")
# ---------------- page replacement, independent of the sim
def replace(refs, frames, policy):
    mem, loaded, used, ev, hits = [], {}, {}, [], 0
    for t, p in enumerate(refs):
        if p in mem: hits += 1
        else:
            if len(mem) == frames:
                if policy == "FIFO": v = min(mem, key=lambda x: loaded[x])
                elif policy == "LRU": v = min(mem, key=lambda x: used[x])
                else:
                    nxt = lambda x: refs.index(x, t + 1) if x in refs[t + 1:] else float("inf")
                    v = max(mem, key=lambda x: (nxt(x), -mem.index(x)))
                mem.remove(v); ev.append(v)
            mem.append(p); loaded[p] = t
        used[p] = t
    return len(refs) - hits, hits, ev
def hit_positions(refs, frames, policy):
    return [t + 1 for t in range(len(refs)) if replace(refs[:t + 1], frames, policy)[1] > replace(refs[:t], frames, policy)[1]]
OS = [0, 1, 2, 0, 1, 3, 0, 3, 1, 2, 1]
add((replace(OS, 3, "OPT")[:2], round(6 / 11 * 100, 1), round(6 / 7 * 100, 1)), ((5, 6), 54.5, 85.7), "OPT: 6 hits, 5 misses, 54.5 % (85.7 % without the 3 compulsory misses)")
add((replace(OS, 3, "FIFO")[1], round(4 / 11 * 100, 1), replace(OS, 3, "LRU")[1]), (4, 36.4, 6), "FIFO 36.4 %, LRU 6 hits")
nxt = lambda refs, x, t: refs.index(x, t + 1) + 1
add((nxt(OS, 0, 5), nxt(OS, 1, 5), nxt(OS, 2, 5)), (7, 9, 10), "OPT demo card: at the 6th reference 0 is next used at 7, 1 at 9, 2 at 10")
EXR = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
BEL = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
add(replace(EXR, 3, "FIFO"), (10, 3, [7, 0, 1, 2, 3, 0, 4]), "the skill tree's exercise 4 under FIFO: 10 faults, evicting 7 0 1 2 3 0 4")
add(replace(EXR, 3, "LRU"), (9, 4, [7, 1, 2, 3, 0, 4]), "…under LRU: 9 faults, evicting 7 1 2 3 0 4")
add(hit_positions(EXR, 3, "FIFO"), [5, 12, 13], "fifo-count: hits at references 5, 12, 13")
add((replace(BEL, 3, "FIFO")[0], replace(BEL, 4, "FIFO")[0], replace(BEL, 4, "FIFO")[2]), (9, 10, [1, 2, 3, 4, 5, 1]), "Belady's anomaly: 9 vs 10")
add(replace(BEL, 3, "OPT")[0], 7, "opt-sim: 7 faults")
add(replace(BEL, 3, "LRU")[0], 10, "lru-boss: 10")
add(hit_positions(BEL, 3, "LRU"), [8, 9], "lru-boss: only the 8th and 9th references hit")
# ---------------- file system layout and access paths
add((5 * 4096 // 256, 5 * 4096 // 128, 64 - 8), (80, 160, 56), "vsfs: 80 inodes (160 with 128-byte inodes), 56 data blocks")
add((32 * 256, 12 * 1024 + 32 * 256, (12 * 1024 + 32 * 256) // 512), (8192, 20480, 40), "inode 32 at 20 KB, sector 40")
add(12 * 1024 + 50 * 256, 25088, "inode-50")
add(((12 + 1024) * 4, (12 + 4096 // 8) * 4, (12 + 1024 + 1024 ** 2) * 4 * 1024 > 4 * 2 ** 30), (4144, 2096, True), "4144 KB; with 8-byte addresses 2096 KB; double indirect > 4 GB")
add(100 // 4 + (1 if 100 // 4 > 12 else 0), 26, "blocks-100k: 25 data blocks + 1 indirect")
add((2 * 2 + 1, 2 * 4 + 1, 5 + 3 * 3, 3 * 5, 2 * 3 + 1), (5, 9, 14, 15, 7), "open /foo/bar 5, /a/b/c/file 9, open + 3 reads 14, 3 allocating writes 15, /usr/lib/x.so 7")
add((2 ** 19 * 4 // 2 ** 20, hex(0x12345678 >> 12)), (2, "0x12345"), "pt-boss 2 MB, vpn-boss 0x12345")

bad = [(w, g, e) for g, e, w in checks if g != e]
for w, g, e in bad:
    print(f"MISMATCH {w}: got {g!r}, want {e!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
sys.exit(1 if bad else 0)
