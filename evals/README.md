# Evals

A small, dependency-free harness that follows the
[agentskills.io guide to evaluating skills](https://agentskills.io/skill-creation/evaluating-skills):
run each case with and without the skill, grade assertions with evidence, aggregate, review, iterate.

It runs **locally only**. Every model call (the agent under test, the simulated user, the grader)
goes through the `claude` CLI on the owner's Claude login. Nothing runs in CI.

## Layout

| Path | What |
|---|---|
| `skills/<skill>/evals/evals.json` | The cases: prompt, expected output, fixture files, assertions |
| `skills/<skill>/evals/files/` | Fixture repos copied into each run's working directory |
| `evals/personas/owner.md` | The simulated user: answers the agent's questions as the owner would |
| `evals/harness/` | `run.py`, `grade.py`, `aggregate.py`, and scripted `checks.py` |
| `workspace/<skill>/iteration-N/` | Results (gitignored): `eval-<name>/<config>/run-<n>/` with `outputs/`, `timing.json`, `grading.json`; plus `benchmark.json` and `benchmark.md` |

## Running

```bash
python3 -I evals/harness/run.py user-stories --iteration 1        # all cases, both configs
python3 -I evals/harness/grade.py user-stories --iteration 1
python3 -I evals/harness/aggregate.py user-stories --iteration 1  # prints benchmark.md
```

`run.py` runs only cases marked `"validated": true` (the owner has confirmed the case and its
expected behaviour), `runs_per_eval` times each (3 by default). It takes `--eval NAME` and
`--config with_skill|without_skill` (repeatable) to run a subset, `--runs N` to override the count,
and `--include-unvalidated` to try draft cases.

## How a run works

1. The case's fixture is copied into a fresh temp directory outside any repo. For `with_skill`, the
   skill is copied into its `.claude/skills/`.
2. The agent runs with `--setting-sources project`, so the owner's global skills, plugins, and
   CLAUDE.md never load. The only difference between the two configs is the skill.
3. After each agent turn the persona reads the conversation and either replies or declares the work
   done. The same persona answers both configs. It supplies product knowledge but never coaches on
   format, so it cannot rescue a weak baseline.
4. Up to five agent turns. Skill invocations are read from the session transcript Claude Code saves.

## Assertions

Plain strings are graded by a model that must quote evidence for every PASS. An assertion written as
`{"text": "...", "script": "<check>"}` is checked in code by the named function in `checks.py`;
prefer that for anything mechanical. Per the guide, revisit assertions after each iteration: drop
ones that pass in both configs, fix ones that fail in both.
