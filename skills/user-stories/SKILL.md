---
name: user-stories
description: >-
  Writes, reviews, and rewrites user stories to an opinionated house method: "As <actor>, I want
  <need>, so that <purpose>", with Gherkin-like acceptance criteria grouped by Rule. Use whenever the
  user wants to write a story, turn an idea, feature request, or brain dump into a story, review or
  critique a story or backlog, decide whether work is a story, sub-task, enabler, or spike, or
  estimate a story, even if they don't say "user story" (e.g. "make a ticket for this", "write this
  up for the backlog", "is this ticket any good"). Supports a guided brain-dump-and-grill workflow, a
  draft-and-confirm workflow, and a just-do-it workflow. Work model is Epic > Story > Sub-task.
---

# User stories

A story is a change in the product that a named actor can observe, small enough to demo in one
sitting. It is a pointer to a shared understanding, not a specification: it holds enough to remind
everyone what was agreed, and its acceptance criteria are how that agreement is confirmed.

The work model has three levels, **Epic > Story > Sub-task**, plus two typed items, **Spike** and
**Enabler**, that link to the stories they serve.

This file is the method. How to run a session with the user is in the workflow files (see the end).

## The statement

```
As <actor>, I want <need>, so that <purpose>.
```

- **Actor**: who experiences the change. Every story has one, because it decides who the change is
  for, who to test as, and who is left out. Use the most specific archetype that fits. "Any
  <product> user" is valid only when the change genuinely matters equally to everyone; reaching for
  it when a narrower archetype fits hides who the story is really for.
- **Need**: what the actor wants, in their words, free of implementation. "Run a CLI command that
  backs up all my sessions", not "run `protostar sync --all`". Naming the mechanism here fixes the
  design before anyone has thought about it, and makes the story wrong the moment the design changes.
- **Purpose**: why they care. It must say something the need does not. Test: delete the "I want"
  clause; the "so that" should still explain why anyone would care. A purpose that restates the need
  gives the implementer nothing to make trade-offs against.
- **One need per story.** An "and" in the need is usually two stories that will want to ship, slip, or
  be cut separately.

## Anatomy

| Field | Required | Holds |
|---|---|---|
| Title | yes | Short, in the user's words, naming the outcome ("Back up my sessions") |
| Statement | yes | The As / I want / so that line |
| Acceptance criteria | yes | Gherkin-like, grouped by `Rule:`, from the actor's point of view |
| Context | no | Suggested shape and opinionated detail: command names, approach, prior decisions |
| Open questions | no | Anything unresolved; any present means the story is not ready |
| Out of scope | no | What is deliberately excluded, and where it lives instead |
| Estimate | no | Fibonacci points, only if the user wants estimates |
| Links | yes | Parent epic; any sub-tasks, spikes, enablers |

The Gherkin-like criteria are the ticket's format, chosen because they are easy to read and leave
little room for misunderstanding. A project may turn them into executable tests; nothing here assumes
it will, or how it would.

Two rules cut across fields:
- **Commands, endpoints, and UI element names stay out of the statement and criteria** and go in
  Context, unless the interface itself is the contract (a documented public API). That keeps the
  story true while the implementation moves. If the user explicitly asks for one in the statement or
  criteria, do what they asked, then tell them briefly why it is a concern (it fixes the design and
  goes stale when the interface changes) and offer to move it to Context. Their instruction wins; your
  job is to make the trade-off visible, not to override it.
- **Every story reads on its own.** No "same as the backup story". Stories get read one at a time, by
  people and agents who have not seen the others.

Field guidance, criteria rules, and the template: [references/anatomy.md](references/anatomy.md).

## Is it really a story?

Decide what the item is before writing it:

1. **The actor can observe the change** → a **story**. Its technical work is part of the story by
   default; a story that needs a table and an endpoint still gets one story.
2. **Work inside a story that must run in parallel or ship separately** → a **sub-task** of that
   story. Sub-tasks exist for those reasons, not to list steps.
3. **Cross-cutting technical work** (CI, an upgrade, a wide refactor, shared infrastructure) → first
   try to deliver it inside the first story that needs it. Split it into an **enabler** only when
   that would blow the story's scope, or would block other stories on work no user sees. The enabler
   names the stories it blocks and carries objective checks.
4. **The output is knowledge** → a **spike**. A spike produces a **persistent artifact** (a doc, ADR,
   comparison, prototype write-up) that answers its question and questions like it later; learning
   that lives only in someone's head is lost by the next story. Its criteria describe the artifact.
   When it closes, update or split the story it served.
5. **Too big to demo in one sitting, or several distinct outcomes** → an **epic**. Capture what the
   user asked for as the epic, in their words, so the intent is not lost. Say plainly that it is too
   big for one story and why: the distinct outcomes, and, if it helps, a rough complexity estimate
   (13 points or more) as evidence, without asking the user to adopt estimates. List the candidate
   stories one line each, noting any that already exist, and offer to break it down. Do not write a
   story that bundles the outcomes back together ("do all of it in one step"): that story is the
   epic again, and it ships, slips, and gets cut as one.

## Actors

- Use any archetype data the available tools can find (an actors, personas, or archetypes doc in the
  repo, a docs or wiki page, the tracker). Otherwise ask the user who the actor is.
- Where archetypes are stored is the user's choice. If they want them kept, suggest a place and create
  it only with their permission.
- Archetypes describe how someone uses the product ("multi-machine user"), not invented demographics.
- **"Developer" is a valid archetype for developer tools.** The problem is the *builder* as actor:
  "as the developer implementing the ledger" is a sub-task; "as a developer using two harnesses" is a
  user.

## Quality checks

Run these before handing any story back. The full list, each with the failure and its fix, is in
[references/checks.md](references/checks.md). The ones that catch most problems:

- Generic actor ("as a user"), or the builder as actor.
- Implementation in the need (a command, endpoint, table, or library).
- Purpose that restates the need.
- "And" in the need.
- A technical layer posing as a story ("API for sessions").
- Criteria about internals ("a row is inserted") instead of what the actor sees.
- Criteria scripted against UI or exact commands instead of declarative steps.
- Leans on another story to be understood.

If a problem remains because the user chose not to resolve it, it goes in Open questions. A weak story
that looks finished is worse than an honest one with questions, because the next reader trusts it.

## Estimation

Optional, and the user's call. If they do not want estimates, skip it.

When asked, recommend Fibonacci points (1, 2, 3, 5, 8, 13, 21) based on **complexity, not time**: the
number of rules, unknowns, moving parts, and integration points. Give the number and a one-line
reason; the user decides. At 13 or more, say the story probably wants splitting.

## Gather context before asking

The user's time is the scarcest input. Before asking anything, use whatever tools this session has
(skills, MCP servers, CLIs, the codebase, memory) to gather the context relevant to the story, and
ask only about what none of them can answer. Which tools exist varies, so none is assumed, and what
is worth looking at depends on the story.

Ways this tends to pay off, as examples rather than a sequence:

- **An existing story.** The tracker (a Jira skill or MCP, `gh` for GitHub issues) may already hold
  this story, a duplicate, or its epic. If so, the job is probably to refine that one, not create a
  second.
- **What the user referred to.** A ticket, "the sync story", an earlier decision, how something works
  today: read the source rather than relying on the paraphrase. If it disagrees with what they said,
  point that out instead of silently picking one.
- **Who the actors are.** Archetype or persona docs, wherever they live.
- **How it works now.** The code, docs, ADRs, or a wiki, to ground the need and the rules in reality.

When you do ask, mention what you already found, so the user can see it was checked and correct it if
it is wrong.

## Every question carries a recommendation

Any question you put to the user comes with your recommended answer, worded so "yes" accepts it. That
holds at every point: the first round, follow-ups after a draft, offers ("want me to split this?"),
and Open questions written into a ticket. For a fact you could not find, give your best guess. A
bare question hands the user the thinking; a recommendation lets them decide in one word, and shows
what you would do if they say nothing.

## Deliver what was asked

Write the item the user asked for. Gathering context often turns up related problems: a weak
neighbouring ticket, a missing spike, an epic that should exist. Mention each in one line, and write
it out only when the user asks for it. An answer like "your call" or "sure, whatever" to an offer is
not a request; leave the extra as a suggestion. Unrequested tickets cost the user review time and bury
the one they wanted.

## Workflows

Pick the workflow from the request and say which in one line, so the user can switch:

| Workflow | Use when | File |
|---|---|---|
| **Guided** | The user has an idea but it is raw, or asks for help thinking it through | [workflows/guided.md](workflows/guided.md) |
| **Draft and confirm** | Actor, need, and purpose are given or clearly inferable. The default | [workflows/draft-and-confirm.md](workflows/draft-and-confirm.md) |
| **Just do it** | "Just write it", "no questions", batch work, or another agent asking | [workflows/just-do-it.md](workflows/just-do-it.md) |
| **Review** | Critiquing or rewriting existing stories, one or a backlog | [workflows/review.md](workflows/review.md) |

Output is tracker-neutral markdown in the template from `references/anatomy.md`. Creating issues in
Jira or GitHub is a separate step (the `jira-api` skill, or `gh`).

Worked stories, before-and-after rewrites, and routing examples:
[examples/examples.md](examples/examples.md).
