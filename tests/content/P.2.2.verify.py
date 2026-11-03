# Checks every output, value, size and error message that data/content/P.2.2.yaml states, by compiling
# and running C with gcc (64-bit Linux: the sizes in the lessons are the common LP64 ones).
# usage: python -I tests/content/P.2.2.verify.py   (prints "N/N claims hold"; exit code 1 on any mismatch)
# Uses gcc on PATH if it is there, otherwise WSL's gcc (wsl.exe -e ...). Scratch files go to temp/c-verify.
import os, shutil, subprocess, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORK = os.path.join(ROOT, "temp", "c-verify")
os.makedirs(WORK, exist_ok=True)
NATIVE = shutil.which("gcc") and sys.platform != "win32"

def wsl_path(p):
    p = os.path.abspath(p).replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:] if p[1] == ":" else p

def sh(cmd):
    """Run a shell command in the work directory; returns (exit code, stdout, stderr)."""
    if NATIVE:
        r = subprocess.run(["sh", "-c", cmd], cwd=WORK, capture_output=True)
    else:
        r = subprocess.run(["wsl.exe", "-e", "sh", "-c", f"cd '{wsl_path(WORK)}' && {cmd}"], capture_output=True)
    dec = lambda b: b.decode("utf-8", "replace").replace("\r", "")
    return r.returncode, dec(r.stdout), dec(r.stderr)

HEAD = "#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <unistd.h>\n"
n = 0
def write(name, text):
    with open(os.path.join(WORK, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def run(src, body=True, flags=""):
    """Compile and run; body=True wraps src in main(). Returns (stdout, exit code)."""
    global n
    n += 1
    name = f"t{n}"
    code = HEAD + (f"int main(void) {{\n{src}\nreturn 0;\n}}\n" if body else src)
    write(name + ".c", code)
    rc, out, err = sh(f"gcc {flags} -o {name} {name}.c && ./{name}")
    if rc and "error" in err:
        return ("COMPILE ERROR: " + err, rc)
    return (out, rc)

def out(src, **kw):
    return run(src, **kw)[0]

def compile_err(src):
    global n
    n += 1
    write(f"e{n}.c", src)
    return sh(f"gcc -c -o /dev/null e{n}.c")[2]

checks = [
    # hello-c
    (out('printf("A");\nprintf("B\\n");\nprintf("C\\n");'), "AB\nC\n"),
    ("expected ‘;’ before ‘return’" in compile_err('#include <stdio.h>\nint main(void) {\n    printf("one\\n");\n    printf("two\\n")\n    return 0;\n}\n'), True),
    ("c.c:4:20:".split(":")[1], "4"),
    # c-basics
    (out('int x = 7 / 2;\nprintf("%d\\n", x);'), "3\n"),
    (out('printf("%d\\n", 7 / 2);\nprintf("%f\\n", 7.0 / 2);'), "3\n3.500000\n"),
    (out('int a = 17, b = 5;\nprintf("%d\\n", a / b + a % b);'), "5\n"),
    (out('for (int i = 0; i < 5; i++) {\nprintf("%d ", i);\n}'), "0 1 2 3 4 "),
    (out('int sum = 0;\nfor (int i = 1; i <= 3; i++) { sum = sum + i; }\nprintf("%d\\n", sum);'), "6\n"),
    (out('int sum = 0;\nfor (int i = 1; i <= 4; i++) { sum = sum + i * i; }\nprintf("%d\\n", sum);'), "30\n"),
    (out('int count = 0;\nfor (int i = 10; i > 0; i = i - 3) { count++; }\nprintf("%d\\n", count);'), "4\n"),
    # multi-file: undefined reference at link time, the same file compiles alone
]
write("mathx.h", "int add(int a, int b);\n")
write("mathx.c", "int add(int a, int b) { return a + b; }\n")
write("main.c", '#include <stdio.h>\n#include "mathx.h"\nint main(void) { printf("%d\\n", add(2, 3)); return 0; }\n')
rc_c, _, _ = sh("gcc -c main.c -o main.o")
rc_l, _, err_l = sh("gcc main.c -o app_bad")
rc_ok, out_ok, _ = sh("gcc main.c mathx.c -o app && ./app")
rc_sep, out_sep, _ = sh("gcc -c main.c && gcc -c mathx.c && gcc main.o mathx.o -o app2 && ./app2 && ls hello.o 2>/dev/null; echo 'int main(void){return 0;}' > hello.c && gcc -c hello.c && ls hello.o")
checks += [
    (rc_c, 0), (rc_l != 0 and "undefined reference to `add'" in err_l, True),
    (out_ok, "5\n"), (out_sep.strip().endswith("hello.o") and out_sep.startswith("5\n"), True),
    # syscalls
    (out('fflush(stdout);\nwrite(1, "hello\\n", 3);'), "hel"),
    (run('#include <stdio.h>\nint main(void) { return 3; }\n', body=False)[1], 3),
    # bytes-addresses
    (out('printf("%zu %zu %zu %zu\\n", sizeof(char), sizeof(int), sizeof(double), sizeof(int *));'), "1 4 8 8\n"),
    (3 * 4 + 8, 20), (0x1F, 31), (0x10, 16), (1000 + 4, 1004), (2000 + 8, 2008),
    (out('int a[2]; printf("%td\\n", (char *)&a[1] - (char *)&a[0]);'), "4\n"),
    (out('double d[2]; printf("%td\\n", (char *)&d[1] - (char *)&d[0]);'), "8\n"),
    # pointers
    (out('int x = 42;\nint *p = &x;\n*p = 7;\nprintf("%d\\n", x);'), "7\n"),
    (out('double *q; printf("%zu\\n", sizeof(q));'), "8\n"),
    (out('int a = 5;\nint *p = &a;\n*p = *p + 10;\nprintf("%d\\n", a);'), "15\n"),
    (out('int a = 1, b = 2;\nint *p = &a;\n*p = 10;\np = &b;\n*p = 20;\nprintf("%d %d\\n", a, b);'), "10 20\n"),
    (out('int a = 3, b = 4;\nint *p = &b;\n*p = a;\np = &a;\n*p = 9;\nprintf("%d\\n", a + b);'), "12\n"),
    (out('void add_one(int n) { n = n + 1; }\nvoid add_one_p(int *n) { *n = *n + 1; }\nint main(void) { int x = 5; add_one(x); printf("%d ", x); add_one_p(&x); printf("%d\\n", x); return 0; }', body=False), "5 6\n"),
    (out('void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }\nvoid swap2(int a, int b) { int t = a; a = b; b = t; }\nint main(void) { int x = 1, y = 2; swap2(x, y); printf("%d %d ", x, y); swap(&x, &y); printf("%d %d\\n", x, y); return 0; }', body=False), "1 2 2 1\n"),
    (out('void triple(int *n) { *n = *n * 3; }\nint main(void) { int x = 4; triple(&x); triple(&x); printf("%d\\n", x); return 0; }', body=False), "36\n"),
    (run('int *p = NULL;\n*p = 5;\nprintf("never\\n");')[1], 139),
    # arrays
    (out('int a[3] = {10, 20, 30};\nint *p = a;\nprintf("%d\\n", *(p + 1));'), "20\n"),
    (out('int a[5] = {3, 8, 5, 2, 9};\nprintf("%d\\n", a[1] + a[4]);'), "17\n"),
    (out('int a[4]; int *p = a + 2; printf("%td\\n", (char *)p - (char *)a);'), "8\n"),
    (out('int a[4] = {5, 1, 4, 2};\nint *p = a;\np = p + 2;\nprintf("%d\\n", *p);\np = p - 1;\nprintf("%d\\n", *p + *(p + 2));'), "4\n3\n"),
    (out('int a[5] = {2, 4, 6, 8, 10};\nint *p = a + 1;\nprintf("%d\\n", *(p + 2) - *p);'), "4\n"),
    (out('int sum(int *a, int n) { int s = 0; for (int i = 0; i < n; i++) s = s + a[i]; return s; }\nint main(void) { int b[3] = {3, 5, 7}; printf("%d %d\\n", sum(b, 3), sum(b + 1, 2)); return 0; }', body=False), "15 12\n"),
    # c-strings
    (out('char s[] = "cat"; printf("%zu\\n", sizeof(s));'), "4\n"),
    (out('char s[] = "hello"; printf("%zu %zu\\n", sizeof(s), strlen(s));'), "6 5\n"),
    (out('printf("%c %d %d\\n", \'A\' + 2, \'A\', \'a\');'), "C 65 97\n"),
    (out('printf("%zu\\n", strlen("hi there"));'), "8\n"),
    (out('char a[] = "abc"; char b[] = "abc"; printf("%d %d\\n", a == b, strcmp(a, b) == 0);', flags="-w"), "0 1\n"),
    (out('char d[8]; strcpy(d, "world"); printf("%zu\\n", sizeof("world"));'), "6\n"),
    (len("hello") + 1, 6),
    # memory-map
    (out('#include <stdio.h>\nint count;\nint main(void) { printf("%d\\n", count); return 0; }', body=False), "0\n"),
    (out('#include <stdio.h>\n#include <stdlib.h>\n#include <stdint.h>\nint g = 1; int s;\n'
         'int main(void) { int a = 0; int *p = malloc(4);\n'
         'uintptr_t m = (uintptr_t)main, G = (uintptr_t)&g, S = (uintptr_t)&s, H = (uintptr_t)p, A = (uintptr_t)&a;\n'
         'printf("%d\\n", m < G && G < S && S < H && H < A); return 0; }', body=False), "1\n"),
    # stack-frames
    (out('int fact(int n) { if (n <= 1) return 1; return n * fact(n - 1); }\nint main(void) { printf("%d\\n", fact(4)); return 0; }', body=False), "24\n"),
    (sh("ulimit -s")[1].strip(), "8192"),
    (run('int f(int n) { return 1 + f(n + 1); }\nint main(void) { return f(0); }\n', body=False)[1], 139),
    # lifetime
    (out('void tick(void) { static int n = 0; n = n + 1; printf("%d\\n", n); }\nint main(void) { tick(); tick(); tick(); return 0; }', body=False), "1\n2\n3\n"),
    (out('void tick(void) { int n = 0; n = n + 1; printf("%d\\n", n); }\nint main(void) { tick(); tick(); tick(); return 0; }', body=False), "1\n1\n1\n"),
    (out('int f(void) { static int s = 0; int t = 0; s = s + 1; t = t + 1; return s + t; }\nint main(void) { f(); f(); printf("%d\\n", f()); return 0; }', body=False), "4\n"),
    # heap
    (out('double *d = malloc(10 * sizeof(double)); printf("%zu\\n", 10 * sizeof(double)); free(d);'), "80\n"),
    (out('int *make_squares(int n) { int *a = malloc(n * sizeof(int)); for (int i = 0; i < n; i++) a[i] = i * i; return a; }\n'
         'int main(void) { int *s = make_squares(4); printf("%d ", s[3]); free(s); s = make_squares(5); printf("%d\\n", s[2] + s[4]); free(s); return 0; }', body=False), "9 20\n"),
    (3 * 100, 300),
    # memory-bugs
    ("function returns address of local variable" in sh("cat > w.c <<'X'\n#include <stdio.h>\nchar *make_greeting(char *name) { char buf[64]; sprintf(buf, \"Hello, %s!\", name); return buf; }\nint *f(void) { int x = 1; return &x; }\nX\ngcc -Wall -c w.c -o /dev/null")[2], True),
    (out('char buf[64]; int k = sprintf(buf, "Hello, %s!", "Alice"); printf("%d %zu\\n", k + 1, strlen("Hello, ") + strlen("!"));'), "14 8\n"),
    (64 - 7 - 1 - 1, 55),
    (out('char buf[8]; snprintf(buf, 8, "Hello, %s!", "Alice"); printf("[%s] %zu\\n", buf, strlen(buf));', flags="-w"), "[Hello, ] 7\n"),
    ("heap-use-after-free" in sh("cat > u.c <<'X'\n#include <stdlib.h>\nint main(void) { int *p = malloc(sizeof(int)); free(p); p[0] = 3; return 0; }\nX\ngcc -w -fsanitize=address -g u.c -o u && ./u")[2], True),
    # boss
    (out('int a[4] = {1, 2, 3, 4};\nint *p = a + 1;\n*p = *p * 10;\nprintf("%d\\n", a[0] + a[1]);'), "21\n"),
    (out('char s[] = "abc"; int n[3]; printf("%zu\\n", sizeof(s) + sizeof(n));'), "16\n"),
    (out('int next(void) { static int c = 10; c = c + 5; return c; }\nint main(void) { next(); next(); next(); printf("%d\\n", next()); return 0; }', body=False), "30\n"),
    (out('void step(int *x, int y) { *x = *x + y; y = 0; }\nint main(void) { int a = 2, b = 5; step(&a, b); step(&a, b); printf("%d\\n", a + b); return 0; }', body=False), "17\n"),
    (5 * 20, 100),
    (out('char w[10] = "hey"; printf("%zu\\n", sizeof(w) - strlen(w));'), "7\n"),
]

# ---- lessons added 2026-11-03 for knowledge coverage (reports/coverage/P.2.2.md) ----
def nm_table(obj):
    """{symbol: letter} from `nm obj`."""
    rows = [l.split() for l in sh(f"nm {obj}")[1].splitlines() if l.strip()]
    return {r[-1]: r[-2] for r in rows}

def asm_lines(src, flags):
    """Instruction lines of `gcc -S`, without directives, labels starting with .L and endbr64."""
    write("asm.c", src)
    text = sh(f"gcc -S {flags} -o - asm.c")[1]
    keep = []
    for l in text.splitlines():
        l = " ".join(l.split())
        if not l or l.startswith(".") or l == "endbr64" or l[0].isdigit():
            continue
        keep.append(l)
    return keep

A_C = "int count = 3;\nint total;\nstatic int hidden = 7;\nstatic int helper(int x) { return x * 2; }\nint twice(int x) { return helper(x) + hidden; }\n"
B_C = '#include <stdio.h>\nextern int count;\nint twice(int x);\nint main(void) {\n    printf("%d\\n", twice(count));\n    return 0;\n}\n'
write("a.c", A_C); write("b.c", B_C); write("c.c", "int count = 5;\n")
write("b2.c", "int helper(int x);\nint main(void) { return helper(1); }\n")
write("x.c", "int helper(void) { return 1; }\nint fx(void) { return helper(); }\n")
write("y.c", "int helper(void) { return 2; }\nint fy(void) { return helper(); }\nint fx(void);\nint main(void) { return fx() + fy(); }\n")
write("xs.c", "static int helper(void) { return 1; }\nint fx(void) { return helper(); }\n")
write("ys.c", "static int helper(void) { return 2; }\nint fy(void) { return helper(); }\nint fx(void);\nint main(void) { return fx() + fy(); }\n")
sh("gcc -c a.c b.c")
SQRT_C = '#include <math.h>\n#include <stdio.h>\n#include <stdlib.h>\nint main(int argc, char **argv) { double x = atof(argv[1]); printf("%f\\n", sqrt(x)); return 0; }\n'
SQRT2_C = '#include <math.h>\n#include <stdio.h>\nint main(void) { printf("%f\\n", sqrt(2.0)); return 0; }\n'
write("m2.c", SQRT_C); write("m.c", SQRT2_C)
write("mylib.c", "int square(int x) { return x * x; }\n")
write("app.c", '#include <stdio.h>\nint square(int x);\nint main(void) { printf("%d\\n", square(7)); return 0; }\n')
write("dl.c", '#include <dlfcn.h>\n#include <stdio.h>\nint main(void) { void *h = dlopen("./libmylib.so", RTLD_NOW); int (*sq)(int) = (int (*)(int))dlsym(h, "square"); printf("%d\\n", sq(7)); return 0; }\n')
FIO_C = '''#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(void) {
    int fd = open("note.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    printf("fd = %d\\n", fd);
    write(fd, "hi\\n", 3);
    close(fd);
    char buf[64];
    fd = open("note.txt", O_RDONLY);
    ssize_t n = read(fd, buf, 64);
    printf("n = %zd\\n", n);
    n = read(fd, buf, 64);
    printf("n = %zd\\n", n);
    close(fd);
    int bad = open("nope.txt", O_RDONLY);
    printf("bad = %d\\n", bad);
    fflush(stdout);
    perror("open");
    return 0;
}
'''
write("fio.c", FIO_C)
write("cat.c", '#include <fcntl.h>\n#include <unistd.h>\nint main(void) { char buf[64]; ssize_t n; int fd = open("note.txt", O_RDONLY);\n    while ((n = read(fd, buf, sizeof buf)) > 0)\n        write(1, buf, n);\n    close(fd); return 0; }\n')
write("modes.c", '#include <fcntl.h>\n#include <unistd.h>\nint main(void) { int fd = open("m.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644); write(fd, "abc", 3); close(fd);\n fd = open("m.txt", O_WRONLY | O_TRUNC); write(fd, "x", 1); close(fd);\n fd = open("m.txt", O_WRONLY | O_APPEND); write(fd, "y", 1); close(fd); return 0; }\n')
write("perm.c", '#include <fcntl.h>\n#include <unistd.h>\nint main(void) { close(open("/dev/shm/cs-verify-644", O_WRONLY | O_CREAT | O_TRUNC, 0644)); close(open("/dev/shm/cs-verify-600", O_WRONLY | O_CREAT | O_TRUNC, 0600)); return 0; }\n')
write("redir.c", '#include <stdio.h>\n#include <fcntl.h>\nint main(void) { printf("out\\n"); fflush(stdout); open("nope.txt", O_RDONLY); perror("open"); return 0; }\n')
write("pw.c", '#include <stdio.h>\n#include <unistd.h>\nint main(void) { printf("a\\n"); write(1, "b\\n", 2); return 0; }\n')
GREET_C = '#include <stdio.h>\n#include <string.h>\nvoid greet(const char *name) {\n    char buf[16];\n    strcpy(buf, name);\n    printf("%s\\n", buf);\n}\nint main(void) { greet("a name that is much too long for sixteen"); return 0; }\n'
write("ov.c", GREET_C)
SUB_C = "long sub(long a, long b) { return a - b; }\nlong twice_sub(long a, long b) { return sub(a, b) * 2; }\n"
SWAP = "void swap(void *a, void *b, size_t n) {\n    char tmp[n];\n    memcpy(tmp, a, n);\n    memcpy(a, b, n);\n    memcpy(b, tmp, n);\n}\n"
POINT = "struct point { int x; int y; };\n"
MOVE = "void move_right(struct point *p) {\n    p->x = p->x + 1;\n}\n"
VEC = '''typedef struct { int *data; int size; int cap; } Vec;
int reallocs = 0;
void push(Vec *v, int x) {
    if (v->size == v->cap) {
        v->cap = v->cap * 2;
        v->data = realloc(v->data, v->cap * sizeof(int));
        reallocs++;
    }
    v->data[v->size++] = x;
}
'''
NODE = "struct node {\n    int value;\n    struct node *next;\n};\nstruct node *push_front(struct node *head, int v) {\n    struct node *n = malloc(sizeof *n);\n    n->value = v;\n    n->next = head;\n    return n;\n}\n"
CMP_INT = "int cmp_int(const void *a, const void *b) {\n    int x = *(const int *)a, y = *(const int *)b;\n    return (x > y) - (x < y);\n}\nint cmp_desc(const void *a, const void *b) {\n    int x = *(const int *)a, y = *(const int *)b;\n    return (x < y) - (x > y);\n}\n"
CMP_STR = "int cmp_str(const void *a, const void *b) {\n    return strcmp(*(char *const *)a, *(char *const *)b);\n}\n"

def allocator_model(heap, requests):
    """CS107-style implicit list, first fit, 8-byte headers, payloads rounded up to 8, split only when the
    rest can hold a header and an 8-byte payload. Returns the payload offsets and sizes handed out."""
    blocks = [[0, heap - 8, False]]          # [header offset, payload size, used]
    got = []
    for n in requests:
        need = (n + 7) // 8 * 8
        for i, (off, size, used) in enumerate(blocks):
            if used or size < need:
                continue
            if size - need >= 8 + 8:
                blocks[i:i + 1] = [[off, need, True], [off + 8 + need, size - need - 8, False]]
                got.append((off + 8, need))
            else:
                blocks[i][2] = True
                got.append((off + 8, size))
            break
        else:
            got.append(None)
    return got, blocks

shm_rc, shm_out, _ = sh("gcc perm.c -o perm && umask 022 && ./perm && stat -c %a /dev/shm/cs-verify-644 /dev/shm/cs-verify-600; rm -f /dev/shm/cs-verify-644 /dev/shm/cs-verify-600")
# -lmylib takes libmylib.so over libmylib.a when both are there, so the static build runs first, alone
static_rc = sh("rm -f libmylib.so libmylib.a && gcc -c mylib.c && ar rcs libmylib.a mylib.o && gcc app.c -L. -lmylib -o app_static && rm -f libmylib.a && ./app_static")
both = sh("gcc -c mylib.c && ar rcs libmylib.a mylib.o && gcc -shared -fPIC mylib.c -o libmylib.so && gcc app.c -L. -lmylib -o app_both && ldd app_both")[1]
sh("rm -f libmylib.a")
shared_build = sh("gcc -shared -fPIC mylib.c -o libmylib.so && gcc app.c -L. -lmylib -o app_dyn")
missing = sh("./app_dyn")
with_path = sh("LD_LIBRARY_PATH=. ./app_dyn")
ldd_dyn = sh("LD_LIBRARY_PATH=. ldd app_dyn")[1]
sh("gcc m2.c -o m -lm")
ldd_m = [" ".join(l.split()) for l in sh("ldd m")[1].splitlines()]
ldd_m = [l.split(" (0x")[0] for l in ldd_m]
sizes = sh("gcc m.c -o m_dyn && gcc -static m.c -o m_static && stat -c %s m_dyn m_static")[1].split()

checks += [
    # symbols
    (nm_table("a.o"), {"count": "D", "total": "B", "hidden": "d", "helper": "t", "twice": "T"}),
    (nm_table("b.o"), {"count": "U", "twice": "U", "printf": "U", "main": "T"}),
    (sh("gcc a.c b.c -o ab && ./ab")[1], "13\n"),
    (all(w in sh("gcc a.c b.c c.c -o abc")[2] for w in ["multiple definition of `count'", "first defined here"]), True),
    ("undefined reference to `helper'" in sh("gcc a.c b2.c -o ab2")[2], True), (sh("gcc -c b2.c")[0], 0),
    ("multiple definition of `helper'" in sh("gcc x.c y.c -o xy")[2], True),
    (sh("gcc xs.c ys.c -o xys && ./xys; echo $?")[1], "3\n"), (nm_table("xs.o") if sh("gcc -c xs.c")[0] == 0 else None, {"helper": "t", "fx": "T"}),
    # shared-libs
    ("undefined reference to `sqrt'" in sh("gcc m2.c -o m_nolm")[2], True), (sh("gcc -c m2.c -o m2.o")[0], 0),
    (sh("gcc m2.c -o m_lm -lm && ./m_lm 2")[1], "1.414214\n"),
    (static_rc[1], "49\n"), (shared_build[0], 0), ("libmylib.so" in both, True),
    (("error while loading shared libraries: libmylib.so: cannot open shared object file" in missing[2], missing[0]), (True, 127)),
    (with_path[1], "49\n"), ("libmylib.so => ./libmylib.so" in ldd_dyn, True),
    (ldd_m, ["linux-vdso.so.1", "libm.so.6 => /usr/lib/x86_64-linux-gnu/libm.so.6", "libc.so.6 => /usr/lib/x86_64-linux-gnu/libc.so.6", "/lib64/ld-linux-x86-64.so.2"]),
    (sizes, ["15952", "816880"]), (816880 / 15952 > 50, True),
    ("interpreter /lib64/ld-linux-x86-64.so.2" in sh("file m_dyn")[1], True),
    (sh("gcc dl.c -o dl && ./dl")[1], "49\n"),
    # file-io
    (sh("gcc fio.c -o fio && ./fio"), (0, "fd = 3\nn = 3\nn = 0\nbad = -1\n", "open: No such file or directory\n")),
    (sh("gcc cat.c -o cat && ./cat")[1], "hi\n"),
    (sh("gcc modes.c -o modes && ./modes && cat m.txt")[1], "xy"),
    (shm_out.split(), ["644", "600"]), (4 + 2, 6),
    (sh("gcc redir.c -o redir && ./redir > out.txt; cat out.txt"), (0, "out\n", "open: No such file or directory\n")),
    (sh("gcc pw.c -o pw && script -qc ./pw /dev/null")[1].replace("\r", ""), "a\nb\n"),
    (sh("./pw > pw.txt && cat pw.txt")[1], "b\na\n"),
    # structs
    (out(POINT + 'int main(void) { printf("%zu\\n", sizeof(struct point)); struct point p = {3, 4}; printf("%d\\n", p.x + p.y); p.y = 10; printf("%d\\n", p.x * p.y); return 0; }', body=False), "8\n7\n30\n"),
    (out('typedef struct {\n    char name[16];\n    int age;\n} Student;\nint main(void) { Student s = {"Ann", 20}; Student t = s; t.age = 99; t.name[0] = \'Z\'; printf("%s %d %s %d\\n", s.name, s.age, t.name, t.age); return 0; }', body=False), "Ann 20 Znn 99\n"),
    (out(POINT + 'int main(void) { struct point a = {1, 2}; struct point b = a; b.x = 9; printf("%d\\n", a.x); return 0; }', body=False), "1\n"),
    (out(POINT + MOVE + 'int main(void) { struct point q = {5, 0}; move_right(&q); move_right(&q); printf("%d\\n", q.x); return 0; }', body=False), "7\n"),
    (out(POINT + 'int main(void) { struct point q = {5, 6}; struct point *pp = &q; printf("%d %d\\n", pp->y, (*pp).y); return 0; }', body=False), "6 6\n"),
    ("error" in compile_err(POINT + "int main(void) { struct point q = {5, 6}; struct point *pp = &q; return pp.y; }\n"), True),
    ("error" in compile_err(POINT + "int main(void) { struct point q = {5, 6}; struct point *pp = &q; return *pp.y; }\n"), True),
    (out('#include <stddef.h>\nstruct rec { char c; int n; };\nstruct student { char name[16]; int age; double score; };\nint main(void) { printf("%zu %zu %zu %zu %zu\\n", sizeof(struct rec), offsetof(struct rec, n), sizeof(struct student), offsetof(struct student, age), offsetof(struct student, score)); return 0; }', body=False), "8 4 32 16 24\n"),
    (out('typedef struct { char name[16]; int age; } Student;\nint main(void) { Student class_[3] = {{"Ann", 20}, {"Bo", 23}, {"Cy", 17}};\n    Student *best = &class_[0];\n    for (int i = 1; i < 3; i++)\n        if (class_[i].age > best->age)\n            best = &class_[i];\n    printf("%s\\n", best->name); return 0; }', body=False), "Bo\n"),
    (out('typedef struct { char name[16]; int age; } Student;\nint main(void) {\n    Student c[3] = {{"Ann", 20}, {"Bo", 23}, {"Cy", 17}};\n    int total = 0;\n    for (int i = 0; i < 3; i++)\n        total += c[i].age;\n    printf("%d\\n", total / 3);\n    return 0;\n}', body=False), "20\n"),
    ("field ‘next’ has incomplete type" in compile_err("struct node { int value; struct node next; };\n"), True),
    (compile_err("struct node { int value; struct node *next; };\nint main(void) { return 0; }\n"), ""),
    (out('struct node { int value; struct node *next; };\nint main(void) { printf("%zu\\n", sizeof(struct node *)); return 0; }', body=False), "8\n"),
    # void-pointers
    (out('int x = 5;\nvoid *p = &x;\nprintf("%d\\n", *(int *)p);'), "5\n"),
    (all(w in compile_err('#include <stdio.h>\nint main(void) { int x = 5; void *p = &x; printf("%d\\n", *p); return 0; }\n') for w in ["dereferencing ‘void *’ pointer", "invalid use of void expression"]), True),
    (out(SWAP + 'int main(void) {\n    double x = 1.5, y = 4.0;\n    swap(&x, &y, sizeof x);\n    printf("%.1f\\n", x - y);\n    return 0;\n}', body=False), "2.5\n"),
    (out(SWAP + 'int main(void) { double x = 1.5, y = 4.0; swap(&x, &y, sizeof(int)); printf("%g %g\\n", x, y); return 0; }', body=False), "1.5 4\n"),
    (out(SWAP + '#include <math.h>\nint main(void) { double x = 1.5, y = 0.1; swap(&x, &y, sizeof(int)); printf("%d %d\\n", x != 1.5 && fabs(x - 1.5) < 1e-6, y != 0.1 && fabs(y - 0.1) < 1e-6); return 0; }', body=False), "1 1\n"),
    (out('double x = 1.0; printf("%zu\\n", sizeof x);'), "8\n"),
    ("assignment of read-only location ‘*p’" in compile_err("int main(void) { int x = 1; const int *p = &x; *p = 5; return 0; }\n"), True),
    ("assignment of read-only variable ‘q’" in compile_err("int main(void) { int x = 1, y = 2; int *const q = &x; q = &y; return 0; }\n"), True),
    (compile_err("int main(void) { int x = 1, y = 2; const int *p = &x; p = &y; int *const q = &x; *q = 5; x = 6; return *p; }\n"), ""),
    # function-pointers
    (out('int add(int a, int b) { return a + b; }\nint mul(int a, int b) { return a * b; }\nint main(void) { int (*op)(int, int) = add; printf("%d ", op(2, 3)); op = mul; printf("%d ", op(2, 3)); printf("%d\\n", op(4, 5) + add(1, 1)); return 0; }', body=False), "5 6 22\n"),
    (out(CMP_INT + 'int main(void) { int v[4] = {5, 2, 9, 1}; qsort(v, 4, sizeof v[0], cmp_int); for (int i = 0; i < 4; i++) printf("%d ", v[i]); qsort(v, 4, sizeof v[0], cmp_desc); for (int i = 0; i < 4; i++) printf("%d ", v[i]); return 0; }', body=False), "1 2 5 9 9 5 2 1 "),
    (out(CMP_STR + 'int main(void) { char *words[3] = {"pear", "apple", "fig"}; qsort(words, 3, sizeof words[0], cmp_str); printf("%s %s %s\\n", words[0], words[1], words[2]); return 0; }', body=False), "apple fig pear\n"),
    (out('void apply(int *a, int n, int (*f)(int)) {\n    for (int i = 0; i < n; i++)\n        a[i] = f(a[i]);\n}\nint square(int x) { return x * x; }\nint main(void) {\n    int v[3] = {1, 2, 3};\n    apply(v, 3, square);\n    printf("%d\\n", v[0] + v[1] + v[2]);\n    return 0;\n}', body=False), "14\n"),
    # machine-stack
    (asm_lines(SUB_C, "-O1 -fno-inline"), ["sub:", "movq %rdi, %rax", "subq %rsi, %rax", "ret", "twice_sub:", "call sub", "addq %rax, %rax", "ret"]),
    ("endbr64" in sh("gcc -S -O1 -o - asm.c")[1], True), ("call" in "\n".join(asm_lines(SUB_C, "-O1")), False),
    (1000 - 8, 992),
    (sh("gcc ov.c -o ov && script -qc ./ov /dev/null")[1].replace("\r", "").splitlines()[:2], ["a name that is much too long for sixteen", "*** stack smashing detected ***: terminated"]),
    (sh("./ov")[0], 134), (len("a name that is much too long for sixteen"), 40),
    (out('#include <stdint.h>\nuintptr_t g(void) { int z = 0; return (uintptr_t)&z; }\nuintptr_t f(void) { int y = 0; uintptr_t r = g(); return r + 0 * y; }\nint main(void) { int x = 0; printf("%d\\n", f() < (uintptr_t)&x); return 0; }', body=False, flags="-O0"), "1\n"),
    # growing-arrays
    (out(VEC + 'int main(void) { Vec v = {malloc(sizeof(int)), 0, 1}; for (int i = 0; i < 9; i++) push(&v, i * i); printf("%d %d %d %d\\n", reallocs, v.cap, v.size, v.data[8]); free(v.data); return 0; }', body=False), "4 16 9 64\n"),
    (sum(c for c in [1, 2, 4, 8]), 15), (sum(range(1, 9)), 36), (15 < 2 * 9, True), (9 * 9 / 2, 40.5),
    # linked-lists
    (out(NODE + 'int main(void) { struct node *head = NULL; head = push_front(head, 1); head = push_front(head, 2); head = push_front(head, 3);\n    int sum = 0;\n    for (struct node *p = head; p != NULL; p = p->next) { sum += p->value; printf("%d ", p->value); }\n    printf("%d\\n", sum);\n    struct node *prev = head, *cur = head->next; prev->next = cur->next; free(cur);\n    for (struct node *p = head; p != NULL; p = p->next) printf("%d ", p->value);\n    while (head != NULL) { struct node *next = head->next; free(head); head = next; }\n    return 0; }', body=False, flags="-fsanitize=address -g"), "3 2 1 6\n3 1 "),
    ("heap-use-after-free" in sh("cat > uaf.c <<'X'\n#include <stdlib.h>\n" + NODE + "int main(void) { struct node *head = push_front(push_front(NULL, 1), 2); struct node *p;\n    for (p = head; p != NULL; p = p->next) free(p);\n    return 0; }\nX\ngcc -g -fsanitize=address uaf.c -o uaf && ./uaf")[2], True),
    # allocator (the CS107-style teaching model, then glibc on this machine)
    (allocator_model(64, [10])[0], [(8, 16)]), (allocator_model(64, [10])[1][1], [24, 32, False]),
    (allocator_model(64, [10, 20])[0], [(8, 16), (32, 32)]),
    ((13 + 7) // 8 * 8, 16), ((20 + 7) // 8 * 8, 24), (25 % 8, 1), (25 - 25 % 8, 24), (16 + 8 + 16, 40),
    (out('#include <malloc.h>\nint main(void) { char *a = malloc(10), *b = malloc(10); printf("%ld %zu\\n", (long)(b - a), malloc_usable_size(a)); return 0; }', body=False), "32 24\n"),
    (sh("cat > df.c <<'X'\n#include <stdlib.h>\nint main(void) { char *a = malloc(10); free(a); free(a); return 0; }\nX\ngcc df.c -o df && ./df")[2].splitlines()[0], "free(): double free detected in tcache 2"),
    (sh("./df")[0], 134),
]
bad = [(i, got, want) for i, (got, want) in enumerate(checks) if got != want]
for i, got, want in bad:
    print(f"#{i}: got {got!r}, want {want!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
raise SystemExit(1 if bad else 0)
