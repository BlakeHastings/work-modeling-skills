# AGENTS.md

This repo packages an opinionated work-modeling method (stories, and later epics, splitting, spikes)
as Agent Skills. Human-facing overview is in `README.md`.

## Invariants

- **Skills live in `skills/<name>/`.** Each has a `SKILL.md`; detail goes in `references/`,
  `workflows/`, and `examples/`, each linked directly from `SKILL.md` (one level deep).
- **`SKILL.md` frontmatter uses only Agent Skills spec fields**: `name`, `description`, `license`,
  `compatibility`, `metadata`, `allowed-tools`. Claude-specific values go under `metadata`.
- **A `SKILL.md` body stays under 500 lines.** Files over 100 lines get a contents list.
- **Rules explain why.** Prefer a reason over an all-caps MUST; the reader is a capable model.
- **No em dashes or spaced en dashes** anywhere: skills, docs, commits.
- **Bump `version` in `.claude-plugin/plugin.json`** when a skill's behaviour changes.
- **Evals run locally only**, never in CI: they drive real agent sessions on the owner's login.

## Writing examples

Examples must be concrete. Use the protostar project (a CLI and registry that back up agent sessions,
skills, and configuration) as the running example domain so examples stay consistent across skills.
