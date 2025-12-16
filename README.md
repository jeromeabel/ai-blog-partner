# AI Blog Partner ✍️🤖

A multi-agent system powered by **Google ADK** (Agent Development Kit) to help you transform raw drafts into polished technical blog posts through **interactive collaboration**.

## 🌟 Philosophy: The Interactive Partner

This isn't an automated AI writer. It's a **collaborative partner system** that works *with* you, not *for* you.

**Core Principles:**
- **No Black Box:** You approve every step before moving forward
- **Conversational:** Natural dialogue, not rigid automation
- **Specialized Agents:** Each agent has one clear role
- **No Hype:** Enforces authentic, technical writing (no "delve", "leverage", "revolutionary")
- **You Stay in Control:** The AI suggests, you decide

---

## 🚀 Quick Start

### Installation

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install google-adk
```

### Setup API Key

Create `blogger/.env` with your Google API key:
```bash
GOOGLE_API_KEY=your_key_here
```

### Run It!

**Option 1: Guided Workflow (Recommended)**
```bash
# Web UI - Visual chat interface
adk web

# Or CLI - Terminal chat
adk run blogger
```

**Option 2: Agent Testing (For Development)**
```bash
# Test individual agents
python -m blogger.playground --agent architect
python -m blogger.playground --agent scribr
```

---

## 🎯 Two Modes of Interaction

### 1. 🌐 Guided Workflow (`adk web`)

**For:** Creating blog posts through a conversational experience

The **Coordinator** agent guides you through 3 steps:
1. **The Architect** - Brainstorm outline structure
2. **The Butcher** - Split draft into sections *(coming soon)*
3. **The Writer** - Polish each section *(coming soon)*

**How it works:**
```
You: I want to create a blog post for my-ai-journey-2

Coordinator: Great! Let me load your draft...
[Reads your draft]
I see themes about AI adoption, productivity myths, and team friction.
What's the core message you want readers to take away?

You: The organizational challenges, not the technical ones.

Coordinator: Perfect. Let me call the Architect to brainstorm structure...
[Calls Architect agent]

Architect: I see two possible angles:
A) "Hype → Reality" (journey arc)
B) "Hidden Costs" (myth-busting)
Which resonates with your draft?

You: B - I want to warn people about non-obvious impacts

Architect: Great! Here's a structure...
[Proposes outline, gets your feedback, iterates]

You: This looks good, save it!

Coordinator: Saved to outputs/my-ai-journey-2/outline.md
Ready for Step 2 when we build it!
```

### 2. 🛝 Playground (`playground.py`)

**For:** Quick agent testing during development

```bash
# Test the Architect agent
python -m blogger.playground --agent architect

You: Read my-ai-journey-2 and help me create an outline
Architect: [Brainstorms with you directly]
```

**Great for:**
- Debugging agent behavior
- Quick iterations on agent instructions
- Testing file I/O tools

---

## 🏗️ Architecture

### The 3-Step Process

```
Step 1: The Architect  🏗️  [✅ Complete]
Draft → Outline
- User pastes/loads raw draft
- Architect brainstorms structure with user
- Scribr polishes titles (removes hype)
- User approves → saves outline

Step 2: The Butcher  🔪  [⏳ Coming Soon]
Outline → Sections
- Deterministic splitting tool
- Matches content to outline structure
- Creates section files

Step 3: The Writer  ✍️  [⏳ Coming Soon]
Polish Sections
- Iterative editing per section
- User feedback loop
- Final assembly
```

### The Agent Team

**Coordinator** - Conversational Guide
- Guides you through the 3-step process
- Calls sub-agents at appropriate times
- **NOT automated** - waits for your approval

**Architect** - Structural Thinker (Step 1)
- Brainstorms outline structures
- Suggests 2-3 angles (Problem→Solution, Story Arc, etc.)
- Iterates based on your feedback
- Calls Scribr for title polishing

**Scribr** - Style Enforcer
- Senior Technical Writer persona
- Enforces "No-Hype" rules
- Removes LLM-isms: "delve", "leverage", "paradigm shift"
- Polishes titles to be specific, not generic

**Linguist** - Language Coach
- Grammar and clarity expert
- Fixes non-native patterns
- Explains the "why" behind corrections

---

## 📁 Project Structure

```
ai-blog-partner/
├── blogger/                    # Main package
│   ├── __init__.py            # ADK App export (for adk run/web)
│   ├── coordinator.py         # Conversational workflow guide
│   ├── playground.py          # Developer testing tool
│   ├── agents.py              # Base agents (Scribr, Linguist)
│   ├── tools.py               # File I/O tools
│   ├── utils.py               # Helper functions
│   ├── step_agents/           # Step-specific agents
│   │   ├── architect.py       # ✅ Step 1: Draft → Outline
│   │   ├── butcher.py         # ⏳ Step 2: Outline → Sections
│   │   └── writer.py          # ⏳ Step 3: Polish Sections
│   ├── instructions/          # Agent system prompts
│   │   ├── coordinator.md     # Coordinator instructions
│   │   ├── architect.md       # Architect instructions
│   │   ├── scribr.md         # Scribr "No-Hype" rules
│   │   └── linguist.md       # Linguist grammar rules
│   └── archive/               # Old automated system (deprecated)
├── inputs/                    # Your raw drafts
│   └── <blog_id>/
│       └── draft.md
├── outputs/                   # Generated results
│   └── <blog_id>/
│       ├── outline.md
│       ├── outline_v1.md
│       └── ...
├── learning/                  # Development journey docs
│   ├── PROGRESS.md           # Current status & roadmap
│   ├── lessons/              # Lessons learned
│   └── plans/                # Implementation plans
├── tests/                    # Unit tests
├── README.md                 # This file
├── AGENTS.md                 # Architecture philosophy
└── DEVELOPMENT.md            # Developer guide
```

---

## 🧑‍💻 Development Guide

### Testing Individual Agents

The playground is your best friend for development:

```bash
# Test the Architect
python -m blogger.playground --agent architect

# Test Scribr (style checker)
python -m blogger.playground --agent scribr

# Test Linguist (language coach)
python -m blogger.playground --agent linguist
```

### Building a New Agent

1. **Create the agent** in `step_agents/`
   ```python
   from google.adk.agents import Agent
   from blogger.utils import read_instructions

   new_agent = Agent(
       name="new_agent",
       model="gemini-2.5-flash",
       instruction=read_instructions("new_agent.md"),
       tools=[...],
   )
   ```

2. **Write instructions** in `instructions/new_agent.md`
   - Keep it simple and focused
   - Clear role and constraints
   - Examples help

3. **Register in playground** (`playground.py`)
   ```python
   AGENTS = {
       "architect": architect,
       "scribr": scribr,
       "new_agent": new_agent,  # Add here
   }
   ```

4. **Test interactively**
   ```bash
   python -m blogger.playground --agent new_agent
   ```

5. **Add to coordinator** when ready
   ```python
   coordinator = Agent(
       sub_agents=[architect, new_agent],
       ...
   )
   ```

### Testing the Full Workflow

```bash
# Web UI (best for testing full conversations)
adk web

# Start a conversation
You: I want to create a blog post for my-ai-journey-2
```

### Running Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=blogger --cov-report=html
```

---

## 📖 How It Works: Step 1 (The Architect)

Let's walk through creating an outline for a blog post:

### 1. Prepare Your Draft

Create `inputs/my-blog/draft.md`:
```markdown
# My thoughts on AI tools

- AI tools are hyped
- Productivity is complicated
- Teams struggle with adoption
- Junior developers are affected
...
```

### 2. Start the Workflow

```bash
adk web
```

### 3. Chat with the Coordinator

```
You: I want to create a blog post for my-blog

Coordinator: Let me load your draft...
I see you have thoughts about AI tools, productivity, and team adoption.
Let me call the Architect to help structure this.

Architect: I've read your draft. What's the core message?

You: The organizational challenges teams face when adopting AI

Architect: Got it. I see two angles:
A) "Journey Arc" (Hype → Reality → Adaptation)
B) "Myth-Busting" (Promises vs Reality)

You: B - I want to bust myths

Architect: Perfect. Here's a structure...

# The Hidden Costs of AI Adoption

## 1. The Productivity Myth
[What this section covers...]

## 2. The Team Friction Reality
[What this section covers...]

## 3. The Junior Developer Gap
[What this section covers...]

What do you think?

You: Love it! But can we combine sections 2 and 3?

Architect: Great idea! Let me adjust...
[Shows revised outline]

You: Perfect, save it!

Coordinator: Saved to outputs/my-blog/outline.md
```

### 4. Find Your Outline

Check `outputs/my-blog/outline.md` - ready for Step 2 when we build it!

---

## 🎨 Key Features

### Version-Aware Iteration

The Architect supports multiple outline versions:

```bash
You: Read outputs/my-blog/outline_v1.md and outline_v3.md
     Compare them and tell me what improved

Architect: In v1, you had generic "Introduction" labels.
           In v3, you added emotional hooks like "The Guilt of Falling Behind"
           and target emotions. The structure is much stronger.

You: Can you help me fix the weak sections in v3?

Architect: Sure! Section 4 feels incomplete...
```

### Meta-Commentary Support

Add notes to your outlines:

```markdown
## 1. The Opening Hook
*Target Emotion: Relief & Connection*

Why this works: validates reader anxiety before diving into solutions
```

The Architect respects and builds on your meta-commentary.

### File-Based Workflow

No session state, no hidden data:
- Drafts in `inputs/<blog_id>/draft.md`
- Outlines in `outputs/<blog_id>/outline.md`
- Everything is readable, editable markdown files

---

## 🧠 Learning Journey

This project documents the learning process of building with Google ADK:

### Timeline

**2024-12-14 to 2024-12-15:** OLD System (Abandoned)
- Attempted automated orchestrator with session state
- Built LoopAgents for quality control
- Complex 6-step pipeline
- **Why abandoned:** Over-engineered, black-box, didn't match vision

**2024-12-16+:** NEW System (Interactive Partner)
- ✅ Phase 1: Foundation & The Architect
- ⏳ Phase 2: The Butcher (content splitting)
- ⏳ Phase 3: The Writer (section polishing)

### Lessons Learned

See `learning/lessons/phase1-reboot.md` for detailed insights:
- File tools > Terminal pasting
- Simplicity > Complex instructions
- Team collaboration (Architect + Scribr) > Solo agents
- Interactive > Automated

**Progress Tracker:** `learning/PROGRESS.md`

---

## 🎯 Current Status

**✅ Ready to Use:**
- Step 1: The Architect (Draft → Outline)
- Interactive playground for agent testing
- `adk web` guided workflow

**⏳ Coming Soon:**
- Step 2: The Butcher (Outline → Sections)
- Step 3: The Writer (Polish Sections)

**Try it now:**
```bash
adk web
```

---

## 📚 Documentation

- **README.md** (this file) - Overview and getting started
- **AGENTS.md** - Architecture philosophy and design decisions
- **DEVELOPMENT.md** - Detailed development guide
- **learning/** - Development journey and lessons learned

---

## 👤 Author

**Jérôme Abel**
- 🌐 Website: [dev.jeromeabel.net](https://dev.jeromeabel.net/)
- 🐙 GitHub: [@jeromeabel](https://github.com/jeromeabel)

---

## 🤝 Contributing

This is a learning project, but feedback and suggestions are welcome! Check the issues or start a discussion.

---

## 📄 License

See LICENSE file for details.
