# 2. The Promise of Productivity

We’ve all seen the demos that takes 20 minutes to build a complete fullstack app. It sells the idea of the "10x Developer." But when you try to apply that to a real-world, 5-year-old codebase with some legacy dependencies, the magic often dissolves into a frustrating game of "spot the hallucination. That kind of demo often hides the time to write, experiment, refine and test the specification files that help generating the app - the real things. 

## How to Measure It

If "productivity" is the promise, how do we know if we are actually winning?

As a Side effect of AI, all the questions about AI usages brings interesting questions, as it tries to better understand the system of producing products & value, through all different kind of jobs, skills and tasks. I tend to think that reports, surveys, tech radars from the industry become more and more important to navigate in the Fog, understand what happens, what could happen. 

Some of reports spotted this year:
- https://getdx.com/research/measuring-ai-code-assistants-and-agents/
- AI Where It Matters: Where, Why, and How Developers Want AI Support in Daily Work: https://cabird.github.io/AI_where_it_matters/
- DORA, https://dora.dev/research/2025/dora-report/, The State of AI-assisted Software Development report
- AI Assisted Development: Real World Patterns, Pitfalls, and Production Readiness, InfoQ, https://www.infoq.com/minibooks/ai-assisted-development-2025/
- AI Impact: Report 2025, https://leaddev.com/the-ai-impact-report-2025
- Tech Radar from ThoughtWorks, https://www.thoughtworks.com/radar
- The GenAI Divide: STATE OF AI IN BUSINESS 2025 from MIT, https://mlq.ai/media/quarterly_decks/v0.1_State_of_AI_in_Business_2025_Report.pdf

All of this reports show that there is not one single way to measure impact, it is very complex.

> AI impact must be measured across multiple dimensions. [...] It requires looking at a set of metrics across multiple dimensions (quality, effectiveness, speed) as opposed to relying on a single metric. (DX. AI and developer productivity: Insights from Microsoft, Google, and GitHub researchers.)

DX proposes this AI Measurement Framework https://getdx.com/research/measuring-ai-code-assistants-and-agents/
![https://getdx.com/img/optimized/fiISLE-A0k-4040.webp?_cchid=bc3577b59e550f888f851b7c5ed458fd]


## The Context Reality: there is no one ai usage that works for everyone (one sits for all)

Another great study [^3] on 100K Developers from Yegor Denisov-Blanch bring what's actually missing. It stands that trying to count commits number on a repository for instance is not a good metric, because AI creates a lot of rewrite codes (bugs or refactors). The study results is really close to what a daily developer might think. Sometimes it boots our productivity, but sometimes not. 

They spot several parameters that influence the productivity of AI Tools: 
- language popularity: the real pain might be for niche languages where the models have not enough trained data
- context length: you know that even if the context window of the LLM is increasing, more the context is big, more the LLM can be disaligned. It is related to other parameters, if you have to put a lot of context to explain your task, your codebase, it could result some bad side effects.
- task complexity: when asking simple and isolated tasks, one function, one component, or few tests for this function the results are pretty much fine or close to what is expected; but complex refactoring or not-trivial feature that include mutliple files / folders needs to be done very carefully with a lot of context and preparation - results could be less predictable, or even just a waste of time.
- codebase maturity (Greenfield vs. Brownfield). AI excels on brand new projects (Greenfield), this is the "YouTube Demo" mode, but Brownfield (Legacy Systems) is where most of us live, where you have old dependencies, a mix of new & old patterns
- codebase size: more the codebase is big, more the LLM can be disaligned

![graph-greenfield-brownfield.png]
Greenfield projects gain 30-35% on simple task, and 10-15% on complex ones, versus 15-20% and 5-10% in brownfield projects - Yegor Denisov-Blanch

I think we could add also a parameter about "AI skills": how to use AI tools efficiency, using the right tool, given enough context files or documentation, coding environment settings & rules.

These parameters are very useful to explain why on some days, I'm a "5x developer" (prototyping a new feature in YOLO mode), and on other days, I'm a "-5% developer" (refactoring legacy code to add new features, or think about architecture patterns that is not well done is other part of the codebase).

---
[^5]: **DX & GitHub Research**: "Generative tools tend to produce verbose code, and more code often increases long-term maintenance cost." — *DX Roundtable*
[^6]: **Yegor Denisov-Blanch Study**: Analyzing 100k developers showed that productivity gains vary wildly based on task complexity and codebase maturity.
