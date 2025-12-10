IDEES.
- productivity/metrique: comment mesurer la productivité ?
- problème: sert à justifier des décisions: biais de confirmation, ne fait pas confiance aux autres membres de l'équipe -> CONFIANCE, DERESPONSABILISER
- problème: discussion où on s'adapte (ne comprend pas l'implicite) > effet pervers sur les autres discussions entre humains
- problème: organisation, équipe, adoption
- problème: flow / context switching
- intéressant: nouvelle interaction home/machine, la conversation -> sochratic method, This chain of thought -> PARTNER / HUMAN IN THE LOOP
	- duck buddy, comments conversation
	- Partner mode, explain changes, redo by hand
	- Language https://www.youtube.com/watch?v=yjLsHD9IzIA: # Why we're giving AI too much credit | Morten Rand-Hendriksen | TEDxSurrey
	- they are mirrors. Hack ourself, on ne comprend plus ce qui est artificiel et ce qui est humain => anxiété. Learning, Thinking, reasoning, training = human metaphor
	- Comme quand on voit deux rond noir => on pense que c'est un visage
		- -> https://www.experimental-history.com/p/bag-of-words-have-mercy-on-us (ChatGPT as a bag of words)
	- "Nous n'avons pas décider ou aller maintenant avec l'IA"
	- => "Assisted technologies"
- intéressant: se comprendre
- intéressant: challenge arts, challenge not being dumb
- intéressant: se questionner, introspection sur les gestes et étapes d'un workflow 


DevAI: Beyond Hype and Denial
https://www.ivankusalic.com/realistic-DevAI/

https://www.youtube.com/watch?v=-5_6HQR0WhA
L'état de l'adoption de l'IA dans les équipes d'ingénierie 📊 — avec Matt McClernan

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
- Alignement (Beast mode). Le créateur de Best Mode (agent for VS Code COPILOT) a lu toute la documentaion d'Open AI pour comprendre comment obtenir les meilleurs résultats avec leur modèle
• Le contexte est roi : la qualité des résultats de l'IA dépend directement de la qualité du contexte fourni. La documentation et les spécifications deviennent la source de vérité, des artefacts fondamentaux.

Updated Standards
> Language models can only reproduce language patterns from their training data. **They can't learn anything new**. 


### But Needs of Specific processes
- FILES/DOCS for AI or for Humans (!!!). Docs are not only for Human, ultra verbose to contrain the model, repetitive
- Déformation : traiter les humains comme des machines -> IHM

### 1 PROCESS MORE OR FEWer PROCESSES LESS ?

There are differents mindsets for developers. Time, Code artefact

Les profils dev "fonceurs", make it work first peuvent pas apprécier que la documentation, les spécifications prennent le pas sur la production de l'artefact le plus important le code. Encore une manière de détourner l'énergie

Conceptuel vs Organic: 1 process de plus -> bureaucraty, process > creativity, DIY, plaisir, human



### NON DETERMINISTIC
The Paradigm Shift: From Predictable Code to Unpredictable Agents (Google Whitepapers)
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
