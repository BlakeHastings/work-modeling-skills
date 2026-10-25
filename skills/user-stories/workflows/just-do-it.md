# Just-do-it workflow

The user, or another agent, wants the story written with no back-and-forth. Write the best version you
can and make every gap visible instead of asking about it.

```
Progress:
- [ ] 1. Gather what is known, from the request and every source the tools reach
- [ ] 2. Route the item and draft the story
- [ ] 3. Run the checks
- [ ] 4. Record every gap in the story itself
```

1. **Gather** following "Gather context before asking" in SKILL.md, harder than usual since you will
   not ask: search the tracker for an existing or duplicate story, read every ticket or decision
   referenced, and mine every source the available tools reach. If a matching story exists, update it
   (or say why not) rather than create a duplicate. Where a source contradicts the request, follow the
   request and record the conflict in Open questions.
2. **Route and draft** as in SKILL.md, in the template from `references/anatomy.md`.
3. **Check** against `references/checks.md` and fix everything you can without the user.
4. **Record gaps.** Do not stop to ask:
   - Each assumption you made goes in **Context**, marked as an assumption.
   - Each thing only the user can decide goes in **Open questions**, with your recommended answer.
   - If you could not pin the actor, use the best-fitting archetype and say so in Open questions.

Not asking is not the same as hiding. A reader must be able to see, from the story alone, everything
you were unsure of. If there are open questions, end with one line saying the story is not ready
until they are answered.
