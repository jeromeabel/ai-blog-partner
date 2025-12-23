## 3. The Dehumanization Trap

To get better at using AI, we have to look objectively at the friction it creates. While the speed of LLMs is impressive, their verbosity creates a set of technical and psychological side effects that can actually degrade the quality of our work and our well-being.

### The "Average" Factory

In his piece "AI Makes Everyone Average" [^10], Steve Huynh highlights a risk often called "skills atrophy". If you rely entirely on AI, you stop engaging with the "boring" but essential parts of the job—raw documentation, source code, and RFCs. You begin to live in a "Summary Layer": a crowded space where everyone uses AI to generate the same B+ explanations and generic components.

The real technical edge in engineering comes from the nuance found in the raw source material. When we stop digging deeper, our solutions regress to the mean. This can lead to a dangerous "de-responsibilization," where critical thinking is replaced by a confirmation bias—assuming the LLM is correct simply because its output looks authoritative or confirms our initial hypothesis.

### The Context-Switching Tax

Context switching is the enemy of engineering flow. Moving between tasks can cost as much as 40 percent of a person's productive time. AI tools introduce a new, unpredictable form of this interruption.

> "Even brief mental blocks created by shifting between tasks can cost as much as 40 percent of someone's productive time" (American Psychological Association [^11])

When working with AI, feedback loops can range from five seconds to several minutes. For simple tasks, the wait is predictable; for complex research or multi-file edits, it’s a black hole. While many tools now show "steps" or intermediate results to keep you engaged, the "thinking gap" often breaks your concentration. 

I’ve tried managing two user stories across two IDEs—launching an AI task in one and switching to the other while it runs. To be honest, in most cases, it fries my brain. It only feels manageable when the projects are homogeneous—similar in both timeframe and scope. But the question remains: what kind of AI task can you launch without breaking your flow? Usually, if a task is going to take a while, it’s better to launch it before a coffee break rather than trying to multi-task through the wait.

### The Joy of Crafting

For many of us, the joy of coding comes from the "cognitive battle"—the stimulating effort of solving a problem ourselves. Failure is a vital part of that learning process; it teaches us why certain paths were wrong and what trade-offs were made. AI shifts the developer’s role from a "creator" to an "orchestrator" or "compliance officer".

I’ve noticed that dealing with specification files creates a clear divide in how developers work. Some of us prefer to code first and let the specs evolve organically as we build. Forcing a complete specification upfront feels like a return to the Waterfall model—it’s bureaucratic and disengaging. We are being pushed into the drudgery of prompt engineering, where the "make it work" joy of hacking is being replaced by a "specify it correctly" mindset that turns our craft into a compliance task.

> Lawmakers as programmers?! (Sean Grove [^12])

We are entering a paradox of Spec-Driven Development. I find myself writing more documentation than ever, but I'm not writing it for my team—I'm writing it to constrain the LLM’s search space. This results in two sets of documentation: one for humans and a verbose, counter-intuitive set for the machine, filled with capital letters and "DO/DON'T" instructions specifically designed to prevent the model from hallucinating. 

The weirdest part is that you eventually end up asking the LLM to write instructions for itself based on its own previous failures. In this workflow, you aren't the builder anymore; you’ve become a "human gateway" between the specification and the code.

### The Team Dynamic

As Martin Fowler notes [^2]:, we are still learning how to operate with AI in a team environment. It requires a shift in organizational culture and a healthy data ecosystem.

> Successful AI adoption requires more than just tools. Our new DORA AI Capabilities Model identifies seven foundational practices—including a clear AI policy, a healthy data ecosystem, and a user-centric focus—that are proven to amplify the positive impact of AI on organizational performance. (DORA Report [^13])

AI creates a "problem of more". AI allows us to generate more code, which leads to more PRs, more branches, and more feedback cycles—yet we have the same number of people to do the actual reviewing. We’re creating a massive bottleneck where code sits in waiting, reliant on human validation that hasn't scaled alongside the AI's output.

There is also a deeper problem with empathy. It’s tempting to give an LLM more confidence than your own teammates. When you stop trusting the humans on your team and defer to the model, you lose the shared responsibility that actually makes a team functional.

---

Footnotes

* **[^10] Steve Huynh**, [AI Makes Everyone Average](https://alifeengineered.substack.com/p/ai-makes-everyone-average-here-is)
* **[^11] American Psychological Association**, [Multitasking: Switching costs](https://www.apa.org/topics/research/multitasking)
* **[^12] Sean Grove**, [The New Code](https://youtu.be/8rABwKRsec4), OpenAI
* **[^13] DORA**, [The State of AI-assisted Software Development report (2025)](https://dora.dev/research/2025/dora-report/)

