# learnAIRedteam: personal AI red teaming workspace

Goal: get faster and more independent at **finding, validating, explaining, and helping remediate**
weaknesses in AI agents. This is not a tutorial checklist.

## Layout
| Path | What lives there |
|---|---|
| `progress/profile.md` | Current level on 4 dimensions, evidence, gaps, repeated mistakes |
| `sessions/YYYY-MM-DD.md` | One log per study session (objective → experiment → evidence → next) |
| `diagnostic/` | Calibration scenarios and answers |
| `labs/` | Local, reproducible vulnerable systems to attack (all synthetic) |
| `tools/` | Reusable harnesses, inventory scripts, evaluators, regression suites |
| `research/questions.md` | Open hypotheses, prior-work checks, novelty status |

## Investigation method (the loop every exercise trains)
1. Map the system: observed facts vs assumptions
2. Assets, trust boundaries, security invariants, authorization decisions
3. Specific attack hypothesis
4. Minimum experiment
5. Predict outcomes *before* running
6. Run, in authorized environments only
7. Evidence + alternative explanations
8. Exploitability, impact, reliability, limitations
9. Architectural root cause
10. Mitigation, and test that it works
11. Reproducible regression test
12. Write it up

Finding ladder: prompt compliance → information exposure → unauthorized action → demonstrated security impact.
A weird model response is not a vulnerability until it climbs this ladder.

## Data-handling rule
No employer or customer data, credentials, system prompts, or proprietary artifacts in this repo.
Use sanitized reproductions in `labs/` instead.
