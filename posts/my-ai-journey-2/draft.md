


# TITLE: My Ai-Journey part 2: A Balanced Shift


Exploring an evergreen art, made 10x more relevant by AI https://refactoring.fm/p/managing-context-for-ai-coding

## AUDIENCE
FOCUS on developers, teams tech industry: human feeling, secure jobs, be ready, share experiences

## FIRST IDEA OF A PLAN
- evaluate the shift (==BIG==, ==HARDER==), pressure on us (FOMO), seniors feedbacks (very useful, if not imposter syndrome AI fatigue, so hard to evaluate we are inside the movement, so hard for a quite new person in the industry), paradigm non determinist tool, force multiplier
- evaluate the promise of productivity, how to measure, results are not unanime, there are bad experiences
- list & listen to negative impacts/experiences to address them! (teams adoption, reality dilemna, skills, confiance, déresponsabilisation, context switching, reviews, AI Makes Everyone Average, a lots of docs for machines/not humans(paradox of spec driven))
- Opportunities, embrace chaos. the interesting parts (specs/code/artefacts, role of coding/high level task, conversations/ihm une nouvelle façon de communiquer avec les machines au delà de la commande, deliberate learning/invest in mentoring & learning, orchestrator/more PM skills, ship prototypes / test ideas in YOLO MODE, dev workflows (introspection de ces propres gestes, vocabulaires, tâches) ), find joy/pleasure in craft
- Open questions: what and how to get the hard skills fondations/hard parts
- ENDING: NExt blog post will be more practical - Keep Human in the workflow -> Teacher mode experiments with LLM


---

### The Junior Reviewer Paradox
This is the most dangerous shift I’ve seen. Historically, we had a perfect learning progression for junior engineers: you write small, isolated pieces of code, you break things, you fix them, and you slowly build a mental model of the system.

AI disrupts this flow. As Meri Williams argues, entry-level engineers are no longer writing code—they are generating it. Suddenly, a junior dev is expected to **review** code they didn't write, often using patterns they don't understand.

> *"A lot of entry level engineers don’t review much code. They’re not yet trusted to do PR reviews... But with AI, they’re reviewing code all the time."*

We are asking people with the least context to perform the task that requires the most intuition: code review. This leads to the "LGTM" syndrome, where superficially convincing AI code gets merged because the reviewer lacks the battle scars to spot the edge case hiding in line 42.



---

AGENTS
The core philosophy is moving from a "God-Mode" single agent to a **Team of Specialists** led by a **Director**.


---


PROBLEMES
- productivity/metrique
- problème: sert à justifier des décisions: biais de confirmation, ne fait pas confiance aux autres membres de l'équipe -> CONFIANCE, DERESPONSABILISER
- problème: discussion où on s'adapte (ne comprend pas l'implicite) > effet pervers sur les autres discussions entre humains
- problème: organisation, équipe, adoption
- problème: flow / context switching : plus de code, plus de revue, plus de PR, plus de feeback avec des temps difference, plus de branches reliées entre elles, en attente de validation

---

INTERESTING PARTS
- intéressant: nouvelle interaction home/machine, la conversation -> socratic method, This chain of thought
	- duck buddy, comments conversation
	- Partner mode, explain changes, redo by hand
- intéressant: chat window ou CLI AI => documentation dans l'IDE
- intéressant: se comprendre
- intéressant: challenge arts, challenge not being dumb
- intéressant: se questionner, introspection sur les gestes et étapes d'un workflow 


----
https://www.lennysnewsletter.com/p/how-to-build-your-pm-second-brain

How to build your PM second brain with ChatGPT

## **Context is important—but comes with a heavy mental load**

No matter _what_ we’re doing, we’re constantly trying to hold way too much information in our heads. I always imagine it like carrying a giant basket filled with random things like eggs, water bottles, watermelons, toy cars, a cactus (I hope you’re picturing a Dr. Seuss scene). And I’m on the go, so things are rocking all around the basket, and more things keep being added, and then an egg falls and cracks, one of the water bottles starts to spill over, a toy car keeps banging into one of the watermelons . . . basically anxiety in a metaphor.


Step 1: Create its personality
If someone were to ask you, “Hey, do you want a really smart, eager, motivated, capable person by your side who knows what you know and is super-enthusiastic to tackle anything you want?” you’d probably say yes in a heartbeat. Well, you’re in luck, because that’s exactly what Projects can be.


Step 2: Feed it information

Step 3: Let it cook

----
##  My LLM coding workflow going into 2026
https://addyo.substack.com/p/my-llm-coding-workflow-going-into
https://www.youtube.com/watch?v=FoXHScf1mjA
**AI coding assistants became game-changers this year, but harnessing them effectively takes skill and structure.**

Start with a clear plan (specs before code)
Don’t just throw wishes at the LLM - begin by defining the problem and planning a solution.

Break work into small, iterative chunks
A crucial lesson I’ve learned is to avoid asking the AI for large, monolithic outputs. Instead, we break the project into iterative steps or tickets and tackle them one by one. 
The key point is to **avoid huge leaps**. By iterating in small loops, we greatly reduce the chance of catastrophic errors and we can course-correct quickly. LLMs excel at quick, contained tasks - use that to your advantage.

Provide extensive context and guidance
LLMs are only as good as the context you provide - show them the relevant code, docs, and constraints.
 The principle is: don’t make the AI operate on partial information.


Choose the right model (and use multiple when needed)
Each model has its own “personality”. The key is: if one model gets stuck or gives mediocre outputs, try another. 

Leverage AI coding across the lifecycle
Supercharge your workflow with coding-specific AI help across the SDLC.
It’s a bit eerie to witness: you issue a command like “refactor the payment module for X” and a little while later you get a pull request with code changes and passing tests. We are truly living in the future. You can read more about this in conductors to orchestrators.

That said, these tools are not infallible, and you must understand their limits. They accelerate the mechanical parts of coding - generating boilerplate, applying repetitive changes, running tests automatically - but they still benefit greatly from your guidance. 


We’re not at the stage of letting an AI agent code an entire feature unattended and expecting perfect results. Instead, I use these tools in a supervised way: I’ll let them generate and even run code, but I keep an eye on each step, ready to step in when something looks off. There are also orchestration tools like Conductor that let you run multiple agents in parallel on different tasks (essentially a way to scale up AI help) - some engineers are experimenting with running 3-4 agents at once on separate features.

Keep a human in the loop - verify, test, and review everything
AI will happily produce plausible-looking code, but you are responsible for quality - always review and test thoroughly. One of my cardinal rules is never to blindly trust an LLM’s output. As Simon Willison aptly says, think of an LLM pair programmer as “over-confident and prone to mistakes”. It writes code with complete conviction - including bugs or nonsense - and won’t tell you something is wrong unless you catch it. So I treat every AI-generated snippet as if it came from a junior developer: I read through the code, run it, and test it as needed. You absolutely have to test what it writes - run those unit tests, or manually exercise the feature, to ensure it does what it claims. Read more about this in vibe coding is not an excuse for low-quality work.

If anything, AI-written code needs extra scrutiny, because it can sometimes be superficially convincing while hiding flaws that a human might not immediately notice.

It’s all about mindset: the LLM is an assistant, not an autonomously reliable coder. I am the senior dev; the LLM is there to accelerate me, not replace my judgment. Maintaining this stance not only results in better code, it also protects your own growth as a developer. (I’ve heard some express concern that relying too much on AI might dull their skills - I think as long as you stay in the loop, actively reviewing and understanding everything, you’re still sharpening your instincts, just at a higher velocity.) In short: stay alert, test often, review always. It’s still your codebase at the end of the day.


Commit often and use version control as a safety net. Never commit code you can’t explain.
Frequent commits are your save points - they let you undo AI missteps and understand changes.

Customize the AI’s behavior with rules and examples
Steer your AI assistant by providing style guides, examples, and even “rules files” - a little upfront tuning yields much better outputs.
Even without a fancy rules file, you can set the tone with custom instructions or system prompts.
Another powerful technique is providing in-line examples of the output format or approach you want. If I want the AI to write a function in a very specific way, I might first show it a similar function already in the codebase: “Here’s how we implemented X, use a similar approach for Y.” 


 Essentially, _prime_ the model with the pattern to follow. LLMs are great at mimicry - show them one or two examples and they’ll continue in that vein.

The community has also come up with creative “rulesets” to tame LLM behavior. You might have heard of the [“Big Daddy” rule](https://harper.blog/2025/04/17/an-llm-codegen-heros-journey/#:~:text=repository,it%20in%20a%20few%20steps) or adding a “no hallucination/no deception” clause to prompts.

In summary, don’t treat the AI as a black box - tune it.

Embrace testing and automation as force multipliers
Use your CI/CD, linters, and code review bots - AI will work best in an environment that catches mistakes automatically.


Continuously learn and adapt (AI amplifies your skills)
Treat every AI coding session as a learning opportunity - the more you know, the more the AI can help you, creating a virtuous cycle.

One of the most exciting aspects of using LLMs in development is how much I have learned in the process. Rather than replacing my need to know things, AIs have actually exposed me to new languages, frameworks, and techniques I might not have tried on my own.
This pattern holds generally: if you come to the table with solid software engineering fundamentals, the AI will amplify your productivity multifold. If you lack that foundation, the AI might just amplify confusion. Seasoned devs have observed that LLMs “reward existing best practices” - things like writing clear specs, having good tests, doing code reviews, etc., all become even more powerful when an AI is involved.

As Simon Willison notes, almost everything that makes someone a senior engineer (designing systems, managing complexity, knowing what to automate vs hand-code) is what now yields the best outcomes with AI. So using AIs has actually pushed me to up my engineering game - I’m more rigorous about planning and more conscious of architecture, because I’m effectively “managing” a very fast but somewhat naïve coder (the AI).
For those worried that using AI might degrade their abilities: I’d argue the opposite, if done right. 


The big picture is that AI tools amplify your expertise. 

But I’m also aware that for those without a solid base, AI can lead to Dunning-Kruger on steroids (it may seem like you built something great, until it falls apart). So my advice: continue honing your craft, and use the AI to accelerate that process. Be intentional about periodically coding without AI too, to keep your raw skills sharp. In the end, the developer + AI duo is far more powerful than either alone, and the developer half of that duo has to hold up their end.


I’ve learned: the best results come when you apply classic software engineering discipline to your AI collaborations. It turns out all our hard-earned practices - design before coding, write tests, use version control, maintain standards - not only still apply, but are even more important when an AI is writing half your code.

---
An LLM Codegen Hero's Journey
https://harper.blog/2025/04/17/an-llm-codegen-heros-journey
----


How I Use AI: Early 2025
https://benjamincongdon.me/blog/2025/02/02/How-I-Use-AI-Early-2025

---






Baby steps into semi-automatic coding
https://blog.lmorchard.com/2025/06/07/semi-automatic-coding

---


AGENTS
The core philosophy is moving from a "God-Mode" single agent to a **Team of Specialists** led by a **Director**.


---

Morten Rand-Hendriksen https://www.youtube.com/watch?v=yjLsHD9IzIA, Why we're giving AI too much credit | Morten Rand-Hendriksen | TEDxSurrey
	- Language  #
	- they are mirrors. Hack ourself, on ne comprend plus ce qui est artificiel et ce qui est humain => anxiété. Learning, Thinking, reasoning, training = human metaphor
	- Comme quand on voit deux rond noir => on pense que c'est un visage
		- -> https://www.experimental-history.com/p/bag-of-words-have-mercy-on-us (ChatGPT as a bag of words)
	- "Nous n'avons pas décider ou aller maintenant avec l'IA"
	- The word "Intelligence" ? => "Assisted technologies" 


---


```
# AI and developer productivity: Insights from Microsoft, Google, and GitHub researchers
From brook@em.getdx.com>: DX recently hosted a year-in-review roundtable with developer productivity researchers from Microsoft, Google, and GitHub to reflect on what we learned in 2025 about how AI is changing the way engineering teams work.

## Approaches to measuring AI impact

AI impact must be measured across multiple dimensions. Measuring AI’s impact is no different than measuring developer productivity: it requires looking at a set of metrics across multiple dimensions (quality, effectiveness, speed) as opposed to relying on a single metric.
Frameworks like the AI Measurement Framework are available to help leaders measure AI’s impact. AI is applied to an existing socio-technical system. The right approach is to measure system-level outcomes with established frameworks, and then infer AI’s impact, rather than inventing AI-only metrics in isolation.
Organizational capabilities inform AI’s impact. Capabilities such as working in small batches, strong version control practices, clear AI policies, and effective process and tooling teams amplify the benefits of AI on team and organizational performance.


## Metrics to avoid, and how to use newer AI metrics

AI has brought lines of code back into the mainstream, but it’s still not a credible measure of AI impact. Generative tools tend to produce verbose code, and more code often increases long-term maintenance cost, complexity, and risk.
The reason LOC may be having a return: it is visible and easy to measure, which makes it tempting to use. The group cautioned against defaulting to metrics that are easy rather than meaningful. Also, AI is just as good at deleting code as at generating it. The panelists provided an example of a company that significantly reduced security incidents after using AI to delete code.
The percentage of AI-generated code may be useful only as contextual data. Tracking the share of AI-authored or AI-modified code can help understand adoption patterns, budget, and token usage, as well as areas where AI is entering the stack. It is not a standalone goal metric and should not be treated as “the number” for AI success or risk.


## How AI is changing the developer role and skillset

The day-to-day work of developers is shifting from implementation to orchestration. One panelist compared this to the role of a manager. Developers need to set AI up for success with clear prompts and context, and then check the work.
There is an open question about the development of junior engineers. One concern is that relying on agents may limit opportunities to build foundational skills. Another hypothesis is that juniors may actually develop leadership and systems-thinking skills earlier because they are forced to delegate, specify problems, and review complex work sooner.
Human collaboration skills may be at risk. Working with agents does not require the same interpersonal abilities as working with people. There is interest in how agent-heavy workflows might affect communication, empathy, and professional growth beyond technical skills.


## High-value AI use cases beyond code generation

Only a small fraction of developer time is spent writing code. Coding accounts for roughly 14 percent of a typical engineer’s day. Focusing solely on code completion underutilizes AI’s potential.
AI should be applied to real, validated developer problems. The most successful programs start from well-understood friction points in the software delivery lifecycle and ask whether AI or traditional automation is the right solution, instead of starting from the technology and searching for a use case.
Documentation is an area where developers overwhelmingly want AI to help. Early deployments of AI documentation tools are already showing measurable improvements in knowledge transfer at Google.


## Agentic workflows and team-level AI adoption

Agentic workflows are expected to grow in the next phase. The last two years were dominated by IDE completion and in-editor assistants. The next wave is expected to involve agents that operate more autonomously on workflows, backlogs, and infrastructure.
At Google, teams are beginning to define norms for how agents interact with codebases. Teams are standardizing prompts that can be used for specific codebases.
Collaboration will increasingly be “teams plus agents,” not individuals plus tools. There is active research on how teams coordinate with agents, how workflows change when multiple people and agents collaborate, and what this means for concepts like task ownership, review, and accountability.
Task parallelization is a promising but under-measured behavior. Advanced AI users are already using multiple agents to explore alternative designs and implementations in parallel before committing. This may accelerate experimentation and innovation, but likely requires new metrics to capture its value.
Organizations with strong developer experience data will gain more from agents. Companies that already understand their top developer pain points are better positioned to target agentic solutions to the highest-value problems rather than “throwing AI at everything.”
```

---

AI Makes Everyone Average. Here Is The Simple Antidote.
https://alifeengineered.substack.com/p/ai-makes-everyone-average-here-is
"Actionable Advice: The Raw Layer Audit Stop living in the Summary Layer. The Summary Layer is crowded because it is easy. The Raw Layer is empty because it is dense, boring, and inconvenient. ...
Pick one problem you are stuck on. Find the primary source document related to it. Read the boring parts. You will find a nuance that the summary missed, and that nuance is your leverage"

---

## Humans in the Loop: Engineering Leadership in a Chaotic Industry
https://www.infoq.com/presentations/ai-ml-jobs/
Michelle Rush

TL;TR (BEST QUOTES/IDEAS):
- The **Jevons Paradox** says that as we use large language models to build more software, we're going to create demand for more engineers.
- **Ironies of Automation**: Partial automation makes the residual job _harder_. When you automate the easy parts, what’s left are the hard judgments, debugging edge cases, and maintenance
- AI models operate with _unconscious competence_
- SKILL 1 - System Thinking: As you move up in engineering problems, you start thinking in these bigger chunks. It's less about writing code and more about solving just the problems you have. 
- SKILL 2 - Non-Abstract System Design: **Design before you code:** Understand limits and constraints first.
- SKILL 3 - Reliability:  the large language models are going to really accelerate how quickly our systems grow and how complex they get. Since complexity is the source of outages, that's what scares me. Then, because we'll have automated away whole chunks of the system, we'll be less equipped to jump in and debug it when things go wrong. 
- SKILL 4 - Complexity Theory: What complexity theory basically tells us is that most systems have emergent behavior that is somewhat unpredictable. It is nonlinear. Sometimes it feels non-deterministic. ... The accidental stuff is the stuff that we added as engineers when we were trying to solve the problem through hardware and software. This is like our technology choices, when we write a bunch of boilerplate code, the design tradeoffs we make. In this sense, accidental is not meant to be unintentional.
- Engineering Leadership:  
	- invest in mentoring - more deliberately (think out loud, which is you bring someone along as you're solving a problem, and you talk through your thought processes and why you are solving it the way you did)
	 - make sure there's space to learn. The way we approach projects is going to be more learning focused and less just predictable



NOTES
Ecosystem Pressure & Career Implications
From a team & career standpoint:
- Software demand grows: even if AI boosts productivity, new use cases and features emerge faster. 
- Tooling wont reduce complexity by itself: meaningful automation often surfaces new structural dependencies (deployments, observability, model evaluation). 
- Junior engineers need mentorship: the talk explicitly stresses building foundational competence early — systems thinking and debugging skills scale better than rote tool knowledge. 



TRANSCRIPT
The Jevons Paradox tells us that as we make some resource more efficient to use through technology, that it actually creates more demand. That people use more of that resource. We can think of software or code as this resource in question. Since Jevons Paradox says efficiency increases demand, what we're going to see is that people are going to find more reasons to use something like software when it becomes more efficient to do so.
...
To talk about how our jobs are going to look different, I'm going to start with laying a little foundation. I'm going to talk about a concept called the curse of knowledge. The curse of knowledge is a very simple model for how to think about human knowledge. In this case, it's both knowledge and skills. It has two dimensions. The first dimension is your competence. On one side of it, you use incompetence, the other side of it is competence. You fall somewhere on that spectrum. Then you also have your consciousness. This is not like, how awake are you? It's more about, how aware are you of your own skills and knowledge?
...
Our jobs require us to constantly move between this state of conscious competence and unconscious competence.
The mental model that works really well for me is to think, generally speaking, large language models are unconsciously competent. There was actually an Apple paper, very timely, that talks about this. Basically, large language models by their nature, they know things, but they don't know why they know them. They're not really good at explainability. We are really good at the conscious competence part. Comparatively, we're really good at this. We're also really good at knowing what we don't know, so we sit really well at that conscious incompetence.
...
The biggest challenge with large language models is they sit some amount of time in that unconscious incompetence. That's how I think about hallucinations. The model doesn't know what it doesn't know, so it gets creative and it fills in a blank. The good news is models are getting better and better.
Given that understanding that we have these things that are going to write some of the code for us, but it's not entirely going to be trustworthy, it's going to have that small rate of error, we have to look at what our jobs are going to look like in that new world when we're using them a lot. The way I think about it is there's going to be roughly two categories of jobs. One is making AI/ML more useful to others. Basically, these are the folks who are building features, building workflows that make use of large language models. This is going to involve actually understanding when large language models would be useful. It's going to involve actually evaluating the model quality to see if it actually meets the use case.
...
On the other hand, there's going to be folks that are using AI/ML to be more productive.
...
The way I think about those folks, myself included, is that our jobs are partially automated away. Partially. A piece of it. Not all of it.
...
AUTOMATION
What Bainbridge (the paper of) tells us is that when you automate some piece of work, the job that you leave behind for humans to do is actually harder.
The first reason is because you give the automation the stuff that is easy, comparatively. You give it the stuff that can be described as rules, can be described as patterns, can be described as heuristics. Then humans keep all the work that is hard and requires judgment. The second reason is because when you automate something away, you still have to worry about what happens when the automation breaks. Humans have to come in and they have to fix things when it breaks.
Unfortunately, because they stopped doing that task that they used to do, they are less familiar with that work now over time. It becomes this black box to them.
...
The irony is that when you automate part of the work, the original job gets harder.
...
SKILLS
The Jevons Paradox says that as we use large language models to build more software, we're going to create demand for more engineers. Unfortunately, the ironies of automation says that engineering job is going to be harder. The end result of this is we're going to need a lot of skilled engineers. What type of skills are we talking about? Obviously troubleshooting and debugging. I love this old Brian Kernighan quote. This quote did assume that you were even writing your own code that you were troubleshooting.
Most of us already right now, we have to debug and troubleshoot a mix of code that might have been written by somebody else, someone who quit the company. It's going to be even worse because now we're going to be having code that large language models wrote in the mix. It's not just this. What's going to happen is our brains are going to start working on higher and higher abstractions. The time we might have spent trying to figure out some boilerplate code to go call some API or to figure out how to create some object on the frontend that we wanted to see, that time is going to be used on bigger problems. What that means is our brain does this thing called chunking. Chunking is basically like the brain's version of encapsulation. We take a bunch of related stuff and we group it together, and then we store it in memory as a single concept.

Then we just work on that concept until we need to drill into the details. That's how we're going to be working a lot more. We've actually been doing this our whole careers. This is not new. We don't work in digital logic circuits anymore because the tech industry gave us an abstraction. We got to move up the abstraction level. We don't write machine code. We don't write assembly language. Most people work in higher-order programming languages, but it goes beyond that. A lot of people just think about chunks. A chunk can be a database. A chunk can be a framework. A chunk can be an API method you call. We stop thinking about the details of that part. What I think what I'm going to see happen is that the new world is going to be accelerating this more than it already has. We have to start thinking about, how do we engineer quality systems without deeply understanding the parts?


SKILL 1: System Thinking
The first skill that I think is really important is systems thinking. My favorite introduction to this topic is "Thinking in Systems", by Donella Meadows. To give you a very quick overview, to me, what systems thinking is, is seeing the sociotechnical system. All the systems we work with have a mix of hardware, software, processes, and people. Then when we think about those things, we think of them not in terms of individual code.
...
We thought and we said, how do we get something that is easier to manage, easier to maintain, is less likely to have errors where somebody just misses a step? We asked the question every engineer should ask, which is, has someone already solved this? Of course, the answer was yes.

There was an existing system that was an intent-based rollout system that would allow you to describe the state you wanted production to be in at the end. It would do the work of checking safety constraints and gradually making the changes and making sure everything worked. We decided to use this instead. You might be thinking you didn't build any code, you didn't write any systems, how is this engineering? It's this chunking process.

As you move up in engineering problems, you start thinking in these bigger chunks. It's less about writing code and more about solving just the problems you have. This does not absolve us from the need to still understand what happens under the covers. We still have to be able to get into the details when needed. It just means that we can do that more opportunistically. We only do it when we know we need to work in a particular part of the system.

SKILL 2: Non-Abstract System Design
Jon Bentley wrote this great book, "Programming Pearls", and in it there's an essay called, 'The Back of the Envelope,' it tells stories about engineers before they even wrote any code, just being able to do mathematical functions and figure out whether or not their architecture would scale or not, given different parameters.

At Google we do do this, we call it non-abstract system design. How this works is that we make a map of our architecture, just basic old box and arrow diagrams. We understand that since most systems are distributed systems and most successful systems eventually encounter scaling issues, and all systems are eventually hardware constrained, we actually want to understand that before we go build and deploy the system.

SKILL 3: Reliability Engineering
As I mentioned, we started doing this to help with reliability. That makes the next skill that I think is actually going to be really important. It's like we still need reliable systems, even if we're not always writing all of the code. When I think about reliability, I don't always jump straight to the SRE book that Google wrote. You might think I do, but I don't. I actually come to Dr. Richard Cook's work on how complex systems fail. If you've seen this, it's written as a series of theorems almost. However, I tend to think of it visually. I think it is starting out with, all systems start as a small system that mostly works. I say mostly because they have bugs.
...
I think that the large language models are going to really accelerate how quickly our systems grow and how complex they get. Since complexity is the source of outages, that's what scares me. Then, because we'll have automated away whole chunks of the system, we'll be less equipped to jump in and debug it when things go wrong. I have this saying I love, which is every line of code is potential load bearing, and that's true, even code written by large language models.
...
A good example is there is one generic mitigation that I bet everyone has done, turn it off and turn it back on again. That solves all sorts of weird issues, like memory leaks, deadlocks, resetting bad state that's in memory. All sorts of stuff that's fixed by that.
...
Rollback is another really common generic mitigation.

SKILL 4: Complexity Theory
Where I've been trending with this is that really, as I said, things are going to get really complex really fast if everything plays out as folks expect. You're going to need to get really good at managing complexity. You already need this now, you just might not know it yet. Understanding complexity usually relies on leaning into complexity theory. What complexity theory basically tells us is that most systems have emergent behavior that is somewhat unpredictable. It is nonlinear. Sometimes it feels non-deterministic. It may even feel chaotic to some of us. This is true even when we think we have a somewhat simple system. Because if you've ever looked at chaos theory, you understand that even very simple functions can yield very extreme results depending on the variability in the inputs. Our systems, more and more, are going to look like complex adaptive systems.
In complex adaptive systems, the cause and effect isn't always obvious, and behavior isn't always predictable because the people, the processes, the things within the system can adapt.
...
Sometimes you can't get rid of all the complexity, because there's this idea, and it came from Frederick Brooks, that software has aspects that are essential and aspects that are accidental.
The essential things are the things that have to be there if you're solving a problem. For example, if you're working in medical software, you can't ignore the complexity of clinician-patient interactions. That's always going to be there no matter what happens. The essential stuff is the stuff like the business logic, the fundamental algorithms. This creates essential complexity. The accidental stuff is the stuff that we added as engineers when we were trying to solve the problem through hardware and software. This is like our technology choices, when we write a bunch of boilerplate code, the design tradeoffs we make. In this sense, accidental is not meant to be unintentional. A lot of this is actually intentional decisions. It's meant more in the philosophical sense is how Frederick Brooks used it, which is more like, can you remove it? Will the thing still be true?

Final Note on Engineering Leadership
we're going to need folks with a lot of experience and a lot of skills and a lot of understanding of these higher order concepts. We also have another problem. We're not going to work forever. We're not going to always be here.
...
Making any expert requires first acquiring a novice. Then, of course, we should make sure they have some foundations. They need to have this background that helps us navigate these complex systems we deal with. Of course, we need to level them up in these higher order skills that we need, like systems thinking, and non-abstract system design, and reliability engineering, and, of course, dealing with complexity.
...
They're going to be in that unconscious incompetence state where they're not even going to know what they don't know.
...


First, we're going to have to invest in mentoring. The best way to mentor is not through advice. Advice is the worst way to mentor. The best way to mentor is actually to think out loud, which is you bring someone along as you're solving a problem, and you talk through your thought processes and why you are solving it the way you did. It's more like an apprenticeship. We're going to need to do this more deliberately. The other thing we're going to do is we're going to have to make sure we're having opportunities to learn for folks. We have to make time and space. It's very easy for us when we're experienced folks to basically say, it would just be faster if I did this myself. If we do everything ourselves or if we give everything to the coding assistants, we're not creating space for these early career folks to come in and learn how these things all work. We have to be able to do delegation, like actual delegation. I was almost tempted to call this the fifth skill because so many of us have a hard time doing this. We just want to do things ourselves.

Then, of course, we have to make sure there's space to learn. Not just for the folks coming into the industry, but also for ourselves because we're going to have to grow and adapt and learn as we go. The way we approach projects is going to be more learning focused and less just predictable. Because developing the next batch of experts is going to be a big part of what we need to do going forward, just as much as building all these amazing software systems that we never thought we could build before. Because we're going to need a lot of engineers, capable of managing all this complexity that's going to come at us really fast at this accelerated rate. Because if we don't do that and we don't manage the complexity that's coming at us, our systems are going to devolve into chaos.


---

Human in the Loop: Interpretive and Participatory AI in Research
https://gcdi.commons.gc.cuny.edu/2025/10/10/human-in-the-loop-interpretive-and-participatory-ai-in-research/


---

Task-Centricity: The Future of Human-AI Collaboration
https://humainary.io/blog/task-centricity-the-future-of-human-ai-collaboration/

---


DevAI: Beyond Hype and Denial
https://www.ivankusalic.com/realistic-DevAI/

---

https://www.youtube.com/watch?v=-5_6HQR0WhA
L'état de l'adoption de l'IA dans les équipes d'ingénierie 📊 — avec Matt McClernan

---


Everybody Else Is Doing It, So Why Can't I?
https://www.linkedin.com/pulse/fear-learning-vancouver-clarifying-journey-realities-rand-hendriksen-xzsbc/
Like a shag carpet drenched in spilled soda pop, this looming dread that _everyone else is doing it, so why can't I_ formed the subtle but uncomfortably ever-present base for so many conversations I started wondering if it was I who brought the doom (wouldn't be the first time). So I listened, and observed, and confirmed that no, it wasn't me. It was everyone.


AI GEN MYTHS
https://www.linkedin.com/pulse/ai-bubble-bursting-shocking-mit-study-key-from-gilded-ryan-levesque-uytfe


----


What change / What not

but a nuanced approach to start a pragmatic approach would be to list pain points and find if I can solve them for me at least or for my team at worst. (Identifier les principales frictions rencontrées dans les équipes — techniques, organisationnelles ou humaines — et proposer pour chacune une approche concrète pour les dépasser.)



I’ll be honest: I’m relatively new to this industry, and this rapid evolution induces a specific kind of guilt. I often feel like I’m not adapting fast enough. The tech radar is saturated with AI and LLM content. It feels, by far, like the biggest technology shift in my professional career.

But hearing industry veterans like Martin Fowler acknowledge the magnitude of this change helped me realize: **this is a big shift for everyone.** We are all trying to find our footing.

The question now isn’t *whether* to use these tools. It’s *how* to use them without trading long-term understanding for short-term productivity. Using AI well is genuinely difficult. It requires time to learn, deliberate practice, and a clear sense of when in the workflow it actually helps.

After the JavaScript fatigue, are we entering the AI fatigue?

In the next post, **Part 3: A Balanced Shift, Promises & Reality**, I’ll explore the pressure on productivity, the evergreen skills that still matter, and how to carve out space for experimentation without sacrificing the craft.



Here are the exact text snippets we set aside from your draft. You can copy-paste these directly into your workspace to start **Blog Post 3: "A Balanced Shift."**

### 1. The Opening Hook: AI Fatigue & Guilt

_Use this to open the post. It connects emotionally with the reader after the heavy themes of Post 2._

> "After the JavaScript fatigue, are we entering the AI fatigue?
> 
> I’ll be honest: I’m relatively new to this industry, and this rapid evolution induces a specific kind of guilt. I often feel like I’m not adapting fast enough. But using AI well is genuinely difficult. It requires time to learn, deliberate practice, and a clear sense of _when_ in the workflow it actually helps."

### 2. The Opportunity: Redefining Interaction (New IHM)

_Use this in the section about how we should build tools, not just use them._

> "**New IHM.** I think a great opportunity with these tools is to redefine the human interaction to machine. Underneath all of this, there's still a genuine human need—to communicate, to reason together, to build shared understanding."



## Barriers

Meri argues that, up until today, engineers had a perfect learning progression: write small pieces of code, gradually take on bigger tasks, and slowly build expertise. AI disrupts this natural flow:

> _**“A lot of entry level engineers don’t review much code. They’re not yet trusted to do PR reviews... But with AI, they’re reviewing code all the time.”**_

Something needs to change, and we need to work intentionally on it. Meri’s best guesses are the following:
    🔍 Earlier code review training — teach juniors to spot problems they’ve never encountered.
    🏗️ Focus on foundational skills — security, performance, scalability, maintainability.
    👥 Double down on mentorship — pair programming and design sessions become crucial.

https://refactoring.fm/p/diversity-ai-and-junior-engineers

## Metrics

https://packmind.com/what-we-learned-from-the-packmind-x-dx-webinar-the-real-roi-of-ai-for-engineering-teams/
https://getdx.com/resources/

## Big shift in the industry
I'm quite new in the industry, I feel some discumfort and guilty about that, not adapting myself fast. 

> The radar (veille technologique) is full of a lot AI or LLM things. It's because this is a huge change in my professional carreer. It feels by far the biggest technology innovation changes coming in. (The Pragmatic Engineer, How AI will change software engineering – with Martin Fowler https://youtu.be/CQmI4XKTa0U?t=990). 
> https://newsletter.pragmaticengineer.com/p/martin-fowler
> Gergely Orosz: It's the biggest of my career.

Biggest shift is determinism to non-determinism
Tolérance, précipices
Pros: 
- Prototype, exploration more than just vibe coding (petits outils jetables)
- Understand legacy system: semantic analysis -> graphed database -> RAG, How do you effectively modernize legacy system?
Danger
- review all code: "Genie" (term from G.K. Kent) or "Dusty" (anthropomorphic donkey, term from Birgitta Boeckeler)
- understand legacy code: ok, but modify legacy code is a safe way? It is still a question
- Team: How do we best operate with AI in the team environment?
We're still learning how to do this.

More and more code reviews.

About the idea of "A language to talk to a LLM", we could argue that AI IDE (vs code, cursor, ... ) ou AI CLI (cline, wrap, claude code) add a layer between all inputs and outputs to manage better the conversation with the llm. See https://egghead.io/claude-code-is-a-platform-not-an-app~vlf9f.

Also, you could be interested in something like: https://boundaryml.com/ , The First Language for Building Agents or any AI dev kit, like google Agent Development Kit (ADK)
, https://google.github.io/adk-docs/. I

## First, retrieve Objections to address them

Say, you don't have great results with AI, and you loose too much time, it's a common objection and I tend to think it is part of the learning process of these tools. The answer would be "You don't use  well these tools, you should ..." or it is a mindset issue, personal or organizational ([^2]). Well, it seems true and false.

## Productivity

Wasting time ...

If the productivity is the promise, how might we figure out if AI boosts productivity ? A great study [^3] on 100K Developers from Yegor Denisov-Blanch tried to respond to this question. Trying to count commits number on a repository for instance is not a good metric, because AI creates a lot of rewrite codes (bugs or refactors). The study results is really close to what a daily developer might think. Sometimes it boots our productivity, but sometimes not. The productivity depends on several parameters: language popularity, task complexity, codebase maturity (greenfield / brownfield), codebase size, context length. I think we could add also "AI skills".

IMAGE.

You have certainly seen A lot of video about coding with AI, shows a case with a simple new project from scratch (greenfield). As it is really nice to prototype, share ideas, allowing non-developers to express their own business needs and rules (that's certainly a great point), it is not a common scenario to the majority: we are developing in a hybrid codebase with legacy, dependencies, old and new patterns. If we are in the Research & Development, it is another scenario where AI is tricky: new fields without enough data to train the model ...

Honestly, I'm not a x10 developer, like the study shows, I 'm most likely in between -2%/5%. On certain tasks, I learn and loose some time, on simple tasks i gain some power. I tend to think I'm still a flat growing learning curve.


## Pressure on productivity

> The pressure to ship faster with AI assistance can lead to a culture where understanding code becomes secondary to producing it. Developers now find themselves in environments where asking AI is not just acceptable but expected, potentially stunting their growth trajectory.
> We’re not becoming 10× developers with AI, we’re becoming 10× dependent on AI. **Every time we let AI solve a problem we could’ve solved ourselves, we’re trading long term understanding for short term productivity.** https://codebytom.blog/2025/07/the-hidden-cost-of-ai-reliance


## Evergreen skills in a drastly evolving market

In fact, using AI well is really tough. We certainly need time to learn, experiment, find the best way to inject context, talk to models, using third party helpers, when in the workflow.  Apprendre -> temps (Geoffrey Huntley -> deliberate intentional practice). Context engineering is still an emerging science. Comment gérer les temps d'expérimentation et de production as a team.

### After the JS Fatigue, the AI fatigue?

The current state is always evolving, learning with tools that change is 

• L'accélération des avancées et nouveautés rend l'adaptation difficile dans un contexte professionnel
• Perte de temps (lecture, validation, correction, debug, boucle) 

Initial discomfort 
Tension between acceleration and exhaustion — productivity vs. cognitive fatigue.
- a lot of shifts -> uncomfortable -> embrace
- - épuisant


Promesse de gagner du temps dev pour déplacer l'énergie vers la définition des besoins -> mais beaucoup de ce temps est plutôt dévolu à l'expérimentation


## Benefits for small teams
Everyone becomes an “engineer” — even non-technical roles now prototype with AI. - tout le monde devient ingénieur (sales > prototypes), Code don't belong to developers
BENEFITs: for a small team -> it helps understanding the codebase, develop features, discuss




- Code VS Product



## Security
• Crainte de créer des failles de sécurité  
Comment s'assurer que je ne créé pas des failles de sécurité - risques pour mon entreprise ?



TIME
VERBOSE Mode by default
- Verbeux -> temps de lecture
- Verbeux -> productions > quality, remplissage, qui produira les documents les plus intéressants

## SHIFT. Posture, Role changes

ORCHESTRATEUR:
> The central challenge, and opportunity, lies in a new developer paradigm. We are no longer simply "bricklayers" defining explicit logic; we are "architects" and "directors" who must guide, constrain, and debug an autonomous entity. (Introduction to Agents, White paper)

-> Architecte, système

• Perte de contrôle (responsabilité, plaisir à trouver des solutions) > observateur  
• La posture d'orchestrateur d'agents déplace le temps de l'implémentation vers un temps de spécification (vision produit) et augmente le temps de "review". 'Promesse'


Pionnier du DevOps, Patrick Debois voit dans l’IA native une nouvelle transformation majeure. Les développeurs n’écriront plus le code de la même manière, mais ils piloteront désormais des agents.
https://www.blogdumoderateur.com/devops-ia-native-developpeurs-managers-agents/


## Alignement issues: Re-thinking documentation
• Manque de confiance (hallucinations, non-déterminisme)
- Alignement (Beast mode)
• Le contexte est roi : la qualité des résultats de l'IA dépend directement de la qualité du contexte fourni. La documentation et les spécifications deviennent la source de vérité, des artefacts fondamentaux.

Updated Standards
> Language models can only reproduce language patterns from their training data. **They can't learn anything new**. 


### But Needs of Specific processes
- FILES/DOCS for AI or for Humans (!!!). Docs are not only for Human, ultra verbose to contrain the model, repetitive
- Déformation : traiter les humains comme des machines -> IHM

! EFFET ETRANGE. Le besoin de specs: humain et machine LLM différents. D'ailleurs pour remplir les instructions d'un agent LLM on le fait à l'aide d'un LLM... Différent de specs entre humain (implicite, explicite, alignement, contexte le LLM est un bébé)

### 1 PROCESS MORE OR FEWer PROCESSES LESS ?

There are differents mindsets for developers. Time, Code artefact

Les profils dev "fonceurs", make it work first peuvent pas apprécier que la documentation, les spécifications prennent le pas sur la production de l'artefact le plus important le code. Encore une manière de détourner l'énergie

Conceptuel vs Organic: 1 process de plus -> bureaucraty, process > creativity, DIY, plaisir, human



### NON DETERMINISTIC
The Paradigm Shift: From Predictable Code to Unpredictable Agents
Agent Quality in a Non-Deterministic World.
• Manque de confiance (hallucinations, non-déterminisme)
• Travailler avec un assistant "non déterministe". L'IA est un assistant, un copilote. Le développeur reste le pilote.



(> NEXT BLOG POST: Context Engineering)

* AI isn’t changing the fundamentals of software development — we still need tools, skills, and human judgment.
* AI is a tool — embrace its non-determinism and learn to use it to your advantage.
* Don’t trust the AI blindly — LLMs don’t understand; they reproduce existing patterns.
* Models are conservative and biased — but you can steer them with the right input and context.
* Tests matter more than ever — make sure your tests actually check something **meaningful**.




- _green field_ = terrain vierge, _brown field_ = site déjà utilisé ou industrialisé
