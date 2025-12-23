## 2. The Promise of Productivity

We’ve all seen the demos: a developer builds a full-stack app in 20 minutes using nothing but natural language prompts. It’s a compelling sell for the "10x Developer" myth. But when you try to apply that same logic to a five-year-old codebase filled with legacy dependencies, the magic usually dissolves into a frustrating game of "spot the hallucination." These demos conveniently ignore the "pre-work"—the hours spent writing, testing, and refining the specification files that actually drive the generation.

### How to Measure It

If productivity is the goal, we need a better way to define "winning" than just lines of code.

AI forces us to re-evaluate how we measure value. To cut through the noise, industry reports and tech radars have become essential for understanding what is actually happening on the ground. Measuring impact is complex and evolving.

> "AI impact must be measured across multiple dimensions. [...] It requires looking at a set of metrics across multiple dimensions—quality, effectiveness, speed—as opposed to relying on a single metric." (DX [^7])

DX proposes this AI Measurement Framework which focus on three key dimensions: utilization, impact, and cost. [^8]

![[dx-ai-measurement-framework.png]]

### The Context Reality: One Size Fits None

A study of 100,000 developers by Yegor Denisov-Blanch [^9] highlights what’s often missing from the conversation. It confirms that counting commits is a useless metric because AI often generates "noisy" code—large chunks of rewrites that may introduce as many bugs as they solve. The results of this study are fairly consistent with what a developer might think on a daily basis. Sometimes it boosts our productivity, sometimes it doesn't.

![[graph-greenfield-brownfield.png]]
(Greenfield projects gain 30-35% on simple task, and 10-15% on complex ones, versus 15-20% and 5-10% in brownfield projects - Yegor Denisov-Blanch)

The data suggests several technical constraints that dictate whether an AI tool is a lever or a weight:

* **Language Popularity:** Models struggle with niche languages where training data is scarce.
* **Context Length:** Even as context windows expand, the risk of "disalignment" increases. The more context you provide to explain a legacy system, the more likely the LLM is to lose the thread.
* **Task Complexity:** AI handles isolated tasks—like writing a single utility function or a unit test—fairly well. However, complex refactoring across multiple files requires so much manual oversight that it can often become a net time-sink.
* **Codebase Maturity:** This is the "Greenfield vs. Brownfield" divide. AI excels in new projects where there is no technical debt to navigate (the "YouTube Demo" mode). In Brownfield projects, where old patterns clash with new dependencies, productivity gains drop significantly.
* **Codebase Size:** As the repository grows, the model's ability to understand the codebase and maintain architectural consistency diminishes.

I’d also add **"AI Literacy"** to this list—knowing how to feed the model the right documentation, setting environment rules, and knowing when to ignore the suggestion entirely.

These parameters explain quite well, why I can feel like a "5x developer" on Tuesday when I'm prototyping in "YOLO mode," only to become a "-5% developer" on Wednesday when I try to rework an existing module the AI simply can't grasp.

---

Footnotes

[^7]: [AI and productivity: Year-in-review with Microsoft, Google, and GitHub researchers](https://getdx.com/blog/year-in-review-with-microsoft-google-and-github-researchers/), DX.
[^8]: [Measuring AI code assistants and agents](https://getdx.com/research/measuring-ai-code-assistants-and-agents/), DX.
[^9]: [Does AI Actually Boost Developer Productivity? (100k Devs Study)](https://youtu.be/tbDDYKRFjhk), Yegor Denisov-Blanch, Stanford.
