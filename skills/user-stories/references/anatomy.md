# Story anatomy

## Contents
- Template
- Title, Statement
- Acceptance criteria (the Gherkin-like rules)
- Context, Open questions, Out of scope, Estimate, Links

## Template

~~~markdown
# <Title>

**As** <actor>, **I want** <need>, **so that** <purpose>.

**Epic:** <link or key>

## Acceptance criteria

```gherkin
Rule: <a business rule in plain language>

  Example: <a short name for this case>
    Given <the situation>
    When <the actor does something>
    Then <what the actor observes>
```

## Context
<optional: suggested command shapes, approach, prior decisions, links>

## Open questions
- <optional: anything unresolved>

## Out of scope
- <optional: excluded item> (lives in <link>)

**Estimate:** <optional: points, with a one-line reason>
**Links:** <sub-tasks, spikes, enablers>
~~~

## Title

Short, in the user's words, describing the outcome: "Back up my sessions", "See which sessions are
not backed up yet". Not a component ("Session sync service") or a task ("Implement ledger").

## Statement

See SKILL.md for the rules. Worked contrasts:

| Weak | Why | Better |
|---|---|---|
| As a user, I want sessions synced, so that they are synced | Generic actor; purpose restates need | As a multi-machine user, I want my sessions backed up to my registry, so that I can reach my history from any machine |
| As a developer, I want a chunked upload endpoint, so that uploads are efficient | The builder as actor; implementation as need | This is a sub-task (or part of a story), not a story |
| As any protostar user, I want to run `protostar sync`, so that ... | Exact command in the need | ... I want to run a CLI command that backs up my sessions, so that ... (command goes in Context) |
| As a multi-harness user, I want Codex sessions backed up and searchable | Two needs | Split: back up Codex sessions; search my sessions |

## Acceptance criteria

The criteria are the confirmation that the story is done. They use a Gherkin-like format because it
is easy to read and unambiguous; it is the ticket's format, not a statement about how the repo tests.
Whether a project turns them into executable tests (Reqnroll, Cucumber, or plain unit tests) is up to
that project and its owner. Write them so that conversion is possible, never assume it happens.

- **Group by `Rule:`.** Each rule is one business rule in plain language; each `Example:` under it is a
  concrete case. Many rules is a sign the story should be split by rule.
- **Actor's point of view.** Steps describe what the actor does and observes. "Then my session is
  listed with its project and machine", never "Then a row is written to the projection table".
- **Declarative, not scripted.** "When I back up my sessions from the CLI", not "When I type
  `protostar sync` and press Enter". Exact interface names appear only when the interface itself is
  the contract.
- **One behaviour per example.** One When, one main Then. A second When usually means a second
  example.
- **Concrete data.** Use real-looking values ("a 400 KB session from yesterday") so edge cases show.
- **Cover the unhappy paths that matter to the actor**: nothing to do, partial failure, offline,
  permission denied. Not every conceivable error.

## Context

Where opinion and implementation hints live: a suggested command shape, an API sketch, a prior
decision, a relevant file. Context informs the implementer but does not bind them; if something must
be binding, it belongs in the criteria.

## Open questions

Each question is something whose answer would change the story. Any open question means the story is
not ready to start. In "just do it" mode, every point you could not resolve goes here.

## Out of scope

What a reader might reasonably expect but is deliberately excluded, each pointing to where it lives
(another story, a later epic) or marked "not planned".

## Estimate

Only when the user wants one. Fibonacci points for complexity (rules, unknowns, moving parts,
integrations), not duration. One-line reason. 13+ suggests splitting.

## Links

The parent epic always. Sub-tasks, spikes, and enablers when they exist. Blocking relationships are
explicit links, not prose.
