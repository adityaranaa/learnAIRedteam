# Breaker: local prompt-injection practice range

Five levels, Lakera-style, fully local. All secrets and targets are synthetic.

    cd labs/breaker
    python3 game.py                 # list levels + progress
    python3 game.py play 1          # play a level  (add --debug to see which gate fired)
    python3 game.py stats           # attempts per level
    python3 game.py reset           # clear progress + attempt log (keeps secrets)
    python3 -m unittest discover -s tests

Levels 1-4: extract the password, then `/guess WORD`. Level 5: agent level, win is judged from the tool-call log.

## Backends
- **mock** (default, offline): keyword-driven stand-in that models *susceptibility*, not intelligence. Good for learning gate-by-gate
  reasoning. It will NOT behave like a real model, so skills learned here must be re-tested on real targets.
- **anthropic**: set `ANTHROPIC_API_KEY` (or `--backend anthropic`); `BREAKER_MODEL` overrides the model. Written against the
  Messages API but not run offline, so treat as untested. A real model may be far harder or far easier than the mock on some levels.

## How to use it (this is the actual training)
Before every attempt, write one line: **hypothesis** (which gate, what I expect) → **prediction** → send. After, use `--debug` to compare.
When you clear a level, write: which gate did I beat, what is the root cause, what fix stops it, what regression test proves it.
Every attempt is logged to `.state/attempts.jsonl` for later analysis.

## Don't peek
`tests/test_breaker.py::Solvable` contains reference solutions. Secrets are random per install (`.state/secrets.json`).
