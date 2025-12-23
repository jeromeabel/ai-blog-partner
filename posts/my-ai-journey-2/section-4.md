## 4. The Opportunities

Let's focus on the interesting parts of this shift

### Prototype in YOLO mode

Despite all negative impacts of vibe-coding, or accepting AI outputs only when the behavior is ok without regarding in details, I found some useful use cases on the YOLO mode. 
- In UX/UI, with Figma Make, trying some variations of the same feature to explore differents designs and interactions. It builds a "variations" app with a switch selector or some kind of list of variations and tweak them for one or two hours. That feel like a pre-prototype quite useful to discuss with the team, even if it is not perfect. 
- Direcly in code, adding a simple feature from an orchestrator perspectice, just to see & test the feature working in a preview branch. It helps to write the specifications, requirements in the real context.  After the experimentation I can ask for an implementation plan that I can tweak to preserve the main coding ideas. The optimization phase, even from scratch will benefit from this plan.
- For non-dev team member, closed to the business rules, it is really powerful. They can focus on the ideas around the business needs like internal tools, strategic reports. In fact, I think it participates to propogate a ubuquitous langage inside the organization. It's like everyone is experimenting Writing specs and tweak them; it can be very hard, to be really explicit. And see the result Spec to Code can be a real learning thing for non-dev to understand what could happen in team where each task is delegated.

### Understand current Workflows

A positive side effect of AI adoption is that it forces to re-think about each step of your current workflow, taking a overall overview of what you do daily / weekly, and the relationships with your team. Indeed, the first approach I've tried, is where and how can I put AI to help in my work.

It's like spliting all of our processes in tasks or micro tasks to understand how can I use AI; understanding their order, some organic loops like (refine iterations). I like to think about it like a catalogue or répertoire of tasks, processes & artefacts; like the Refactoring book from Martin Fowler where each task of the refactoring process has a name. It feels also very close to what happens in sport: a movement, a action has a name and you can compose them to achieve the goal.

This initiative will certainly create some news in your workflow and engage a positive loop to make a habit of consistent introspection and small improvements

### Re-thinking Documentation

https://refactoring.fm/p/how-engineering-docs-change-with (luca rossi with Dennis Pilarinos)
> In my experience, docs have three main failure modes: They don't exist, They can't be trusted, They can't be found 

It's well known that documentation is something painful, it takes a long time, developers often prefer just read the code, it becomes obsolete. Like the debates about comments have been often so dividing. Obsolete or useless text can be considered as "noise" and increase the cognitive load. 

Now, creating and updating a documentation file is a lot easier, It continues to take time to review and refine, but it's far less painful. Generating doc strings to help understand critical functions is also a lot easier. 

Even if some documentation serve a limited time for a specific purpose, generates a mermaid diagram or markdown table  of how files and functions communicate each other offer a pretty efficien overview of a limited area of the codebase. Very useful when you don't know it before implementation.

The debates remain, but I tend to think more documentation is acceptable, if some attention is disciplined to update them; I guess the cost of updating is far less, developers will feel it's no more painful.

As AI tools/agents outputs are way better with the right context aka documentation files, it forces a minimal and updatedset of  documentation of crucial understanding of the project: description, architecture, stack & dependencies, files structure, commands, tests, coding guidelines. It forces also to write clearly the good and bad patterns of the project. A clean and fresh state for any onboarding. It feels also like documentation becomes a 'living-documentation', something we can trust, discuss, refine. A source of truth of the project.


### Re-thinking Code & Specifications artifacts

![[https://substackcdn.com/image/fetch/$s_!aw-J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F198d7f3a-0a59-444f-a3c2-ad393d6841e2_1702x990.png]]
( The pyramid of docs, https://refactoring.fm/p/how-engineering-teams-use-ai, luca rossi)

The shift in our role as developer is you become some kind of orchestrator, managing coding agents, as a Product Manager, but with code we could say. The importance of specifications files crucial, as it serves as a context file for LLMs to generate the most value of LLM output.

It is now well accepted that to have a better implementation, you must start by creating a plan file. It is a great way to improve the output. Some tools has a "plan" mode now. For a feature you could have at least two or three files: the user story (or derivated spec file), the plan that could serve as a brainstorming phase and then for implementation with details (with tasks, subtasks and workflows), when you can follow the progression. It also very convenient to use this file a memory and trace to drive the LLM when you clear the context to avoid hallucinations, start a fresh new chat or when you rework on the tasks from yesterday. 

![[spec-kit-dev-workflow.png]]
Some spec-driven development frameworks involve even more files, like spec-kit (https://speckit.org/), where for an implementation it produces 4 or more files to explicit a maximum of things for the LLM

It's a funny idea that the more important artefacts could be markdown files! Managing all these mardown files create open questions about the coding tasks compared to others. 

> Coding is an incredible skill an asset. But it's not the end goal. Engineering is the precise exploration (by humans) of software solutions to humans problems.
> The Code is 10-20% of your impact; The other 80-90% is the structured communication (talk, understand, distill, ideate, plan, share, translate, test, verify)
> A written specification is what **enables** you to **align humans** - it's the artifact that you discuss, debate, refer to, and sync on.
> Specifications, not prompts or code, are becoming the fundamental unit of programming. (https://youtu.be/8rABwKRsec4, The New Code — Sean Grove, OpenAI)

It's like when for a feature, we start the discussion with the what, with implementations details. It hides the real meaning, the real need of the feature, the "Why", high-level analysis and solutions. In fact, explicit specifications is a trade-off game, very challenging, because you have to connect some people together to share ideas and have a common solution to implement. Talking to LLM, create docs and intermediate files help to understand what is the need, because we take more time to define it, because the tools need it.

> Vishal Kapour on X https://x.com/figelwump: "One thing coding with agents does is it exposes how underbaked your thinking on the details of a product really are. They'll do some stuff that isn't what you wanted, and then you realize you never told it what you wanted, and maybe never fully understood it yourself"

As AI is an amplifier, a side effect is that source documents like the first step of a workflow are extremly important, and need careful human reviews, because, as Dexter Horthy said in https://youtu.be/IS_y40zY-hc, Advanced Context Engineering for Agents, a bad line of plan can result to 10-100 bad line of code:
![[human-leverage-dexter-horthy.png]]


### Redefining Interactions

Another great area of questions remains in the process of interacting with IDE, tools, machines. All these agents, intermiediaries steps, the multimodality (writing, voice, image) I think a great opportunity to redefine the human interaction to machine. Human tend to need communication, and love it, a lot. Speak to a machine like a human, describe things in a natural language rather than a machine langage seems an irresistible human temptation. Even the conversation itself is a new topic to explore. Working not with pure commands, but with a llm black box engine with unpredictable result is certainly a new way of experimenting things in our machine mirrors. As always, all of this is an exploration of our behaviors and "envies"/desires. For a developer, that need to wok in solo with its proper feedbacks, now it can ask some helpful tasks to a assistant and do some brainstorming with it. The crucial need now is to gain some control on quality and reliability, but also to make a real and challenging deep creative brainstorming with this bag of words, and images. as always it is a matter of control/limit and freedom, and society be taking into account to manage, to choose. 





