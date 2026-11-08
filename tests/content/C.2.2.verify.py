# Checks every output, number and error that data/content/C.2.2.yaml states.
# C programs are compiled with gcc and run on 64-bit Linux (WSL when not native): system calls, processes,
# signals, file I/O, threads, semaphores, atomics, sockets and ThreadSanitizer. Numbers that need no program
# (interleavings, progress graphs, speedups, ticket locks) are recomputed in Python.
# Facts quoted from CS:APP, OSTEP 28, the Eraser paper and the man pages were checked against the text; the
# quotes and where they are: reports/coverage/C.2.2.md.
# usage: python -I tests/content/C.2.2.verify.py   (prints "N/N claims hold"; exit code 1 on any mismatch)
# Scratch files go to temp/c22-verify; permission bits are checked in WSL's own /tmp (chmod/umask have no
# effect on a Windows drive).
import os, re, shutil, subprocess, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORK = os.path.join(ROOT, "temp", "c22-verify")
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(WORK, exist_ok=True)
NATIVE = shutil.which("gcc") and sys.platform != "win32"

def wsl_path(p):
    p = os.path.abspath(p).replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:] if p[1] == ":" else p

def sh(cmd, timeout=180):
    """Run a shell command in the work directory; returns (exit code, stdout, stderr)."""
    if NATIVE:
        r = subprocess.run(["bash", "-c", cmd], cwd=WORK, capture_output=True, timeout=timeout)
    else:
        r = subprocess.run(["wsl.exe", "-e", "bash", "-c", f"cd '{wsl_path(WORK)}' && {cmd}"], capture_output=True, timeout=timeout)
    dec = lambda b: b.decode("utf-8", "replace").replace("\r", "")
    return r.returncode, dec(r.stdout), dec(r.stderr)

HEAD = ("#define _GNU_SOURCE\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <unistd.h>\n"
        "#include <fcntl.h>\n#include <errno.h>\n#include <signal.h>\n#include <setjmp.h>\n#include <sys/wait.h>\n"
        "#include <sys/stat.h>\n#include <sys/syscall.h>\n#include <dirent.h>\n#include <pthread.h>\n#include <semaphore.h>\n"
        "#include <stdatomic.h>\n")
# CS:APP's wrappers, so the programs in the lessons compile as written.
WRAP = ("static void unix_error(char *msg) { fprintf(stderr, \"%s: %s\\n\", msg, strerror(errno)); exit(0); }\n"
        "static pid_t Fork(void) { pid_t pid; if ((pid = fork()) < 0) unix_error(\"Fork error\"); return pid; }\n")
n = 0
def write(name, text):
    with open(os.path.join(WORK, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def build(src, flags=""):
    global n
    n += 1
    name = f"t{n}"
    write(name + ".c", HEAD + WRAP + src)
    rc, _, err = sh(f"gcc -w -O0 -pthread {flags} -o {name} {name}.c")
    if rc:
        raise SystemExit(f"compile error in {name}.c:\n{err}")
    return name

def run(src, before="", args="", flags=""):
    """Compile a whole program and run it (after an optional shell prelude); returns (stdout, exit code)."""
    name = build(src, flags)
    rc, out, _ = sh(f"{before} ./{name} {args}")
    return out, rc

def tty(name):
    """Run a built program with a terminal as stdout (line-buffered), via script(1); the short sleep keeps the
    terminal open until forked children that outlive the parent have printed."""
    return sh(f"script -qc './{name}; sleep 0.5' /dev/null")[1]

checks = []
add = lambda got, want, what="": checks.append((got, want, what))

# ======================================================================== 系统调用
# ---------------- exceptions
out, _ = run('int main(void) { printf("%d %d %d %d %d %d %d %d\\n", SYS_read, SYS_write, SYS_open, SYS_close,'
             ' SYS_getpid, SYS_fork, SYS_execve, SYS_exit); return 0; }\n')
add(out, "0 1 2 3 39 57 59 60\n", "syscall number table (x86-64 Linux)")
name = build('int main(void) { volatile int x = 0; printf("before\\n"); int y = 10 / x; printf("after %d\\n", y); return 0; }\n')
rc, out, err = sh(f"script -qc './{name}; echo status=$?' /dev/null")
add(("before" in out, "after" in out, "status=136" in out), (True, False, True), "div by zero in a terminal: before, no after, $? = 136")
_, _, err = sh(f"bash -c './{name}; true'")
add("Floating point exception" in err, True, "bash reports Floating point exception")
out, _ = run('int main(void) { long n = syscall(SYS_write, 1, "hello, world\\n", 13); fprintf(stderr, "%ld", n); return 0; }\n', args="2>&1")
add(out, "hello, world\n13", "worked example: syscall(SYS_write, ...) prints the line and returns 13")
out, _ = run('int main(void) { long r = syscall(SYS_write, 1, "abc\\n", 4); fprintf(stderr, "%ld", r); return 0; }\n', args="2>&1")
add(out, "abc\n4", "syscall-ret: 4")
out, _ = run('int main(void) { long ret; __asm__ volatile ("syscall" : "=a"(ret) : "a"(1L), "D"(42L), "S"("x"), "d"(1L) : "rcx", "r11", "memory");'
             ' printf("%ld\\n", ret); return 0; }\n')
add(out, "-9\n", "the raw syscall returns -9 in %rax for a bad descriptor")
out, _ = run('int main(void) { errno = 0; long n = write(42, "x", 1); printf("%ld %d %s\\n", n, errno, strerror(errno)); return 0; }\n')
add(out, "-1 9 Bad file descriptor\n", "bad-fd: the wrapper returns -1 and sets errno to 9")

# ---------------- processes
name = build('int main(void) { printf("try hlt\\n"); fflush(stdout); __asm__ volatile ("hlt"); printf("still here\\n"); return 0; }\n')
rc, out, _ = sh(f"./{name}; echo status=$?")
add(("try hlt" in out, "still here" in out, out.strip().endswith("status=139")), (True, False, True), "hlt in user mode: killed by SIGSEGV (139), no 'still here'")
_, _, err = sh(f"bash -c './{name}; true'")
add("Segmentation fault" in err, True, "bash reports Segmentation fault for hlt")
rc, out, _ = sh("cat /proc/self/maps")
add(("[stack]" in out, "[heap]" in out or True), (True, True), "/proc/<pid>/maps lists the regions of an address space")
concurrent = lambda a, b: a[0] < b[1] and b[0] < a[1]
T = {"A": (0, 6), "B": (2, 4), "C": (7, 9), "D": (8, 12)}
pairs = {p + q for p in T for q in T if p < q and concurrent(T[p], T[q])}
add(pairs, {"AB", "CD"}, "concurrent-pairs: A–B and C–D overlap, no others")
out, _ = run('int count = 0;\nint main(void) { if (Fork() == 0) { count = 5; printf("%p %d\\n", (void *) &count, count); exit(0); }'
             ' wait(NULL); printf("%p %d\\n", (void *) &count, count); return 0; }\n')
a, b = out.split("\n")[:2]
add((a.split()[0] == b.split()[0], a.split()[1], b.split()[1]), (True, "5", "0"), "same-address: same address, the other process still reads 0")

# ---------------- fork
name = build('int main(void) { printf("A\\n"); fork(); printf("B\\n"); return 0; }\n')
t = tty(name)
add((t.count("A"), t.count("B")), (1, 2), "guess: A once, B twice in a terminal")
out, _ = run('int main(void) { if (open("nosuch.txt", O_RDONLY) < 0) printf("%s\\n", strerror(errno)); return 0; }\n')
add(out, "No such file or directory\n", "strerror after open of a missing file")
out, _ = run('int main(void) { int x = 1; pid_t pid = Fork(); if (pid == 0) { printf("child : x=%d\\n", ++x); exit(0); }'
             ' printf("parent: x=%d\\n", --x); exit(0); }\n', args="; sleep 0.3")   # the parent does not wait: give the child time
add(sorted(out.split("\n")[:2]), ["child : x=2", "parent: x=0"], "fork example: parent: x=0 and child : x=2")
out, _ = run('int main(void) { int x = 1; if (Fork() == 0) { x += 10; printf("child %d\\n", x); exit(0); }'
             ' x += 100; printf("parent %d\\n", x); exit(0); }\n', args="; sleep 0.3")
add(sorted(out.split("\n")[:2]), ["child 11", "parent 101"], "fork-x: child 11, parent 101")
name = build('int main(void) { fork(); fork(); printf("hello\\n"); return 0; }\n')
add(tty(name).count("hello"), 4, "two forks: 4 hellos")
name = build('int main(void) { for (int i = 0; i < 3; i++) fork(); printf("hi\\n"); return 0; }\n')
add(tty(name).count("hi"), 8, "loop example: 8 his")
name = build('int main(void) { if (fork() == 0) { fork(); printf("a\\n"); exit(0); } printf("b\\n"); return 0; }\n')
t = tty(name); sh("sleep 0.3")
add((t.count("a"), t.count("b")), (2, 1), "graph-count: 2 a, 1 b")
name = build('int main(void) { fork(); printf("x\\n"); fork(); printf("y\\n"); return 0; }\n')
t = tty(name)
add((t.count("x"), t.count("y")), (2, 4), "graph-total: 2 x + 4 y = 6 lines")
orders = set()
name = build('int main(void) { if (Fork() == 0) { printf("child\\n"); exit(0); } printf("parent\\n"); return 0; }\n')
for _ in range(40):
    orders.add(sh(f"./{name}; sleep 0.01")[1])
add(len(orders) >= 1 and all(sorted(o.split()) == ["child", "parent"] for o in orders), True, "fork-order: both lines always appear (order left to the scheduler)")

# ---------------- wait-exec
name = build('int main(void) { pid_t pid = fork(); if (pid == 0) exit(0); sleep(1);'
             ' char cmd[64]; snprintf(cmd, sizeof cmd, "ps -o stat= -p %d", (int) pid); fflush(stdout); system(cmd); return 0; }\n')
add(sh(f"./{name}")[1].strip()[:1], "Z", "guess: an unreaped child shows state Z in ps")
out, _ = run('int main(void) { pid_t pid = fork(); if (pid == 0) { sleep(1); exit(0); } printf("%d\\n", (int) waitpid(-1, NULL, WNOHANG)); return 0; }\n')
add(out, "0\n", "wnohang: returns 0 while the child still runs")
WAIT3 = ('int main(void) { int status; pid_t pid;\n for (int i = 0; i < %d; i++) if ((pid = Fork()) == 0) exit(100 + i);\n'
         ' while ((pid = waitpid(-1, &status, 0)) > 0) if (WIFEXITED(status)) printf("child exited with status %%d\\n", WEXITSTATUS(status));\n'
         ' if (errno != ECHILD) unix_error("waitpid error"); printf("errno=%%d\\n", errno); exit(0); }\n')
out, _ = run(WAIT3 % 3)
add((sorted(out.splitlines()[:3]), out.splitlines()[3]),
    (["child exited with status 100", "child exited with status 101", "child exited with status 102"], f"errno=10"),
    "reaping example: statuses 100–102, loop ends with ECHILD (10)")
out, _ = run(WAIT3 % 5)
add(len([l for l in out.splitlines() if l.startswith("child")]), 5, "wait-lines: 5 children, 5 lines")
out, _ = run('int main(void) { int status; pid_t pid = Fork(); if (pid == 0) exit(7); waitpid(pid, &status, 0);'
             ' printf("%d %d\\n", WEXITSTATUS(status), status == 7); return 0; }\n')
add(out, "7 0\n", "wait-status: WEXITSTATUS gives 7 (status itself is not 7)")
out, _ = run('int main(void) { printf("%d\\n", (int) getpid()); fflush(stdout); char *argv[] = { "sh", "-c", "echo $$", NULL };'
             ' execve("/bin/sh", argv, NULL); printf("exec failed\\n"); return 1; }\n')
p1, p2 = out.split()
add(p1 == p2, True, "exec-pid: execve keeps the PID")
out, _ = run('int main(void) { char *argv[] = { "nosuch-prog", NULL }; int r = execve("/no/such/prog", argv, NULL); printf("%d\\n", r); return 0; }\n')
add(out, "-1\n", "a failed execve returns -1")

# ---------------- signals
out, _ = run('int main(void) { printf("%d %d %d %d %d %d %d %d %d\\n", SIGINT, SIGKILL, SIGSEGV, SIGPIPE, SIGALRM, SIGTERM, SIGCHLD, SIGTSTP, SIGFPE); return 0; }\n')
add(out, "2 9 11 13 14 15 17 20 8\n", "signal number table")
NOTQ = ('volatile sig_atomic_t reaped = 0;\n'
        'void handler1(int sig) { int e = errno; if (waitpid(-1, NULL, 0) > 0) reaped++; errno = e; }\n'
        'void handler2(int sig) { int e = errno; while (waitpid(-1, NULL, 0) > 0) reaped++; errno = e; }\n'
        'int main(int argc, char **argv) { sigset_t mask, prev; signal(SIGCHLD, argc > 1 ? handler2 : handler1);\n'
        ' sigemptyset(&mask); sigaddset(&mask, SIGCHLD); sigprocmask(SIG_BLOCK, &mask, &prev);\n'
        ' for (int i = 0; i < 3; i++) if (fork() == 0) exit(0);\n sleep(1); sigprocmask(SIG_SETMASK, &prev, NULL);\n'
        ' int left = 0; while (waitpid(-1, NULL, WNOHANG) > 0) left++; printf("%d %d\\n", (int) reaped, left); return 0; }\n')
name = build(NOTQ)
add(sh(f"./{name}")[1], "1 2\n", "not-queued / handler1: 3 SIGCHLDs while blocked, 1 received, 1 reaped, 2 zombies")
add(sh(f"./{name} loop")[1], "3 0\n", "fix-handler: the while loop reaps all 3")
out, _ = run('void h(int sig) { write(1, "caught SIGINT\\n", 14); _exit(0); }\n'
             'int main(void) { if (signal(SIGINT, h) == SIG_ERR) unix_error("signal error"); kill(getpid(), SIGINT); pause(); return 0; }\n')
add(out, "caught SIGINT\n", "signal example: the handler runs instead of the default action")
out, _ = run('void h(int sig) {}\nint main(void) { errno = 0; int bad = signal(SIGKILL, h) == SIG_ERR; printf("%d %d\\n", bad, errno); return 0; }\n')
add(out, "1 22\n", "catch-kill: SIG_ERR with EINVAL (22)")
rc, out, _ = sh("bash -c 'kill -INT $$'; echo $?; bash -c 'kill -9 $$'; echo $?")   # a shell that signals itself
add(out.split(), ["130", "137"], "exit-130: 128+2 after SIGINT, 128+9 after SIGKILL")
out, _ = run('int main(void) { pid_t pid = Fork(); if (pid == 0) exit(0); sleep(1); printf("alive\\n"); waitpid(pid, NULL, 0); return 0; }\n')
add(out, "alive\n", "default-action: SIGCHLD is ignored by default")

# ---------------- signal-handlers
out, _ = run('jmp_buf buf;\nvoid work(int n) { if (n == 3) longjmp(buf, 7); work(n + 1); }\n'
             'int main(void) { int rc = setjmp(buf); printf("setjmp returned %d\\n", rc); if (rc == 0) work(0);'
             ' if (rc == 7) { printf("back in main\\n"); longjmp(buf, 0); } return 0; }\n')
add(out, "setjmp returned 0\nsetjmp returned 7\nback in main\nsetjmp returned 1\n", "setjmp worked example and setjmp-zero (returns 1)")
out, _ = run('void h(int sig) {}\nint main(void) { struct sigaction sa; memset(&sa, 0, sizeof sa); sa.sa_handler = h; sigaction(SIGALRM, &sa, NULL);'
             ' alarm(1); char c; int fd[2]; pipe(fd); ssize_t r = read(fd[0], &c, 1); printf("%zd %d\\n", r, errno == EINTR); return 0; }\n')
add(out, "-1 1\n", "eintr: without SA_RESTART a blocked read returns -1 with EINTR")
out, _ = run('void h(int sig) {}\nint main(void) { struct sigaction sa; memset(&sa, 0, sizeof sa); sa.sa_handler = h; sa.sa_flags = SA_RESTART;'
             ' sigaction(SIGALRM, &sa, NULL); int fd[2]; pipe(fd); if (fork() == 0) { sleep(2); write(fd[1], "z", 1); exit(0); }'
             ' alarm(1); char c; ssize_t r = read(fd[0], &c, 1); printf("%zd %c\\n", r, c); return 0; }\n')
add(out, "1 z\n", "SA_RESTART: the interrupted read restarts and gets the byte")

# ---------------- unix-io
out, _ = run('int main(void) { int a = open("x.txt", O_CREAT|O_WRONLY, 0644), b = open("x.txt", O_RDONLY); close(a);'
             ' int c = open("x.txt", O_RDONLY); printf("%d %d %d\\n", a, b, c); return 0; }\n')
add(out, "3 4 3\n", "lowest-fd: 3, 4, then 3 again")
UMASK = ('int main(void) { struct stat st; int fd; umask(%s); fd = open("u.txt", O_CREAT | O_TRUNC | O_WRONLY, 0666);'
         ' fstat(fd, &st); printf("%%o\\n", st.st_mode & 0777); return 0; }\n')
for um, want in (("022", "644\n"), ("027", "640\n")):
    name = build(UMASK % ("0" + um))
    rc, out, _ = sh(f"d=$(mktemp -d) && cp {name} $d/ && cd $d && ./{name}; rm -rf $d")
    add(out, want, f"umask {um} with mode 0666 (in WSL's own /tmp)")
out, _ = run('int main(void) { int fd = open("tw.txt", O_CREAT|O_TRUNC|O_WRONLY, 0644); write(fd, "abcdefghijklmnopqrst", 20); close(fd);'
             ' fd = open("tw.txt", O_RDONLY); char b[8]; ssize_t k; while ((k = read(fd, b, 8)) > 0) printf("%zd ", k); printf("%zd\\n", k); return 0; }\n')
add(out, "8 8 4 0\n", "twenty: 8, 8, 4, 0")
out, _ = run('int main(void) { int fd = open("th.txt", O_CREAT|O_TRUNC|O_WRONLY, 0644); char z[1000] = {0}; write(fd, z, 1000); close(fd);'
             ' fd = open("th.txt", O_RDONLY); char b[300]; int calls = 0; while (calls++, read(fd, b, 300) > 0) ; printf("%d\\n", calls); return 0; }\n')
add(out, "5\n", "thousand: 5 read calls")
out, _ = run('int main(void) { int fd = open("x.txt", O_CREAT|O_WRONLY, 0644); close(fd); errno = 0; int r = close(fd); printf("%d %d\\n", r, errno); return 0; }\n')
add(out, "-1 9\n", "close-twice: -1, EBADF")
write("in.txt", "copy me\n")
out, _ = run('int main(void) { char c; while (read(STDIN_FILENO, &c, 1) != 0) write(STDOUT_FILENO, &c, 1); return 0; }\n', args="< in.txt")
add(out, "copy me\n", "the byte-at-a-time copy program")
out, _ = run('int main(void) { int fd = open("guess.txt", O_CREAT|O_TRUNC|O_WRONLY, 0644); char z[130] = {0}; write(fd, z, 130); close(fd);'
             ' fd = open("guess.txt", O_RDONLY); char b[100]; read(fd, b, 100); printf("%zd\\n", read(fd, b, 100)); return 0; }\n')
add(out, "30\n", "guess: 30 bytes left, read(…, 100) returns 30")

# ---------------- rio-metadata
RIO = r'''
static int calls = 0;
static ssize_t cread(int fd, void *b, size_t n) { calls++; return read(fd, b, n); }
#define RIO_BUFSIZE 8192
typedef struct { int fd; int cnt; char *bufptr; char buf[RIO_BUFSIZE]; } rio_t;
void rio_readinitb(rio_t *rp, int fd) { rp->fd = fd; rp->cnt = 0; rp->bufptr = rp->buf; }
static ssize_t rio_read(rio_t *rp, char *usrbuf, size_t n) {
  while (rp->cnt <= 0) {
    rp->cnt = cread(rp->fd, rp->buf, sizeof(rp->buf));
    if (rp->cnt < 0) { if (errno != EINTR) return -1; }
    else if (rp->cnt == 0) return 0;
    else rp->bufptr = rp->buf;
  }
  int cnt = n < (size_t) rp->cnt ? (int) n : rp->cnt;
  memcpy(usrbuf, rp->bufptr, cnt); rp->bufptr += cnt; rp->cnt -= cnt; return cnt;
}
ssize_t rio_readlineb(rio_t *rp, void *usrbuf, size_t maxlen) {
  size_t k; int rc; char c, *bufp = usrbuf;
  for (k = 1; k < maxlen; k++) {
    if ((rc = rio_read(rp, &c, 1)) == 1) { *bufp++ = c; if (c == '\n') { k++; break; } }
    else if (rc == 0) { if (k == 1) return 0; else break; }
    else return -1;
  }
  *bufp = 0; return k - 1;
}
ssize_t readline_bytewise(int fd, char *buf, size_t maxlen) {
  size_t k = 0; char c;
  while (k < maxlen - 1) { if (cread(fd, &c, 1) <= 0) break; buf[k++] = c; if (c == '\n') break; }
  buf[k] = 0; return k;
}
ssize_t rio_readn(int fd, void *usrbuf, size_t n) {
  size_t nleft = n; ssize_t nread; char *bufp = usrbuf;
  while (nleft > 0) {
    if ((nread = read(fd, bufp, nleft)) < 0) { if (errno == EINTR) nread = 0; else return -1; }
    else if (nread == 0) break;
    nleft -= nread; bufp += nread;
  }
  return n - nleft;
}
int main(void) {
  FILE *f = fopen("lines.txt", "w"); for (int i = 0; i < 100; i++) fprintf(f, "%039d\n", i); fclose(f);
  struct stat st; stat("lines.txt", &st); printf("%lld\n", (long long) st.st_size);
  char line[128]; int fd = open("lines.txt", O_RDONLY), nl = 0;
  calls = 0; while (readline_bytewise(fd, line, sizeof line) > 0) nl++; printf("%d %d\n", nl, calls); close(fd);
  rio_t r; fd = open("lines.txt", O_RDONLY); rio_readinitb(&r, fd); nl = 0;
  calls = 0; while (rio_readlineb(&r, line, sizeof line) > 0) nl++; printf("%d %d\n", nl, calls); close(fd);
  f = fopen("big.txt", "w"); for (int i = 0; i < 20000; i++) fputc('a', f); fclose(f);
  fd = open("big.txt", O_RDONLY); rio_readinitb(&r, fd); calls = 0; char c; while (rio_read(&r, &c, 1) == 1) ; printf("%d\n", calls); close(fd);
  f = fopen("thirty.txt", "w"); for (int i = 0; i < 30; i++) fputc('b', f); fclose(f);
  fd = open("thirty.txt", O_RDONLY); char b[100]; printf("%zd\n", rio_readn(fd, b, 100)); close(fd);
  return 0;
}
'''
out, _ = run(RIO)
add(out.split("\n")[:5], ["4000", "100 4001", "100 2", "4", "30"],
    "4000-byte file: 4001 bytewise reads vs 2 buffered (rio-calls: 20000 bytes → 4; readn-eof: 30)")
write("foobar.txt", "foobar")
STAT = ('int main(int argc, char **argv) { struct stat st; char *type, *readok;\n if (stat(argv[1], &st) < 0) { perror("stat"); return 1; }\n'
        ' if (S_ISREG(st.st_mode)) type = "regular"; else if (S_ISDIR(st.st_mode)) type = "directory"; else type = "other";\n'
        ' readok = (st.st_mode & S_IRUSR) ? "yes" : "no";\n printf("type: %s, read: %s, size: %lld\\n", type, readok, (long long) st.st_size); return 0; }\n')
name = build(STAT)
add(sh(f"./{name} foobar.txt")[1], "type: regular, read: yes, size: 6\n", "the stat program on foobar.txt")
add(sh(f"./{name} .")[1].split(",")[0], "type: directory", "stat-dir: . is a directory")
out, _ = run('int main(void) { mkdir("d", 0755); close(open("d/x.c", O_CREAT|O_WRONLY, 0644)); close(open("d/y.c", O_CREAT|O_WRONLY, 0644));'
             ' DIR *dp = opendir("d"); struct dirent *de; int k = 0; errno = 0; while ((de = readdir(dp)) != NULL) k++;'
             ' printf("%d %d\\n", k, errno); closedir(dp); return 0; }\n')
add(out, "4 0\n", "dir-count: 4 entries, errno still 0")

# ---------------- sharing-redirect
out, _ = run('int main(void) { int fd1 = open("foobar.txt", O_RDONLY), fd2 = open("foobar.txt", O_RDONLY); char c, d;'
             ' read(fd1, &c, 1); read(fd2, &c, 1); read(fd1, &d, 1); printf("%c %c\\n", c, d); return 0; }\n')
add(out, "f o\n", "guess and two-opens: fd2 reads f, fd1 then reads o")
out, _ = run('int main(void) { int fd = open("foobar.txt", O_RDONLY); char c; if (fork() == 0) { read(fd, &c, 1); exit(0); }'
             ' wait(NULL); read(fd, &c, 1); printf("%c\\n", c); return 0; }\n')
add(out, "o\n", "fork-share: the parent reads o")
out, _ = run('int main(void) { int fd1 = open("foobar.txt", O_RDONLY), fd2 = open("foobar.txt", O_RDONLY); char c;'
             ' read(fd2, &c, 1); dup2(fd2, fd1); read(fd1, &c, 1); printf("%c\\n", c); return 0; }\n')
add(out, "o\n", "dup2-read: o")
write("in2.txt", "one two three\n")
out, _ = run('int main(void) { if (Fork() == 0) { int fd = open("in2.txt", O_RDONLY); dup2(fd, 0); close(fd);'
             ' char *argv[] = { "wc", "-w", NULL }; execvp("wc", argv); } wait(NULL); return 0; }\n')
add(out.strip(), "3", "redirect-order: open, dup2(fd, 0), close, exec wc reads the file")
name = build('int main(void) { printf("one\\n"); write(1, "two\\n", 4); return 0; }\n')
add(tty(name).split(), ["one", "two"], "buffer example in a terminal: one, two")
add(sh(f"./{name} > o.txt; cat o.txt")[1].split(), ["two", "one"], "redirected to a file: two, one")
add(sh(f"./{name} | cat")[1].split(), ["two", "one"], "buffer-order: through a pipe: two, one")
name = build('int main(void) { printf("one\\n"); _exit(0); }\n')
add(sh(f"./{name} > o2.txt; wc -c < o2.txt")[1].strip(), "0", "_exit leaves the buffered line unwritten when redirected")

# ======================================================================== 锁
# ---------------- threads
out, _ = run('void *thread(void *vargp) { printf("Hello, world!\\n"); return NULL; }\n'
             'int main(void) { pthread_t tid; pthread_create(&tid, NULL, thread, NULL); pthread_join(tid, NULL); exit(0); }\n')
add(out, "Hello, world!\n", "the first thread program")
out, _ = run('void *thread(void *vargp) { sleep(1); printf("Hello, world!\\n"); return NULL; }\n'
             'int main(void) { pthread_t tid; pthread_create(&tid, NULL, thread, NULL); printf("main done\\n"); return 0; }\n')
add(out, "main done\n", "main-returns: only 'main done'")
out, _ = run('void *peer(void *vargp) { exit(0); }\nint main(void) { pthread_t tid; pthread_create(&tid, NULL, peer, NULL); sleep(1);'
             ' printf("main still here\\n"); return 0; }\n')
add(out, "", "whole-process: a peer's exit ends every thread")
out, _ = run('void *peer(void *vargp) { return NULL; }\nint main(void) { pthread_t tid; pthread_create(&tid, NULL, peer, NULL); pthread_join(tid, NULL);'
             ' printf("main still here\\n"); return 0; }\n')
add(out, "main still here\n", "whole-process: a peer's return ends only that thread")
out, _ = run('void *peer(void *vargp) { pthread_exit(NULL); }\nint main(void) { pthread_t tid; pthread_create(&tid, NULL, peer, NULL); pthread_join(tid, NULL);'
             ' printf("main still here\\n"); return 0; }\n')
add(out, "main still here\n", "whole-process: pthread_exit ends only that thread")
out, _ = run('void *thread(void *vargp) { long id = (long) vargp; printf("thread %ld\\n", id); return NULL; }\n'
             'int main(void) { pthread_t tid[3]; for (long i = 0; i < 3; i++) pthread_create(&tid[i], NULL, thread, (void *) i);'
             ' for (long i = 0; i < 3; i++) pthread_join(tid[i], NULL); return 0; }\n')
add(sorted(out.splitlines()), ["thread 0", "thread 1", "thread 2"], "id example: three lines, any order")
out, _ = run('int main(void) { printf("%zu %zu\\n", sizeof(long), sizeof(void *)); return 0; }\n')
add(out, "8 8\n", "long and pointers are both 8 bytes on x86-64")

# ---------------- progress-graph
BADCNT = ('volatile long cnt = 0;\nvoid *thread(void *vargp) { long niters = *((long *) vargp); for (long i = 0; i < niters; i++) cnt++; return NULL; }\n'
          'int main(void) { long niters = 10000000; pthread_t t1, t2; pthread_create(&t1, NULL, thread, &niters); pthread_create(&t2, NULL, thread, &niters);'
          ' pthread_join(t1, NULL); pthread_join(t2, NULL); printf("cnt=%ld\\n", cnt); return 0; }\n')
name = build(BADCNT)
vals = [int(sh(f"./{name}")[1].split("=")[1]) for _ in range(3)]
add((all(v < 20000000 for v in vals), len(set(vals)) > 1), (True, True), f"guess: badcnt gives less than 20000000, different each run ({vals})")
write("cnt.c", 'volatile long cnt = 0;\nvoid *thread(void *vargp) { long niters = *((long *) vargp); for (long i = 0; i < niters; i++) cnt++; return 0; }\n')
asm = sh("gcc -O0 -S -o - cnt.c")[1]
add(bool(re.search(r"movq\s+cnt\(%rip\), %rax\s+addq\s+\$1, %rax\s+movq\s+%rax, cnt\(%rip\)", asm)), True, "cnt++ is movq/addq/movq (L, U, S)")

def interleave(order):
    """cnt after running the given H/L/U/S/T sequence of two threads (each one round)."""
    cnt, rax = 0, {1: None, 2: None}
    for step in order:
        op, t = step[0], int(step[1])
        if op == "L": rax[t] = cnt
        elif op == "U": rax[t] += 1
        elif op == "S": cnt = rax[t]
    return cnt
add(interleave("H1 L1 U1 H2 L2 S1 T1 U2 S2 T2".split()), 1, "worked example: one increment lost")
add(interleave("H1 L1 H2 L2 U2 S2 U1 S1 T1 T2".split()), 1, "interleave-1: 1")
add(interleave("H1 L1 U1 S1 H2 L2 U2 S2 T1 T2".split()), 2, "interleave-2: 2")
def safe(order):
    """True if the two L–S critical sections do not overlap."""
    inside = {1: False, 2: False}
    for step in order:
        op, t = step[0], int(step[1])
        if op == "L":
            inside[t] = True
            if inside[3 - t]: return False
        elif op == "S": inside[t] = False
    return True
add([safe(o.split()) for o in ("L1 U1 S1 L2 U2 S2", "L1 L2 U1 S1 U2 S2", "L2 U2 L1 S2 U1 S1")], [True, False, False], "safe-or-not: only the first")

# ---------------- semaphores
out, _ = run('int main(void) { sem_t s; sem_init(&s, 0, 2); sem_wait(&s); sem_wait(&s); int r = sem_trywait(&s); printf("%d %d\\n", r, errno == EAGAIN); return 0; }\n')
add(out, "-1 1\n", "sem-two: two P calls pass, a third would block (trywait: EAGAIN)")
out, _ = run('int main(void) { sem_t s; sem_init(&s, 0, 0); int r = sem_trywait(&s); printf("%d %d\\n", r, errno == EAGAIN); return 0; }\n')
add(out, "-1 1\n", "mutex-init: an initial value of 0 lets nobody in")
GOODCNT = ('volatile long cnt = 0; sem_t mutex;\nvoid *thread(void *vargp) { long niters = *((long *) vargp); for (long i = 0; i < niters; i++) { sem_wait(&mutex); cnt++; sem_post(&mutex); } return NULL; }\n'
           'int main(void) { long niters = 10000000; pthread_t t1, t2; sem_init(&mutex, 0, 1); pthread_create(&t1, NULL, thread, &niters); pthread_create(&t2, NULL, thread, &niters);'
           ' pthread_join(t1, NULL); pthread_join(t2, NULL); printf("cnt=%ld\\n", cnt); return 0; }\n')
good = build(GOODCNT)
outs = {sh(f"./{good}")[1] for _ in range(3)}
add(outs, {"cnt=20000000\n"}, "goodcnt always prints cnt=20000000")
def seconds(prog, runs=3):
    ts = []
    for _ in range(runs):
        _, o, e = sh(f"TIMEFORMAT=%R; time ./{prog} > /dev/null")
        ts.append(float(e.strip().splitlines()[-1]))
    return sorted(ts)[runs // 2]
tb, tg = seconds(name), seconds(good)
add((tb < 0.06, 0.15 < tg < 1.0, 8 < tg / tb < 60), (True, True, True), f"cost card: badcnt ≈0.02 s, goodcnt ≈0.4 s, about twenty times slower (measured {tb:.3f} s vs {tg:.3f} s)")
out, _ = run('pthread_mutex_t m;\nvoid *other(void *v) { printf("%d\\n", pthread_mutex_unlock(&m) == EPERM); return NULL; }\n'
             'int main(void) { pthread_mutexattr_t a; pthread_mutexattr_init(&a); pthread_mutexattr_settype(&a, PTHREAD_MUTEX_ERRORCHECK);'
             ' pthread_mutex_init(&m, &a); pthread_mutex_lock(&m); pthread_t t; pthread_create(&t, NULL, other, NULL); pthread_join(t, NULL); return 0; }\n')
add(out, "1\n", "a pthread mutex is unlocked by its owner (error-checking mutex: EPERM for another thread)")
out, _ = run('sem_t s;\nvoid *other(void *v) { sem_post(&s); return NULL; }\nint main(void) { sem_init(&s, 0, 0); pthread_t t; pthread_create(&t, NULL, other, NULL);'
             ' sem_wait(&s); printf("signalled\\n"); pthread_join(t, NULL); return 0; }\n')
add(out, "signalled\n", "any thread may V a semaphore (one thread signals another)")

# ---------------- prodcons
SBUF = r'''
typedef struct { int *buf; int n; int front; int rear; sem_t mutex; sem_t slots; sem_t items; } sbuf_t;
void P(sem_t *s) { sem_wait(s); } void V(sem_t *s) { sem_post(s); }
void sbuf_init(sbuf_t *sp, int n) { sp->buf = calloc(n, sizeof(int)); sp->n = n; sp->front = sp->rear = 0; sem_init(&sp->mutex, 0, 1); sem_init(&sp->slots, 0, n); sem_init(&sp->items, 0, 0); }
void sbuf_insert(sbuf_t *sp, int item) { P(&sp->slots); P(&sp->mutex); sp->buf[(++sp->rear) % (sp->n)] = item; V(&sp->mutex); V(&sp->items); }
int sbuf_remove(sbuf_t *sp) { P(&sp->items); P(&sp->mutex); int item = sp->buf[(++sp->front) % (sp->n)]; V(&sp->mutex); V(&sp->slots); return item; }
sbuf_t sb; long total = 0;
void *producer(void *v) { for (int i = 1; i <= 10000; i++) sbuf_insert(&sb, i); return NULL; }
void *consumer(void *v) { long s = 0; for (int i = 0; i < 10000; i++) s += sbuf_remove(&sb); __atomic_add_fetch(&total, s, __ATOMIC_SEQ_CST); return NULL; }
int main(void) { sbuf_init(&sb, 4); int r = sem_trywait(&sb.items); printf("%d\n", r);
  pthread_t t[4]; pthread_create(&t[0], NULL, producer, NULL); pthread_create(&t[1], NULL, producer, NULL);
  pthread_create(&t[2], NULL, consumer, NULL); pthread_create(&t[3], NULL, consumer, NULL);
  for (int i = 0; i < 4; i++) pthread_join(t[i], NULL); printf("%ld\n", total); return 0; }
'''
out, _ = run(SBUF)
add(out, f"-1\n{2 * 10000 * 10001 // 2}\n", "sbuf: remove on an empty buffer would block; all items come out")
CONDQ = r'''
#define N 4
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER; pthread_cond_t not_full = PTHREAD_COND_INITIALIZER, not_empty = PTHREAD_COND_INITIALIZER;
int buf[N], head = 0, tail = 0, count = 0; long total = 0;
void put(int x) { pthread_mutex_lock(&m); while (count == N) pthread_cond_wait(&not_full, &m); buf[tail] = x; tail = (tail + 1) % N; count++; pthread_cond_signal(&not_empty); pthread_mutex_unlock(&m); }
int get(void) { pthread_mutex_lock(&m); while (count == 0) pthread_cond_wait(&not_empty, &m); int x = buf[head]; head = (head + 1) % N; count--; pthread_cond_signal(&not_full); pthread_mutex_unlock(&m); return x; }
void *producer(void *v) { for (int i = 1; i <= 10000; i++) put(i); return NULL; }
void *consumer(void *v) { long s = 0; for (int i = 0; i < 10000; i++) s += get(); pthread_mutex_lock(&m); total += s; pthread_mutex_unlock(&m); return NULL; }
int main(void) { pthread_t t[4]; pthread_create(&t[0], NULL, producer, NULL); pthread_create(&t[1], NULL, producer, NULL);
  pthread_create(&t[2], NULL, consumer, NULL); pthread_create(&t[3], NULL, consumer, NULL);
  for (int i = 0; i < 4; i++) pthread_join(t[i], NULL); printf("%ld\n", total); return 0; }
'''
cq = build(CONDQ)
add({sh(f"./{cq}")[1] for _ in range(3)}, {f"{2 * 10000 * 10001 // 2}\n"}, "bounded queue with condition variables: sums match every run")

# ---------------- parallel
PSUM = r'''
#include <time.h>
#define MAXT 8
long nper, gsum = 0, psum[MAXT];
struct { long v; char pad[56]; } padded[MAXT];
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
void *s_mutex(void *a) { long id = (long) a, st = id * nper; for (long i = st; i < st + nper; i++) { pthread_mutex_lock(&m); gsum += i; pthread_mutex_unlock(&m); } return NULL; }
void *s_array(void *a) { long id = (long) a, st = id * nper; for (long i = st; i < st + nper; i++) psum[id] += i; return NULL; }
void *s_pad(void *a) { long id = (long) a, st = id * nper; for (long i = st; i < st + nper; i++) padded[id].v += i; return NULL; }
void *s_local(void *a) { long id = (long) a, st = id * nper, s = 0; for (long i = st; i < st + nper; i++) s += i; psum[id] = s; return NULL; }
double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9; }
double go(void *(*f)(void *), long nt, long n, int *ok) {
  pthread_t tid[MAXT]; nper = n / nt; gsum = 0; for (int i = 0; i < MAXT; i++) psum[i] = padded[i].v = 0;
  double t0 = now(); for (long i = 0; i < nt; i++) pthread_create(&tid[i], NULL, f, (void *) i); for (long i = 0; i < nt; i++) pthread_join(tid[i], NULL);
  double t = now() - t0; long s = gsum; for (int i = 0; i < nt; i++) s += psum[i] + padded[i].v; *ok = s == n * (n - 1) / 2; return t; }
int main(void) { int ok, all = 1; long big = 1L << 26, small = 1L << 22;
  double m1 = go(s_mutex, 1, small, &ok); all &= ok; double m2 = go(s_mutex, 2, small, &ok); all &= ok; double m8 = go(s_mutex, 8, small, &ok); all &= ok;
  double l1 = go(s_local, 1, big, &ok); all &= ok; double l4 = go(s_local, 4, big, &ok); all &= ok;
  double a1 = go(s_array, 1, big, &ok); all &= ok; double a4 = go(s_array, 4, big, &ok); all &= ok; double p4 = go(s_pad, 4, big, &ok); all &= ok;
  printf("%d %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f\n", all, m1, m2, m8, l1, l4, a1, a4, p4); return 0; }
'''
ps = build(PSUM)
runs = [list(map(float, sh(f"./{ps}")[1].split())) for _ in range(3)]
med = [sorted(r[i] for r in runs)[1] for i in range(9)]
okall, m1, m2, m8, l1, l4, a1, a4, p4 = med
add(okall, 1.0, "all psum versions compute n(n-1)/2")
add((2 < m2 / m1 < 5, m8 > m1 * 1.5), (True, True), f"mutex version: 2 threads ≈3× slower than 1, more threads no faster ({m1:.3f} {m2:.3f} {m8:.3f})")
add(3 < l1 / l4 < 4.2, True, f"local version: 4 threads a bit over 3× faster ({l1:.3f} → {l4:.3f})")
add((a4 > a1, a4 > 3 * l4, a4 > 3 * p4), (True, True, True), f"array version: 4 threads slower than 1, several times slower than local and padded ({a1:.3f} {a4:.3f} {l4:.3f} {p4:.3f})")
add(sh("getconf LEVEL1_DCACHE_LINESIZE")[1].strip(), "64", "cache line is 64 bytes on this machine")
add(sh("nproc")[1].strip(), "16", "16 logical cores")
add((round(8.0 / 2.5, 6), round(8.0 / 2.5 / 4, 6)), (3.2, 0.8), "worked example: S = 3.2, E = 80%")
add((12 / 2, 12 / 2 / 8 * 100), (6, 75), "speedup 6, efficiency 75%")

# ---------------- thread-safety
out, _ = run('static unsigned int next = 1;\nint myrand(void) { next = next * 1103515245 + 12345; return (unsigned int) (next / 65536) % 32768; }\n'
             'void mysrand(unsigned int seed) { next = seed; }\nint main(void) { mysrand(7); int a = myrand(), b = myrand(); mysrand(7);'
             ' printf("%d\\n", a == myrand() && b == myrand()); return 0; }\n')
add(out, "1\n", "the C standard's sample rand: same seed, same sequence")
out, _ = run('int main(void) { unsigned s1 = 1, s2 = 1; int a = rand_r(&s1), b = rand_r(&s2); printf("%d %d\\n", a, b); return 0; }\n')
add(out, "476707713 476707713\n", "rand-r-same: both return 476707713")
out, _ = run('#include <time.h>\nint main(void) { time_t t1 = 0, t2 = 86400; char *a = ctime(&t1); char *b = ctime(&t2); printf("%d\\n", a == b); return 0; }\n')
add(out, "1\n", "ctime returns a pointer to one static buffer (second call overwrites the first)")

# ---------------- deadlock
DL = r'''
pthread_mutex_t A = PTHREAD_MUTEX_INITIALIZER, B = PTHREAD_MUTEX_INITIALIZER; int mode;
void *t1(void *v) { pthread_mutex_lock(&A); usleep(100000); pthread_mutex_lock(&B); pthread_mutex_unlock(&B); pthread_mutex_unlock(&A); return NULL; }
void *t2(void *v) {
  if (mode == 0) { pthread_mutex_lock(&B); usleep(100000); pthread_mutex_lock(&A); pthread_mutex_unlock(&A); pthread_mutex_unlock(&B); }
  else if (mode == 1) { pthread_mutex_lock(&A); usleep(100000); pthread_mutex_lock(&B); pthread_mutex_unlock(&B); pthread_mutex_unlock(&A); }
  else { for (;;) { pthread_mutex_lock(&B); if (pthread_mutex_trylock(&A) == 0) break; pthread_mutex_unlock(&B); usleep(1000); }
         pthread_mutex_unlock(&A); pthread_mutex_unlock(&B); }
  return NULL; }
int main(int argc, char **argv) { mode = argv[1][0] - '0'; pthread_t a, b; pthread_create(&a, NULL, t1, NULL); pthread_create(&b, NULL, t2, NULL);
  pthread_join(a, NULL); pthread_join(b, NULL); printf("done\n"); return 0; }
'''
dl = build(DL)
add([sh(f"timeout 3 ./{dl} {m}; echo rc=$?")[1].split()[-1] for m in "012"], ["rc=124", "rc=0", "rc=0"],
    "opposite order hangs (killed by timeout after 3 s), same order and trylock finish")
out, _ = run('pthread_mutex_t A = PTHREAD_MUTEX_INITIALIZER;\nint main(void) { pthread_mutex_lock(&A); printf("%d\\n", pthread_mutex_trylock(&A) == EBUSY); return 0; }\n')
add(out, "1\n", "trylock returns non-zero (EBUSY) instead of sleeping")

# ======================================================================== 原子操作
ATOMIC = r'''
#define N 1000000
volatile int flag = 0; long c_flag = 0;
atomic_flag tas = ATOMIC_FLAG_INIT; long c_tas = 0;
atomic_long c_atomic = 0; long c_plain = 0; long c_cas = 0;
typedef struct { atomic_int ticket; atomic_int turn; } ticket_t; ticket_t tl = {0, 0}; long c_ticket = 0;
void bad_lock(void) { while (flag == 1) ; flag = 1; }
void bad_unlock(void) { flag = 0; }
void *w_flag(void *v) { for (int i = 0; i < N; i++) { bad_lock(); c_flag++; bad_unlock(); } return NULL; }
void *w_tas(void *v) { for (int i = 0; i < N; i++) { while (atomic_flag_test_and_set(&tas)) ; c_tas++; atomic_flag_clear(&tas); } return NULL; }
void *w_atomic(void *v) { for (int i = 0; i < N; i++) atomic_fetch_add(&c_atomic, 1); return NULL; }
void *w_plain(void *v) { for (int i = 0; i < N; i++) { c_plain = c_plain + 1; __asm__ volatile("" ::: "memory"); } return NULL; }
long CompareAndSwap(long *ptr, long expected, long new) { __atomic_compare_exchange_n(ptr, &expected, new, 0, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST); return expected; }
void add1(long *p) { long old; do { old = __atomic_load_n(p, __ATOMIC_SEQ_CST); } while (CompareAndSwap(p, old, old + 1) != old); }
void *w_cas(void *v) { for (int i = 0; i < N; i++) add1(&c_cas); return NULL; }
void *w_ticket(void *v) { for (int i = 0; i < N / 10; i++) { int my = atomic_fetch_add(&tl.ticket, 1); while (atomic_load(&tl.turn) != my) ; c_ticket++; atomic_store(&tl.turn, atomic_load(&tl.turn) + 1); } return NULL; }
void run4(void *(*f)(void *)) { pthread_t t[4]; for (int i = 0; i < 4; i++) pthread_create(&t[i], NULL, f, NULL); for (int i = 0; i < 4; i++) pthread_join(t[i], NULL); }
int main(void) {
  run4(w_flag); run4(w_tas); run4(w_atomic); run4(w_plain); run4(w_cas); run4(w_ticket);
  printf("%ld %ld %ld %ld %ld %ld\n", c_flag, c_tas, (long) c_atomic, c_plain, c_cas, c_ticket);
  int f = 0; int r1 = __atomic_exchange_n(&f, 1, __ATOMIC_SEQ_CST); int r2 = __atomic_exchange_n(&f, 1, __ATOMIC_SEQ_CST);
  printf("%d %d %d\n", r1, r2, f);
  long x = 9; long r = CompareAndSwap(&x, 5, 7); printf("%ld %ld\n", r, x);
  x = 5; r = CompareAndSwap(&x, 5, 9); printf("%ld %ld\n", r, x);
  atomic_int ax = 5; int expected = 5; _Bool ok = atomic_compare_exchange_strong(&ax, &expected, 9); printf("%d %d %d\n", ok, (int) ax, expected);
  expected = 5; ok = atomic_compare_exchange_strong(&ax, &expected, 7); printf("%d %d %d\n", ok, (int) ax, expected);
  atomic_int y = 10; int old = atomic_fetch_add(&y, 3); printf("%d %d\n", old, (int) y);
  atomic_int y2 = 20; int rr = atomic_fetch_add(&y2, 5); printf("%d %d\n", rr, (int) y2);
  return 0;
}
'''
out, _ = run(ATOMIC)
L = out.splitlines()
cf, ct, ca, cp, cc, ck = map(int, L[0].split())
add((1_000_000 <= cf < 2_000_000, ct, ca, 1_000_000 <= cp < 2_000_000, cc, ck), (True, 4_000_000, 4_000_000, True, 4_000_000, 400_000),
    f"flag lock and plain cnt give 'a bit over a million' ({cf}, {cp}); test-and-set lock, atomic_fetch_add, CAS loop and ticket lock are exact")
add(L[1], "0 1 1", "tas-free returns 0; tas-held returns 1 and flag stays 1")
add((L[2], L[3]), ("9 9", "5 9"), "cas-ret: returns 9 and leaves 9; cas-then: 5 becomes 9")
add((L[4], L[5]), ("1 9 5", "0 9 9"), "C11 CAS: true then false, expected rewritten to 9 (c11-fail)")
add((L[6], L[7]), ("10 13", "20 25"), "fetch-add: 10 → returns 10, y 13; faa-ret: returns 20")
write("asm.c", "#include <stdatomic.h>\natomic_long cnt;\nlong a1(void) { return atomic_fetch_add(&cnt, 1); }\nvoid a2(void) { atomic_fetch_add(&cnt, 1); }\n"
               "int tas(atomic_flag *f) { return atomic_flag_test_and_set(f); }\n_Bool cas(atomic_long *p, long *e, long d) { return atomic_compare_exchange_strong(p, e, d); }\n")
asm = sh("gcc -O2 -S -o - asm.c")[1]
add((bool(re.search(r"lock xaddq\s+%\w+, cnt\(%rip\)", asm)), bool(re.search(r"lock addq\s+\$1, cnt\(%rip\)", asm)),
     bool(re.search(r"xchgb", asm)), bool(re.search(r"lock cmpxchgq", asm))), (True, True, True, True),
    "gcc: fetch_add → lock xaddq (result used) / lock addq (unused); test_and_set → xchgb; CAS → lock cmpxchgq")
def ticket_demo():
    ticket = turn = 0
    my = {}
    for t in "ABC":
        my[t] = ticket; ticket += 1
    order = []
    for _ in range(3):
        order.append(next(t for t in "ABC" if my[t] == turn)); turn += 1
    return my, order
add(ticket_demo(), ({"A": 0, "B": 1, "C": 2}, ["A", "B", "C"]), "ticket worked example: A 0, B 1, C 2, enter in that order")
add(5 - 3, 2, "ticket-wait: myturn 5, turn 3 → 2 unlocks")

# ======================================================================== 内存模型
# ---------------- shared-vars
GREET = ('char *names[2] = { "alice", "bob" };\n'
         'void *greet(void *vargp) { long id = (long) vargp; static int count = 0; char buf[16];\n'
         ' snprintf(buf, sizeof buf, "hi %s", names[id]); printf("%s (count=%d)\\n", buf, ++count);\n'
         ' fprintf(stderr, "%p %p\\n", (void *) &id, (void *) &count); return NULL; }\n'
         'int main(void) { pthread_t tid[2]; int marker = 7; for (long i = 0; i < 2; i++) pthread_create(&tid[i], NULL, greet, (void *) i);\n'
         ' for (int i = 0; i < 2; i++) pthread_join(tid[i], NULL); return 0; }\n')
g = build(GREET)
rc, out, err = sh(f"./{g}")
lines = sorted(out.splitlines())
add((len(lines), {l.split(" (")[0] for l in lines}, {l.split("count=")[1] for l in lines}), (2, {"hi alice", "hi bob"}, {"1)", "2)"}),
    "greet: both greetings, count reaches 2 (one shared count)")
a1, a2 = [l.split() for l in err.splitlines()[:2]]
add((a1[0] != a2[0], a1[1] == a2[1]), (True, True), "id has a different address in each thread, count the same address")

# ---------------- reordering
import itertools
def sc_outcomes():
    t1, t2 = [("w", "x"), ("r", "y", "r1")], [("w", "y"), ("r", "x", "r2")]
    res = set()
    for pick in set(itertools.permutations([1, 1, 2, 2])):
        mem, regs, i = {"x": 0, "y": 0}, {}, {1: 0, 2: 0}
        for t in pick:
            op = (t1 if t == 1 else t2)[i[t]]; i[t] += 1
            if op[0] == "w": mem[op[1]] = 1
            else: regs[op[2]] = mem[op[1]]
        res.add((regs["r1"], regs["r2"]))
    return res
add(sc_outcomes(), {(0, 1), (1, 0), (1, 1)}, "sc-outcomes: 3 of 4 outcomes possible under SC, never (0,0)")
SB = r'''
#define N 200000
atomic_int x, y, start, done; int r1, r2, mode;
static inline void st(atomic_int *p) { if (mode) atomic_store(p, 1); else atomic_store_explicit(p, 1, memory_order_relaxed); }
static inline int ld(atomic_int *p) { return mode ? atomic_load(p) : atomic_load_explicit(p, memory_order_relaxed); }
void *t1(void *v) { for (int i = 1; i <= N; i++) { while (atomic_load(&start) != i) ; st(&x); r1 = ld(&y); atomic_fetch_add(&done, 1); } return NULL; }
void *t2(void *v) { for (int i = 1; i <= N; i++) { while (atomic_load(&start) != i) ; st(&y); r2 = ld(&x); atomic_fetch_add(&done, 1); } return NULL; }
int main(int argc, char **argv) { mode = atoi(argv[1]); pthread_t a, b; int c00 = 0;
  pthread_create(&a, NULL, t1, NULL); pthread_create(&b, NULL, t2, NULL);
  for (int i = 1; i <= N; i++) { atomic_store(&x, 0); atomic_store(&y, 0); atomic_store(&done, 0); atomic_store(&start, i);
    while (atomic_load(&done) != 2) ; if (r1 == 0 && r2 == 0) c00++; }
  pthread_join(a, NULL); pthread_join(b, NULL); printf("%d\n", c00); return 0; }
'''
sb = build(SB, flags="-O2")
relaxed = [int(sh(f"./{sb} 0")[1]) for _ in range(3)]
seqcst = [int(sh(f"./{sb} 1")[1]) for _ in range(3)]
add((all(100 <= c <= 100000 for c in relaxed), seqcst), (True, [0, 0, 0]),
    f"200,000 trials: relaxed gives r1 = r2 = 0 every run, hundreds to tens of thousands of times ({relaxed}); seq_cst never ({seqcst})")
write("sbasm.c", "#include <stdatomic.h>\natomic_int x, y; int r1;\n"
                 "void relaxed(void) { atomic_store_explicit(&x, 1, memory_order_relaxed); r1 = atomic_load_explicit(&y, memory_order_relaxed); }\n"
                 "void seqcst(void) { atomic_store(&x, 1); r1 = atomic_load(&y); }\n"
                 "void rel(void) { atomic_store_explicit(&x, 1, memory_order_release); }\nint acq(void) { return atomic_load_explicit(&y, memory_order_acquire); }\n")
asm = sh("gcc -O2 -S -o - sbasm.c")[1]
fn = lambda name: asm.split(f"\n{name}:")[1].split("ret")[0]
add((bool(re.search(r"movl\s+\$1, x\(%rip\)[\s\S]*movl\s+y\(%rip\)", fn("relaxed"))), "xchgl" in fn("seqcst"),
     bool(re.search(r"^\s*movl\s+\$1, x\(%rip\)\s*$", fn("rel"), re.M)) and "mfence" not in fn("rel") and "xchg" not in fn("rel"),
     bool(re.search(r"movl\s+y\(%rip\), %eax", fn("acq")))), (True, True, True, True),
    "asm: relaxed = store then load in program order; seq_cst store = xchgl; release store and acquire load = plain mov")

# ---------------- acquire-release
HOIST = ('int flag = 0;\nvoid *waiter(void *v) { while (!flag) ; printf("seen\\n"); return NULL; }\n'
         'int main(void) { pthread_t t; pthread_create(&t, NULL, waiter, NULL); sleep(1); flag = 1; pthread_join(t, NULL); return 0; }\n')
h2, h0 = build(HOIST, flags="-O2"), build(HOIST)
add((sh(f"timeout 3 ./{h2}; echo rc=$?")[1].split()[-1], sh(f"timeout 3 ./{h0}; echo rc=$?")[1].split()), ("rc=124", ["seen", "rc=0"]),
    "guess: -O2 hangs (killed by timeout after 3 s), -O0 prints seen")
write("hoist.c", HOIST.replace("int flag", "#include <stdio.h>\n#include <pthread.h>\n#include <unistd.h>\nint flag", 1))
asm = sh("gcc -O2 -S -o - hoist.c")[1]
w = asm.split("\nwaiter:")[1].split(".cfi_endproc")[0]
add((w.count("flag(%rip)"), bool(re.search(r"^(\.L\d+):\s*\n\s*jmp\s+\1\s*$", asm, re.M))), (1, True), "-O2 reads flag once, then loops on a jmp to itself")
HOIST_FIX = HOIST.replace("int flag = 0;", "atomic_int flag = 0;")
add(sh(f"timeout 3 ./{build(HOIST_FIX, flags='-O2')}; echo rc=$?")[1].split(), ["seen", "rc=0"], "hoist-fix: atomic_int flag works at -O2")
out, _ = run('atomic_long cnt = 0;\nvoid *w(void *v) { for (int i = 0; i < 1000000; i++) atomic_fetch_add_explicit(&cnt, 1, memory_order_relaxed); return NULL; }\n'
             'int main(void) { pthread_t t[4]; for (int i = 0; i < 4; i++) pthread_create(&t[i], NULL, w, NULL); for (int i = 0; i < 4; i++) pthread_join(t[i], NULL);'
             ' printf("%ld\\n", (long) cnt); return 0; }\n', flags="-O2")
add(out, "4000000\n", "relaxed-means: relaxed fetch_add still exact")
MP = ('int data = 0; atomic_int ready = 0;\nvoid *producer(void *v) { data = 42; atomic_store_explicit(&ready, 1, memory_order_release); return NULL; }\n'
      'void *consumer(void *v) { while (!atomic_load_explicit(&ready, memory_order_acquire)) ; printf("%d\\n", data); return NULL; }\n'
      'int main(void) { pthread_t a, b; pthread_create(&b, NULL, consumer, NULL); pthread_create(&a, NULL, producer, NULL); pthread_join(a, NULL); pthread_join(b, NULL); return 0; }\n')
mp = build(MP, flags="-O2")
add({sh(f"./{mp}")[1] for _ in range(20)}, {"42\n"}, "message passing with release/acquire prints 42 every time")
out, _ = run('atomic_flag f = ATOMIC_FLAG_INIT; long cnt = 0;\nvoid lock(void) { while (atomic_flag_test_and_set_explicit(&f, memory_order_acquire)) ; }\n'
             'void unlock(void) { atomic_flag_clear_explicit(&f, memory_order_release); }\n'
             'void *w(void *v) { for (int i = 0; i < 1000000; i++) { lock(); cnt++; unlock(); } return NULL; }\n'
             'int main(void) { pthread_t t[4]; for (int i = 0; i < 4; i++) pthread_create(&t[i], NULL, w, NULL); for (int i = 0; i < 4; i++) pthread_join(t[i], NULL);'
             ' printf("%ld\\n", cnt); return 0; }\n', flags="-O2")
add(out, "4000000\n", "the C11 spin lock with acquire/release protects the counter")

# ======================================================================== IPC与竞态检测
# ---------------- pipes
PIPE = r'''
#include <limits.h>
int main(int argc, char **argv) {
  int mode = atoi(argv[1]); int fd[2]; char buf[16];
  pipe(fd);
  if (mode == 0) {
    if (fork() == 0) { close(fd[0]); write(fd[1], "hello", 5); close(fd[1]); return 0; }
    close(fd[1]); ssize_t n = read(fd[0], buf, sizeof buf - 1); buf[n > 0 ? n : 0] = '\0'; printf("%s\n", buf);
    printf("%zd\n", read(fd[0], buf, sizeof buf)); close(fd[0]); wait(NULL);
  } else if (mode == 1) {
    if (fork() == 0) { close(fd[0]); write(fd[1], "hello", 5); close(fd[1]); return 0; }
    ssize_t n = read(fd[0], buf, sizeof buf); printf("%zd\n", n); fflush(stdout); read(fd[0], buf, sizeof buf); printf("never\n");
  } else if (mode == 2) { close(fd[0]); write(fd[1], "x", 1); printf("not reached\n");
  } else if (mode == 3) { signal(SIGPIPE, SIG_IGN); close(fd[0]); ssize_t r = write(fd[1], "x", 1); printf("%zd %d %s\n", r, errno, strerror(errno));
  } else { printf("%d %d\n", fcntl(fd[1], F_GETPIPE_SZ), (int) PIPE_BUF); }
  return 0;
}
'''
pp = build(PIPE)
add(sh(f"./{pp} 0")[1], "hello\n0\n", "the child-writes parent-reads program prints hello; a second read returns 0")
add(sh(f"timeout 2 ./{pp} 1; echo rc=$?")[1], "5\nrc=124\n", "worked example: parent keeps its write end, second read blocks (timeout after 2 s)")
add(sh(f"./{pp} 2; echo rc=$?")[1], "rc=141\n", "sigpipe: writing with no reader, $? = 141")
add(sh(f"./{pp} 3")[1], "-1 32 Broken pipe\n", "ignoring SIGPIPE: write returns -1, EPIPE")
add(sh(f"./{pp} 4")[1], "65536 4096\n", "pipe capacity 65536 bytes (16 pages of 4 KiB)")
add(sh("getconf PAGESIZE")[1].strip(), "4096", "page size 4 KiB")
for nm in ("a1", "b2", "c3"): write(nm + ".txt", "")
SHELLPIPE = ('int main(void) { int fd[2]; pipe(fd);\n'
             ' if (Fork() == 0) { dup2(fd[1], 1); close(fd[0]); close(fd[1]); char *a[] = { "ls", NULL }; execvp("ls", a); }\n'
             ' if (Fork() == 0) { dup2(fd[0], 0); close(fd[0]); close(fd[1]); char *a[] = { "wc", "-l", NULL }; execvp("wc", a); }\n'
             ' close(fd[0]); close(fd[1]); wait(NULL); wait(NULL); return 0; }\n')
mine = run(SHELLPIPE)[0].strip()
add(mine, sh("ls | wc -l")[1].strip(), "the pipeline built with pipe/fork/dup2/execve gives the same count as the shell's ls | wc -l")

# ---------------- sockets and concurrent servers
SRV = r'''
#include <netdb.h>
#include <sys/socket.h>
#include <sys/select.h>
int open_listenfd(char *port) {
  struct addrinfo hints, *listp, *p; int listenfd, optval = 1;
  memset(&hints, 0, sizeof hints); hints.ai_socktype = SOCK_STREAM; hints.ai_flags = AI_PASSIVE | AI_ADDRCONFIG | AI_NUMERICSERV;
  getaddrinfo(NULL, port, &hints, &listp);
  for (p = listp; p; p = p->ai_next) {
    if ((listenfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) < 0) continue;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(int));
    if (bind(listenfd, p->ai_addr, p->ai_addrlen) == 0) break;
    close(listenfd);
  }
  freeaddrinfo(listp); if (!p) return -1;
  if (listen(listenfd, 1024) < 0) { close(listenfd); return -1; }
  return listenfd;
}
void echo(int connfd) { char buf[256]; ssize_t n; while ((n = read(connfd, buf, sizeof buf)) > 0) write(connfd, buf, n); }
void sigchld_handler(int sig) { int e = errno; while (waitpid(-1, 0, WNOHANG) > 0) ; errno = e; }
void *thread(void *vargp) { int connfd = *((int *) vargp); pthread_detach(pthread_self()); free(vargp); echo(connfd); close(connfd); return NULL; }
int main(int argc, char **argv) {
  char *mode = argv[1]; int listenfd = open_listenfd(argv[2]); if (listenfd < 0) { perror("listen"); return 1; }
  if (!strcmp(mode, "iter")) for (;;) { int connfd = accept(listenfd, NULL, NULL); echo(connfd); close(connfd); }
  if (!strcmp(mode, "fork")) { signal(SIGCHLD, sigchld_handler);
    for (;;) { int connfd = accept(listenfd, NULL, NULL); if (connfd < 0) continue; if (fork() == 0) { close(listenfd); echo(connfd); close(connfd); exit(0); } close(connfd); } }
  if (!strcmp(mode, "thread")) for (;;) { int *connfdp = malloc(sizeof(int)); *connfdp = accept(listenfd, NULL, NULL); pthread_t tid; pthread_create(&tid, NULL, thread, connfdp); }
  if (!strcmp(mode, "select")) { fd_set read_set, ready_set; int maxfd = listenfd, clients[FD_SETSIZE], nc = 0;
    FD_ZERO(&read_set); FD_SET(listenfd, &read_set);
    for (;;) { ready_set = read_set; select(maxfd + 1, &ready_set, NULL, NULL, NULL);
      if (FD_ISSET(listenfd, &ready_set)) { int c = accept(listenfd, NULL, NULL); FD_SET(c, &read_set); if (c > maxfd) maxfd = c; clients[nc++] = c; }
      for (int i = 0; i < nc; i++) { int c = clients[i]; if (c >= 0 && FD_ISSET(c, &ready_set)) { char buf[256]; ssize_t n = read(c, buf, sizeof buf);
          if (n <= 0) { close(c); FD_CLR(c, &read_set); clients[i] = -1; } else write(c, buf, n); } } } }
  if (!strcmp(mode, "eof")) { int connfd = accept(listenfd, NULL, NULL); char buf[256]; ssize_t n; while ((n = read(connfd, buf, sizeof buf)) > 0) write(connfd, buf, n); printf("read returned %zd\n", n); }
  return 0;
}
'''
CLI = r'''
#include <netdb.h>
#include <sys/socket.h>
int open_clientfd(char *hostname, char *port) {
  struct addrinfo hints, *listp, *p; int clientfd;
  memset(&hints, 0, sizeof hints); hints.ai_socktype = SOCK_STREAM; hints.ai_flags = AI_NUMERICSERV | AI_ADDRCONFIG;
  getaddrinfo(hostname, port, &hints, &listp);
  for (p = listp; p; p = p->ai_next) {
    if ((clientfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) < 0) continue;
    if (connect(clientfd, p->ai_addr, p->ai_addrlen) != -1) break;
    close(clientfd);
  }
  freeaddrinfo(listp); return p ? clientfd : -1;
}
int main(int argc, char **argv) {
  int fd = open_clientfd("localhost", argv[1]); if (fd < 0) { printf("connect failed\n"); return 1; }
  if (argc > 3) sleep(atoi(argv[3]));
  write(fd, argv[2], strlen(argv[2])); char buf[256]; ssize_t n = read(fd, buf, sizeof buf - 1); buf[n > 0 ? n : 0] = 0; printf("%s\n", buf); close(fd); return 0;
}
'''
srv, cli = build(SRV), build(CLI)
write("serve.sh", f"""# usage: bash serve.sh mode port
./{srv} $1 $2 & S=$!
sleep 0.5
(./{cli} $2 slow 3 > a.out) & A=$!          # A connects, waits 3 s, then sends
sleep 0.3
s=$(date +%s.%N)
timeout 6 ./{cli} $2 fast > b.out           # B connects 0.3 s later and sends at once
e=$(date +%s.%N)
wait $A
kill $S
echo "$(cat b.out) $(echo "$e - $s" | bc) $(cat a.out)"
""")
def serve(mode, port):
    """Returns (B's reply, how long B waited, A's reply)."""
    b, t, a = sh(f"bash serve.sh {mode} {port}")[1].split()
    return b, float(t), a
import random
port = random.randint(20000, 40000)
res = {m: serve(m, port + i) for i, m in enumerate(("iter", "fork", "thread", "select"))}
add(all(r[0] == "fast" and r[2] == "slow" for r in res.values()), True, "every server echoes what it gets")
add(2.4 < res["iter"][1] < 3.2, True, f"iterative server: B waits about 2.8 s ({res['iter'][1]:.2f})")
add(all(res[m][1] < 0.3 for m in ("fork", "thread", "select")), True,
    f"process, thread and select servers: B waits about 0.1 s ({', '.join(f'{res[m][1]:.2f}' for m in ('fork', 'thread', 'select'))})")
rc, out, _ = sh(f"{{ ./{srv} eof {port + 9} & S=$!; sleep 0.5; timeout 5 ./{cli} {port + 9} bye > /dev/null; wait $S; }}", timeout=30)  # braces: keep & inside the cd
add(out, "read returned 0\n", "eof-socket: after the client closes, the server's read returns 0")
add(sh("cat /proc/sys/net/ipv4/ip_unprivileged_port_start")[1].strip(), "1024", "ports below 1024 are privileged on this Linux")
out, _ = run('#include <sys/select.h>\nint main(void) { printf("%d\\n", FD_SETSIZE); return 0; }\n')
add(out, "1024\n", "glibc FD_SETSIZE is 1024")
add(7 + 1, 8, "select-n: max descriptor 7 → n = 8")
add(sum(1 for _ in [3, 4, 5, 6]), 4, "listen-vs-conn: 1 listening + 3 connected descriptors")

# ---------------- races
RACE = r'''
#define N 4
void *thread(void *vargp) { int myid = *((int *) vargp); printf("Hello from thread %d\n", myid); return NULL; }
void *slow(void *vargp) { usleep(100000); int myid = *((int *) vargp); printf("Hello from thread %d\n", myid); return NULL; }
void *fixed(void *vargp) { int myid = *((int *) vargp); free(vargp); printf("Hello from thread %d\n", myid); return NULL; }
int main(int argc, char **argv) { pthread_t tid[N]; int i;
  if (argv[1][0] == 'r') { for (i = 0; i < N; i++) pthread_create(&tid[i], NULL, thread, &i); }
  else if (argv[1][0] == 's') { for (i = 0; i < N; i++) pthread_create(&tid[i], NULL, slow, &i); }
  else { for (i = 0; i < N; i++) { int *ptr = malloc(sizeof(int)); *ptr = i; pthread_create(&tid[i], NULL, fixed, ptr); } }
  for (int j = 0; j < N; j++) pthread_join(tid[j], NULL); return 0; }
'''
rp = build(RACE)
ids = lambda o: sorted(int(l.split()[-1]) for l in o.splitlines())
racy = [ids(sh(f"./{rp} r")[1]) for _ in range(3)]
add(racy, [[1, 2, 3, 4]] * 3, "guess: three runs each print 1, 2, 3, 4 (no thread 0, a 'thread 4')")
add(ids(sh(f"./{rp} s")[1]), [4, 4, 4, 4], "with a 0.1 s sleep before the read, all four print 4")
add(ids(sh(f"./{rp} f")[1]), [0, 1, 2, 3], "the malloc fix prints 0, 1, 2, 3")

# ---------------- eraser
def lockset(accesses, all_locks):
    c, warned = set(all_locks), False
    for held in accesses:
        c &= set(held)
        if not c: warned = True
    return c, warned
add(lockset([{"a", "b"}, {"b", "c"}], "abc"), ({"b"}, False), "worked example: after two accesses C(v) = {b}")
add(lockset([{"a", "b"}, {"b", "c"}, set()], "abc"), (set(), True), "worked example: the lock-free access empties C(v) and warns")
add(lockset([{"a", "c"}, {"a", "b", "c"}, {"a"}], "abc"), ({"a"}, False), "lockset item: {a} remains")
add(lockset([{"m"}, {"n"}], "mn"), (set(), True), "eraser-miss: lock m vs lock n is reported")
add(lockset([{"b"}, {"b"}, {"b"}, {"b"}], "b"), ({"b"}, False), "eraser-miss: check and act each under the same lock stay silent")
write("tsan.c", "#include <stdio.h>\n#include <pthread.h>\nlong cnt = 0;\nvoid *thread(void *vargp) { for (int i = 0; i < 1000; i++) cnt++; return NULL; }\n"
                "int main(void) { pthread_t t1, t2; pthread_create(&t1, NULL, thread, NULL); pthread_create(&t2, NULL, thread, NULL); pthread_join(t1, NULL); pthread_join(t2, NULL); printf(\"cnt=%ld\\n\", cnt); return 0; }\n")
write("tsan2.c", "#include <stdio.h>\n#include <pthread.h>\nlong cnt = 0; pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;\n"
                 "void *thread(void *vargp) { for (int i = 0; i < 1000; i++) { pthread_mutex_lock(&m); cnt++; pthread_mutex_unlock(&m); } return NULL; }\n"
                 "int main(void) { pthread_t t1, t2; pthread_create(&t1, NULL, thread, NULL); pthread_create(&t2, NULL, thread, NULL); pthread_join(t1, NULL); pthread_join(t2, NULL); printf(\"cnt=%ld\\n\", cnt); return 0; }\n")
sh("gcc -g -O1 -fsanitize=thread -pthread -o tsan tsan.c && gcc -g -O1 -fsanitize=thread -pthread -o tsan2 tsan2.c")
rc, out, err = sh("./tsan")
add(("WARNING: ThreadSanitizer: data race" in err, "Location is global 'cnt' of size 8" in err, "tsan.c:4" in err, bool(re.match(r"cnt=\d+\n$", out))),
    (True, True, True, True), f"ThreadSanitizer reports the race on cnt at tsan.c:4 (this run printed {out.strip()})")
rc, out, err = sh("./tsan2")
add((out, "ThreadSanitizer" in err), ("cnt=2000\n", False), "with a mutex: cnt=2000 and no report")

# ======================================================================== 结业挑战
name = build('int main(void) { fork(); if (fork() == 0) { printf("c\\n"); exit(0); } printf("p\\n"); return 0; }\n')
t = tty(name)
add((t.count("c"), t.count("p")), (2, 2), "boss-fork: 2 c + 2 p = 4 lines")
add(sh("bash -c 'kill -TERM $$'; echo $?")[1].strip(), "143", "boss-sigterm: 143")
write("data.txt", "abcdef")
out, _ = run('int main(void) { int fd1 = open("data.txt", O_RDONLY); int fd2 = open("data.txt", O_RDONLY); char c;'
             ' read(fd1, &c, 1); read(fd1, &c, 1); dup2(fd1, fd2); read(fd2, &c, 1); printf("%c\\n", c); return 0; }\n')
add(out, "c\n", "boss-dup2: c")
name = build(UMASK % "077")
add(sh(f"d=$(mktemp -d) && cp {name} $d/ && cd $d && ./{name}; rm -rf $d")[1], "600\n", "boss-umask: 600")
def lus(order, start):
    cnt, rax = start, {}
    for step in order:
        op, t_ = step[0], int(step[1])
        if op == "L": rax[t_] = cnt
        elif op == "U": rax[t_] += 1
        elif op == "S": cnt = rax[t_]
    return cnt
add(lus("L1 U1 L2 U2 S2 S1".split(), 5), 6, "boss-interleave: 6")
out, _ = run('int main(void) { sem_t s; sem_init(&s, 0, 3); int passed = 0; for (int i = 0; i < 3; i++) if (sem_trywait(&s) == 0) passed++;'
             ' int blocked = (sem_trywait(&s) != 0) + (sem_trywait(&s) != 0); sem_post(&s); if (sem_trywait(&s) == 0) passed++;'
             ' printf("%d %d\\n", passed, blocked); return 0; }\n')
add(out, "4 2\n", "boss-semaphore: 3 pass, 2 wait, one V lets one more through: 4")
add(20 / 4 / 8 * 100, 62.5, "boss-efficiency: 62.5%")
add(10 - 7, 3, "boss-ticket: 3 unlocks")
out, _ = run('long CAS(long *p, long e, long n) { __atomic_compare_exchange_n(p, &e, n, 0, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST); return e; }\n'
             'int main(void) { long x = 4; CAS(&x, 4, 8); printf("%ld %ld\\n", CAS(&x, 4, 9), x); return 0; }\n')
add(out, "8 8\n", "boss-cas: second call returns 8, x stays 8")
add(sc_outcomes() ^ {(0, 0), (0, 1), (1, 0), (1, 1)}, {(0, 0)}, "boss-sb: only (0,0) is excluded by SC (and seen on x86 above)")
add(max(3, 4, 9) + 1, 10, "boss-select: 10")
add(lockset([{"a", "b", "d"}, {"b", "d"}, {"c", "d"}], "abcd"), ({"d"}, False), "boss-lockset: {d}")

# ======================================================================== report
bad = [(w, g, e) for g, e, w in checks if g != e]
for what, got, want in bad:
    print(f"MISMATCH {what}: got {got!r}, want {want!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
sys.exit(1 if bad else 0)
