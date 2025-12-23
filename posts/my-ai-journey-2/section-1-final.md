## 1. The "Big Shift": Cutting Through the Fog

The hype around JavaScript frameworks has finally quieted down, but only because it was replaced. Since Angular arrived in 2012, we’ve seen at least 15 major frontend frameworks. Now, looking at the volume of AI models & tools released in the last three years, we’ve traded JavaScript fatigue for full-blown **AI fatigue**...

As a newer engineer, this pace feels unsettling. Knowing which skills will matter in five years is nearly impossible, creating a sense of professional vertigo. Morten Rand-Hendriksen captures this in "Everybody Else Is Doing It, So Why Can't I?" which looks at **F.O.M.O.** [^1] in an era of constant change.

### Perspective from the Veterans

To see through the fog, I looked to those who have lived through previous industry shifts.

When **Martin Fowler** and **Gergely Orosz** discussed this, they didn't just nod at the hype; they acknowledged this as the **biggest technology shift of their careers** [^2]. That’s a relief. It confirms the current confusion isn’t just a "junior" problem—it’s an industry-wide transformation. **The ground is moving for everyone**.

### Why This Feels Different

Once you accept the collective struggle, you can evaluate the shift for what it actually is.

**1. The Paradigm Shift: Non-Determinism**
Software engineering is traditionally a deterministic process. You translate requirements into functions and classes with expected behaviors. Even complex bugs remain traceable.

> "Because if you've ever looked at chaos theory, you understand that even very simple functions can yield very extreme results depending on the variability in the inputs". (Michelle Rush [^3])

The new world introduces non-deterministic assistants. We now spend our energy fighting to provide enough context to keep "Black Box" LLMs from drifting—a challenge that scales poorly at the team level. It changes our relationship with code, requiring new skills, new tools and logging strategies.

**2. The "Intelligence" Trap**
Morten Rand-Hendriksen argues that "Intelligence" is a loaded term that gives these tools too much credit; we should view them as **Assisted Technologies** [^4]. Terms like *learning* or *reasoning* are human metaphors that trigger our bias to anthropomorphize machines.

> "We want to understand these things as people... We can’t help it; humans are hopeless anthropomorphizers". (Adam Mastroianni [^5])

This is similar to **Pareidolia**—the same instinct that makes us see faces in clouds. Our brains find patterns and project intent where there is only mathematics. As Rand-Hendriksen notes, when the line between human and artificial becomes blurred, it generates deep-seated anxiety.

**3. The Irony of Automation**
If using AI feels exhausting, there is a technical reason for it. Michelle Rush refers to this as the **Irony of Automation**: partial automation often makes the remaining manual tasks harder.

> "When you automate the easy parts, what’s left are the hard judgments, debugging edge cases, and maintenance". (Michelle Rush [^3])

* The AI handles the "low-hanging fruit": boilerplate, syntax, and common patterns.
* The human is left with the high-complexity tasks: judgment, edge cases, and debugging failures.
* **The Result:** Your "typing" time decreases, but your **thinking intensity** skyrockets.

**4. The Foundation Still Holds**

> "Almost everything that makes someone a senior engineer is what now yields the best outcomes with AI". (Simon Willison [^6])

This leads to a vital reassurance: **the fundamentals haven’t changed**. Engineering foundations are more critical now than ever. If your foundations are weak, AI just helps you build a flawed system faster. If your foundations are strong, AI becomes a powerful lever.

---

**Footnotes**

[^1]: [Everybody Else Is Doing It, So Why Can't I?](https://www.linkedin.com/pulse/fear-learning-vancouver-clarifying-journey-realities-rand-hendriksen-xzsbc/), Morten Rand-Hendriksen.
[^2]: [How AI will change software engineering – with Martin Fowler, Gergely Orosz](https://newsletter.pragmaticengineer.com/p/martin-fowler), The Pragmatic Engineer.
[^3]: [Humans in the Loop: Engineering Leadership in a Chaotic Industry](https://www.infoq.com/presentations/ai-ml-jobs/), Michelle Rush.
[^4]: [Why we're giving AI too much credit](https://www.youtube.com/watch?v=yjLsHD9IzIA), Morten Rand-Hendriksen, TEDxSurrey.
[^5]: [Bag of words, have mercy on us](https://www.experimental-history.com/p/bag-of-words-have-mercy-on-us), Adam Mastroianni.
[^6]: [Using LLMs for code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/), Simon Willison.
