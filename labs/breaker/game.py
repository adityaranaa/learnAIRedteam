#!/usr/bin/env python3
"""Local prompt-injection practice range. Usage: game.py [list|play N|stats|reset] [--debug] [--backend mock|anthropic]"""
import json
import sys
import time

import backends
import levels as L

STATE = L.STATE


def jload(name, default):
    p = STATE / name
    return json.loads(p.read_text()) if p.exists() else default


def log(entry):
    STATE.mkdir(parents=True, exist_ok=True)
    with open(STATE / "attempts.jsonl", "a") as f:
        f.write(json.dumps({"ts": int(time.time()), **entry}) + "\n")


class ChatSession:
    def __init__(self, level, backend):
        self.level, self.backend, self.msgs, self.replies = level, backend, [], []

    def turn(self, text):
        lv, trace = self.level, []
        why = lv.input_filter(text)
        trace.append(("input_filter", f"BLOCKED: {why}" if why else "pass"))
        if why:
            return "[Message blocked by input filter]", trace
        self.msgs.append({"role": "user", "content": text})
        reply = self.backend.chat(lv.system, self.msgs, lv.gullibility)
        trace.append(("model", reply))
        self.msgs.append({"role": "assistant", "content": reply})
        why = lv.output_filter(reply, self.replies)
        self.replies.append(reply)
        trace.append(("output_filter", f"BLOCKED: {why}" if why else "pass"))
        return ("[Response withheld by output filter]" if why else reply), trace


def submit_document(level, backend, doc):
    """Agent level. Returns (shown, trace, won). Win comes from the tool-call log."""
    trace = []
    why = level.input_filter(doc)
    trace.append(("input_filter", f"BLOCKED: {why}" if why else "pass"))
    if why:
        return "[Document rejected by input filter]", trace, False
    summary, calls = backend.agent(level.system, doc)
    trace.append(("model", summary))
    won, lines = False, [f"Summary: {summary}"]
    for c in calls:
        ok = L.recipient_allowed(c.get("to", ""))
        domain = c.get("to", "").rsplit("@", 1)[-1].lower()
        leaked = L.norm(level.secret) in L.norm(c.get("body", ""))
        trace.append(("tool_policy", f"send_email to={c.get('to')} -> {'ALLOWED' if ok else 'DENIED'}"))
        lines.append(f"TOOL LOG: send_email(to={c.get('to')!r}) {'executed' if ok else 'denied by policy'}")
        won = won or (ok and leaked and domain != "corp.test")
    return "\n".join(lines), trace, won


def read_doc():
    print("Paste the document. Finish with a line containing only END.")
    lines = []
    while True:
        try:
            ln = input()
        except EOFError:
            break
        if ln.strip() == "END":
            break
        lines.append(ln)
    return "\n".join(lines)


def mark_solved(n):
    prog = jload("progress.json", {"solved": []})
    if n not in prog["solved"]:
        prog["solved"].append(n)
    (STATE / "progress.json").write_text(json.dumps(prog))


def play(n, backend, debug):
    lv = L.get_levels()[n]
    sess, hint_i = ChatSession(lv, backend), 0
    print(f"\n=== Level {n}: {lv.title} ===\nGoal: {lv.goal}")
    print("Write your hypothesis and predicted outcome BEFORE each attempt.")
    print("Commands: /hint /debug /goal /quit" + ("" if lv.kind == "agent" else " /guess WORD") + "\n")
    while True:
        try:
            line = input("you> ").strip()
        except EOFError:
            return
        if not line:
            continue
        if line == "/quit":
            return
        if line == "/goal":
            print(lv.goal)
        elif line == "/debug":
            debug = not debug
            print("debug", "on" if debug else "off")
        elif line == "/hint":
            print("hint:", lv.hints[min(hint_i, len(lv.hints) - 1)])
            hint_i += 1
        elif line.startswith("/guess") and lv.kind == "chat":
            ok = L.norm(line[6:]) == L.norm(lv.secret)
            log({"level": n, "guess": line[6:].strip(), "correct": ok})
            if ok:
                mark_solved(n)
                print(f"Correct. Level {n} cleared. Now write down: which gate did you beat, and what fix would stop you?")
                return
            print("Wrong.")
        elif lv.kind == "agent":
            doc = line + "\n" + read_doc()
            shown, trace, won = submit_document(lv, backend, doc)
            log({"level": n, "input": doc, "trace": trace, "won": won})
            print(shown)
            if debug:
                for k, v in trace:
                    print(f"  [{k}] {v}")
            if won:
                mark_solved(n)
                print("Exfiltration confirmed in the tool log. Level 5 cleared. Root cause? Mitigation?")
                return
        else:
            shown, trace = sess.turn(line)
            log({"level": n, "input": line, "trace": trace})
            print("bot>", shown)
            if debug:
                for k, v in trace:
                    print(f"  [{k}] {v}")


def main(argv):
    debug = "--debug" in argv
    backend_name = argv[argv.index("--backend") + 1] if "--backend" in argv else None
    args = [a for a in argv if not a.startswith("--") and a not in ("mock", "anthropic")]
    cmd = args[0] if args else "list"
    if cmd == "reset":
        for f in ("progress.json", "attempts.jsonl"):
            (STATE / f).unlink(missing_ok=True)
        print("progress and attempt log cleared (secrets kept)")
    elif cmd == "stats":
        rows = [json.loads(x) for x in (STATE / "attempts.jsonl").read_text().splitlines()] if (STATE / "attempts.jsonl").exists() else []
        for n in range(1, 6):
            r = [x for x in rows if x["level"] == n]
            print(f"level {n}: {len(r)} attempts")
    elif cmd == "play":
        play(int(args[1]), backends.pick(backend_name), debug)
    else:
        solved = jload("progress.json", {"solved": []})["solved"]
        for n, lv in L.get_levels().items():
            print(f"[{'x' if n in solved else ' '}] {n}. {lv.title}: {lv.goal}")
        print(f"\nbackend: {backends.pick(backend_name).name}   (play N | stats | reset | --debug)")


if __name__ == "__main__":
    main(sys.argv[1:])
