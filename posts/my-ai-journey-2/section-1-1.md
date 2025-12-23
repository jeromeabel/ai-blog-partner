## 1. The "Big Shift": Navigating the Fog

The hype surrounding JavaScript frameworks has finally quieted down, but only because it’s been replaced. Since Angular’s debut in 2012, we’ve seen at least 15 major frontend frameworks emerge. Now, looking at the sheer volume of AI models and tools released in just the last three years, it’s clear we’ve moved from JavaScript fatigue into full-blown **AI fatigue**.

As someone relatively new to the industry, this pace is genuinely unsettling. Visibility on which skills will actually matter in five years has dropped to zero, creating a sense of professional vertigo. This feeling is captured perfectly in Morten Rand-Hendriksen’s "Everybody Else Is Doing It, So Why Can't I?" [^1] which explores **F.O.M.O** in an era of constant shift.

### Listening to seasoned developers

To see through the fog, it helps to listen to those who have navigated previous industry shifts.

When I heard veterans like **Martin Fowler** and **Gergely Orosz** discuss this [^2], something clicked. They weren't just nodding at the hype; they acknowledged that this feels like the **biggest technology shift of their professional careers**. Hearing that was a relief. It confirmed that the current confusion isn't a "junior" problem—it’s an industry-wide transformation. **This is a massive shift for everyone**.

### Evaluating the shift

Once you accept that *everyone* is struggling, you can stop panicking and start evaluating the shift for what it is. What makes this particular transition so different?

**1. The Paradigm Shift: Non-Determinism**
Traditionally, building software is a deterministic process. You translate requirements into functions, classes, and dependencies with expected behaviors. Even when complexity leads to bugs, the system remains traceable and debuggable.

> "Because if you've ever looked at chaos theory, you understand that even very simple functions can yield very extreme results depending on the variability in the inputs". (Michelle Rush [^3])

The new world introduces non-deterministic assistants. We now spend our energy fighting to provide enough context to keep "Black Box" LLMs from drifting off-course—a challenge that only intensifies at the team level. It redefines our relationship with code, requiring new skills, tools, and logging strategies.

**2. The "Intelligence" Trap**

Morten Rand-Hendriksen argues that "Intelligence" is a loaded term that gives these tools too much credit. We should view them as **Assisted Technologies** [^4]. Terms like *learning*, *thinking*, and *reasoning* are human metaphors that trigger our natural bias to anthropomorphize anything that mimics human interaction.

> "We want to understand these things as people. When you type a question to ChatGPT and it types back the answer in complete sentences, it feels like there must be a little guy in there doing the typing... We can’t help it; humans are hopeless anthropomorphizers". (Adam Mastroianni [^5])

This is similar to **Pareidolia**—seeing faces in clouds. Our brains are wired to find patterns, leading us to trust the machine more than we should. We project intent where there is only mathematics. As Rand-Hendriksen notes, when the line between human and artificial becomes blurred, it generates deep-seated anxiety.

**3. The Irony of Automation**
If using AI feels exhausting, there is a technical reason for it. Michelle Rush refers to this as the **Irony of Automation**: partial automation often makes the remaining manual tasks harder .

> "When you automate the easy parts, what’s left are the hard judgments, debugging edge cases, and maintenance". (Michelle Rush [^3])

* The AI handles the "low-hanging fruit" (boilerplate, syntax, common patterns).
* The human is left with the high-complexity tasks (judgment, edge cases, debugging failures).
* **The Result:** Your "typing" time decreases, but your "thinking intensity" skyrockets.

**4. The Foundation Remains**

> "Almost everything that makes someone a senior engineer is what now yields the best outcomes with AI." Simon Willison [^6]

This leads to a vital reassurance: **the fundamentals haven’t changed**. Engineering foundations are more critical now than ever. If your foundations are weak, AI just helps you build a flawed system faster. If your foundations are strong, AI becomes a powerful lever.

---

Footnotes

[^1]: [Everybody Else Is Doing It, So Why Can't I?](https://www.linkedin.com/pulse/fear-learning-vancouver-clarifying-journey-realities-rand-hendriksen-xzsbc/), Morten Rand-Hendriksen

[^2]: https://newsletter.pragmaticengineer.com/p/martin-fowler, The Pragmatic Engineer, How AI will change software engineering – with Martin Fowler, Gergely Orosz

[^3]: Humans in the Loop: Engineering Leadership in a Chaotic Industry, https://www.infoq.com/presentations/ai-ml-jobs/, Michelle Rush

[^4]: Morten Rand-Hendriksen https://www.youtube.com/watch?v=yjLsHD9IzIA, Why we're giving AI too much credit | Morten Rand-Hendriksen | TEDxSurrey

[^5]: Bag of words, have mercy on us, https://www.experimental-history.com/p/bag-of-words-have-mercy-on-us, Adam Mastroianni

[^6]: https://simonwillison.net/2025/Mar/11/using-llms-for-code/, Simon Willison
