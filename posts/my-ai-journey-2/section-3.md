## 3. The Dehumanization Trap

To get better as using AI tools, I think objectivally we should list & listen to negative impacts/experiences to address them and find solutions if there is some that fit well! The verbosity of LLM generates a lot of side effects.

### The "Average" Factory
Related to what's called the "skills atrophy", in "AI Makes Everyone Average", Steve Huynh points another interesting arguments. If you rely entirely on AI, you stop reading the "boring parts"—the raw documentation, the source code, the RFCs. You live in a "Summary Layer"—that crowded space where everyone uses AI to generate the same B+ explanations and the same generic React components. But the leverage in engineering often comes from the nuance found in the raw layer. When we stop digging, our solutions regress to the mean. (See https://alifeengineered.substack.com/p/ai-makes-everyone-average-here-is)

Also the confidence is LLM outputs could result to some kind of personal deresponsabilisation, when you critical thinking is not really applied, or it is too hard to pause and review all the generated outpus: todos, mid-results, files, summary, ... We could suffer from a confirmation bias, or simply an imposter syndrom and give LLM outputs to much credits because we think that LLM is better than us, or it just confirm our hypothesis.

### Context Switching

You certainly know that "context switching" is a really bad phenomen in collective work, it decrease productiviy, and increase stress. When a task is interrupted and when we have to go again, we loose a pretty much amount of time. It breaks some kind of "flow". Some reports measure this amount of time lost. That's the other side of working on high cognitive task. Multi-tasking is not a well practice to the majority of people. 

> "even brief mental blocks created by shifting between tasks can cost as much as 40 percent of someone's productive time" (https://www.apa.org/topics/research/multitasking)

When working with AI the amount of time of the feedback could be between from 5 seconds to 2 or more minutes. Well, what happens during that time? What you should do? After experience you can predict the amount of time needed for the model. For simple task, it is quite predictable but when you go in plan or research mode, or even multiple files edition you can't really predict. All Ai tools are improving this time perception by output some kind of steps, todos, intermediary results, and it's nice because you can choose to stay focus and read what happens to have a better understanding and start the review in a work in progress manner. But often, when there is too many steps or just too many time, you loose the flow. 

I've tried to manage two user stories in two IDE, launch a task and switch between the other. For the majority of case, to be honest, I think it burns my head, but when the switch between projects are some kind homogeneous - quite same amount of time, quite same amount of tasks, I found it manageable. But the question remains what kind of AI task could be launch without breaking the flow. Some people know that big task that take a lof time has to be launched when you take a little break or coffee. 

### Joy of crafting
The shift in the role of developer as an orchestrator can lead to something that break some kind of joy or pleasure. A lot of developers, I think, love solving problems, it is like a cognitive battle, very stimulating effort. Side note, everybody know that during this battle, the failures are part of all the learning process to know what paths had been wrong, what alternatives and tradeoffs has been taken. The first tries of using AI tools break a lot of this joy, to craft yourself, discuss with other people, pass to somekind of obstacles and failures to finally find the solution that fits well with the context of the project. Dealing with AI assistants and re-finding the joy of crafting, be part of the process is a non trivial challenge. 

> Lawmakers as programmers?!  (https://youtu.be/8rABwKRsec4, The New Code — Sean Grove, OpenAI)

I found also that dealing with specifications files generates a distinction betweeen developers profiles. Some want to code first, and evolve the specifications organically during the work in progress. Writing all before can lead to a waterfall process, and desengaging process. Some can think: "one more process", despite the code is the only real interface and living implementation of the product. It feels bureaucratic. The "make it work" joy of hacking is replaced by the "specify it correctly" drudgery of prompt engineering. It turns coding into a compliance task.

I found myself that there is a paradox of spec driven. I’m writing more documentation than ever, but for some of them I’m not writing it for my team. I’m writing it for the LLM. Docs are not really the same for humans and LLM. To get high-quality code generation, "Context is King." So we write ultra-verbose specifications, rigorous typing, and detailed comments, not because a human needs them to understand the flow, but to constrain the model’s search space. The promise of a documentation-oriented development through markdown files lead to two sets of documentations. A part of LLM docs are very conter-intuitive, the content rely of previous hallucinations, some CAPITAL WORDS, DO and DON'T specific to their non-deterministic behavior. And the weirdest thing is that finally, you will ask to the LLM to write instructions for itself according last failures. You are just a human "gateway". 


### Team
As Martin Fowler said: 
> "How do we best operate with AI in the team environment? We're still learning how to do this." (https://newsletter.pragmaticengineer.com/p/martin-fowler)

Using AI in a company is not a clear path, it has to be though at an organization level:
> Successful AI adoption requires more than just tools. Our new DORA AI Capabilities Model identifies seven foundational practices—including a clear AI policy, a healthy data ecosystem, and a user-centric focus—that are proven to amplify the positive impact of AI on organizational performance. (DORA Report)

The problem of more : more pr reviews, more Code = same amount of people
plus de code, plus de revue, plus de PR, plus de feeback avec des temps difference, plus de branches reliées entre elles, en attente de validation

The problem of empathy and deresponsabilisation: some people can be tempted to give more confidence in LLM that his team. 
- problème: sert à justifier des décisions: biais de confirmation, ne fait pas confiance aux autres membres de l'équipe -> CONFIANCE, DERESPONSABILISER



