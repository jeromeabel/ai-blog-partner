## 4. The Opportunities

Let’s look at where this actually gets interesting.

### Prototyping in YOLO Mode

Vibe-coding gets a bad rap, but "YOLO mode"—accepting AI output just because it looks "okay"—has actual utility when you're just exploring.

* **UI/UX Exploration:** Using tools like Figma Make to spin up five variations of a feature in an hour. It’s a "variations" app with a toggle. It’s not production-ready, but it’s a tangible prototype to show the team before anyone touches the real codebase.
* **Contextual Specs:** I’ve started adding "orchestrator" features directly in preview branches just to see them run. Testing a feature in its real environment helps me write better specs later. Once the experiment works, I ask for an implementation plan, tweak it to keep my core logic, and then rebuild properly. The "optimization" phase is much faster because the plan is already battle-tested.
* **The Ubiquitous Language:** This is huge for non-devs. When business stakeholders can turn an idea into a functional (if messy) internal tool or report, they start to understand the friction of software. Seeing "Spec to Code" in real-time is a learning loop. It forces everyone to be explicit, which is hard.

### The Continuous Workflow Audit

AI adoption forces you to audit your habits. To figure out where an LLM actually fits, you have to break your day into micro-tasks and identify which ones are implicit or just "organic" noise.

I’ve started thinking of my workflow like Martin Fowler’s *Refactoring* book—where every move has a name. It’s like sports: once you name the movement, you can optimize the sequence. This consistent introspection creates a loop of small, compounding improvements to how you and your team actually interact.

### Living Documentation

> In my experience, docs have three main failure modes: They don't exist, They can't be trusted, They can't be found. — Luca Rossi & Dennis Pilarinos [^14]

We all know the drill: documentation is painful, it’s usually obsolete by the time it’s read, and developers would rather just "read the code." We treat docs like noise because they often are.

AI changes the math. Generating docstrings or Mermaid diagrams to map how functions communicate is now a low-effort task. It provides a map of the codebase before you start digging.

The debate over "too much documentation" is still there, but the cost of keeping it updated has plummeted. Because AI agents *need* this context to be useful, documentation has become a "living" requirement. It’s no longer just for onboarding; it’s the source of truth that keeps the LLM from hallucinating.

### Specs as the Fundamental Unit

![[pyramid-of-docs-luca-rossi.png]]

Our roles are shifting toward "orchestrator", managing coding agents. You’re a Product Manager for your own code. In this world, the **specification file** is the most important asset you own.

Starting with a "plan" file is now standard practice. A single feature might involve two or three files: the User Story, the Brainstorming Plan, and the Implementation Tasks. This creates a paper trail that keeps the LLM on track even when you have to clear the context or pick up work the next day.

![[spec-kit-dev-workflow.png]]

Some frameworks, like spec-kit, take this further, producing four or more files to make every detail explicit for the LLM. [^16]

It’s a bit ironic if the future of high-end engineering might just be managing a bunch of Markdown files

> - Specifications, not prompts or code, are becoming the fundamental unit of programming. (The New Code — Sean Grove, OpenAI [^12])
> - Coding is an incredible skill an asset. But it's not the end goal. Engineering is the precise exploration (by humans) of software solutions to humans problems. 
> - The Code is 10-20% of your impact; The other 80-90% is the structured communication (talk, understand, distill, ideate, plan, share, translate, test, verify)
> - A written specification is what **enables** you to **align humans** - it's the artifact that you discuss, debate, refer to, and sync on.

When we start a feature by talking about implementation details, we lose the "Why." AI forces us back to the high-level analysis. If you can’t explain it clearly in a spec, the agent will fail.

As Vishal Kapour noted [^17], agents expose how "underbaked" your thinking actually is. If the agent does something stupid, it’s usually because you didn’t actually know what you wanted.

Because AI is an amplifier, the leverage is at the start of the chain. As Dexter Horthy points out: one bad line in a plan can result in 100 lines of garbage code. [^18]

![[human-leverage-dexter-horthy.png]]

### Redefining Interactions

AI reshapes how we interact with our tools. The shift isn't just technical; it’s relational. We’re talking to machines—through text, voice, and images—and conversation has become the work.

This feels natural. Humans need communication, and describing intent in plain language is easier than speaking in rigid commands.

For developers — especially when working solo — this creates a new mirror for thinking, feedback, and brainstorming.

The real challenge now is control: quality, reliability, and intentional use. But it is also about freedom — how far we let these systems influence our creative process. As always, it is a matter of balance, and a choice that individuals and society will have to consciously make.

---

Footnotes

[^14]: Luca Rossi & Dennis Pilarinos, [How AI is Changing Engineering Docs](https://refactoring.fm/p/how-engineering-docs-change-with).
[^15]: Luca Rossi, [The pyramid of docs](https://refactoring.fm/p/how-engineering-teams-use-ai).
[^16]: [speckit.org](https://speckit.org/), GitHub.
[^17]: Vishal Kapour [@figelwump] on X: ["One thing coding with agents does is it exposes how underbaked your thinking on the details of a product really are."](https://x.com/figelwump)
[^18]: Dexter Horthy, [Advanced Context Engineering for Agents](https://youtu.be/IS_y40zY-hc), YouTube.
