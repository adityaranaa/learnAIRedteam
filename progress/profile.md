# Learner profile

## Background (self-reported, 2026-10-14)
- AI red teaming role at a startup; ~3–4 months hands-on chatbot testing
- Prior cybersecurity experience
- Lakera Agent Breaker: mostly through Level 3
- Prior notes (redprompter knowledge log, 2026-09-04): Giskard/PyRIT/garak shortlisted but not yet run;
  OWASP LLM Top 10 adopted for reporting

## Calibration: 4 dimensions (0–5, evidence-based only)
| Dimension | Level | Evidence | Updated |
|---|---|---|---|
| Technical understanding | 2 | Finds indirect injection paths; confuses refusal source with enforcement locus (Q1-Q3) | 2026-10-15 |
| Independent attack design | 2 | Good vector instincts; hypotheses not yet falsifiable, no baseline (Q2) | 2026-10-15 |
| Implementation & automation | ? | no tool running yet (per log) | 2026-10-14 |
| Research & evidence quality | 1-2 | Concludes from one explanation; observed vs assumed mixed (Q1, Q3) | 2026-10-15 |

Scale: 1 = can follow a guide · 2 = applies known techniques to familiar targets ·
3 = independently maps unfamiliar systems and designs valid tests · 4 = finds non-obvious
cross-component bugs, proves impact, builds reusable tooling · 5 = produces original, defensible research.

## Skills demonstrated independently
_(only things done without hints)_

## Repeated mistakes / knowledge gaps
1. Treats a refusal (or a missing result) as proof of where a control lives (Q1, Q2, Q3)
2. Mixes observed facts with assumptions
3. Changes more than one variable per test; no baseline
4. Stops at the first plausible explanation instead of listing rivals
5. Reads evidence from the chat reply instead of a system of record

## Next recommended exercises
- Finish diagnostic Q4 (root cause, mitigation, regression test)
- Then: build a small local mock agent with a prompt-only vs code-enforced tool, and a harness that tells them apart
