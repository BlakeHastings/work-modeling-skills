# Story checks

Run every check before handing a story back. Each has the failure it catches and the fix.

## INVEST

| Check | Ask | Typical fix |
|---|---|---|
| Independent | Can it be built and delivered without another story landing first? | Make the dependency an explicit blocking link, or move the shared part into the first story |
| Negotiable | Does it leave room for how it is built? | Move commands, schemas, and approach into Context |
| Valuable | Would the actor notice and care if it shipped alone? | If not, it is a task: merge it into a story that is valuable, or make it a sub-task |
| Estimable | Could someone judge its complexity? | Unknowns go in Open questions; big unknowns become a spike |
| Small | Can it be demoed in one sitting? | Split it |
| Testable | Do the criteria prove it is done? | Write or sharpen the Gherkin |

"Valuable" fails most often. Fix it before checking size: splitting a story that has no value just
produces smaller items with no value.

## Smells

**Generic actor.** "As a user". Fix: name the archetype, or write "any <product> user" deliberately.

**Builder as actor.** "As the developer implementing X". Fix: it is a sub-task or part of a story.
(A developer who *uses* a developer tool is a valid actor.)

**Implementation in the need.** A command, flag, endpoint, table, or library in the "I want".
Fix: describe the capability ("a CLI command that ..."); put the specific shape in Context.

**Purpose restates the need.** "I want X so that X happens". Fix: ask why the actor wants X; the
answer is the purpose.

**Two needs.** "And" in the need. Fix: two stories, unless one is meaningless without the other.

**Technical layer as story.** "Sessions API", "Database schema for skills". Fix: find the user-visible
slice that needs it and fold the layer into that story.

**Internal criteria.** "Then a record is stored". Fix: what does the actor see that proves it?

**Scripted criteria.** "When I click Save" / "When I type `foo --bar`". Fix: declarative step
("When I save my changes"), unless the interface is the contract.

**Leans on another story.** "Same as the backup story but for Codex". Fix: spell the behaviour out.

**Hidden unknowns.** The story reads finished but the conversation left questions open. Fix: list them
in Open questions.

**Spike with no artifact.** "Investigate X". Fix: name the artifact it produces and the questions it
answers.

**Enabler that could be a story.** Cross-cutting work split off before trying to deliver it inside
the first story that needs it. Fix: try folding it in first; split only when that blows the story's
scope or blocks other stories on non-user-facing work.

**Sub-tasks as a to-do list.** Sub-tasks created for every step. Fix: keep the work in the story;
sub-task only for parallel or separately delivered work.
