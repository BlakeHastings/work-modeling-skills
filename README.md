# work-modeling-skills

Agent Skills for modeling work from the point of view of the people who experience it. An
opinionated method, not a survey of agile practice: one way to write stories, one way to write
acceptance criteria, one way to route technical work.

The work model is three levels, **Epic > Story > Sub-task**, plus **Spike** and **Enabler** as typed
items that link to the stories they serve.

## Skills

| Skill | Status | What it does |
|---|---|---|
| [`user-stories`](skills/user-stories/SKILL.md) | Draft | Write, review, and rewrite stories: "As \<actor\>, I want \<need\>, so that \<purpose\>", Gherkin-like criteria grouped by `Rule:`, routing to sub-task, enabler, or spike. Guided, draft-and-confirm, and just-do-it workflows |

Planned: epics, story splitting, spikes, and mapping to Jira and GitHub issues.

## Install

As a Claude Code plugin:

```
/plugin marketplace add BlakeHastings/work-modeling-skills
/plugin install work-modeling@work-modeling-skills
```

For development, symlink a skill into your global skills folder so edits are live:

```bash
ln -s "$PWD/skills/user-stories" ~/.claude/skills/user-stories
```

Do not do both on one machine, or the skill loads twice.

## Evals

Skills are tested against realistic prompts, with and without the skill, and graded on the method's
rules. Evals run locally only. See `evals/` once it lands.

## License

MIT
