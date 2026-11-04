"""Trace a small Python program line by line for the game's `trace` sim.

usage: python -I scripts/lib/pytrace.py < program.json   ({"code": "...", "stdin": "..."})
prints {"steps": [{"line", "frame", "func", "vars", "out", "stack"?}...], "error": null|str}

Each step is the state *before* `line` runs: the variables of the frame that is about to run it
(repr strings) and everything printed so far. The final step (line = null) is the state after the
program ends. `stack` (only while a function is running) is the call stack, outermost first, e.g.
["<module>", "sum_squares", "square"]. Uses sys.settrace; only frames compiled from the traced code
are recorded.

Default reprs carry a memory address ("<__main__.Student object at 0x00000204A8AE6E40>") that changes
on every run, which would make every build of the game differ. Such addresses are replaced, in order of
first appearance, by fixed stand-ins (0x7f0000001000, 0x7f0000001040, ...): the same object keeps the
same address throughout the trace, and different objects get different ones.
"""
import io
import json
import re
import sys

MAX_STEPS = 400


def main():
    req = json.load(sys.stdin)
    code = req["code"]
    out = io.StringIO()
    steps = []
    frame_ids = {}

    def snap(frame):
        names = {k: v for k, v in frame.f_locals.items() if not k.startswith("__") and not callable(v) and not isinstance(v, type(sys))}
        return {k: repr(v) for k, v in names.items()}

    def stack_of(frame):
        names = []
        while frame is not None:
            if frame.f_code.co_filename == "<game>":
                names.append(frame.f_code.co_name)
            frame = frame.f_back
        return names[::-1]

    def step(frame, **extra):
        st = {"line": frame.f_lineno, "frame": frame_ids[id(frame)], "func": frame.f_code.co_name, "vars": snap(frame), "out": out.getvalue(), **extra}
        stack = stack_of(frame)
        if len(stack) > 1:
            st["stack"] = stack
        return st

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<game>":
            return tracer
        frame_ids.setdefault(id(frame), len(frame_ids))
        if event == "line":
            if len(steps) >= MAX_STEPS:
                raise RuntimeError("too many steps")
            steps.append(step(frame))
        elif event == "return":
            steps.append(step(frame, line=None, ret=repr(arg)))
        return tracer

    compiled = compile(code, "<game>", "exec")
    glb = {"__name__": "__main__", "__builtins__": __builtins__}
    old_out, old_in = sys.stdout, sys.stdin
    sys.stdout, sys.stdin = out, io.StringIO(req.get("stdin", ""))
    error = None
    try:
        sys.settrace(tracer)
        exec(compiled, glb)
    except Exception as e:  # the trace still shows the steps up to the error
        error = f"{type(e).__name__}: {e}"
    finally:
        sys.settrace(None)
        sys.stdout, sys.stdin = old_out, old_in
    text = json.dumps({"steps": steps, "error": error, "out": out.getvalue()}, ensure_ascii=False)
    seen = {}
    text = re.sub(r" at 0x[0-9A-Fa-f]+", lambda m: seen.setdefault(m.group(0), f" at 0x{0x7f0000001000 + 0x40 * len(seen):x}"), text)
    print(text)


if __name__ == "__main__":
    main()
