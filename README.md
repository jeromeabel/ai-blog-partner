# AI Blog Partner

Transform raw drafts into polished technical blog posts through interactive AI collaboration.

**Philosophy:** Not an automated writer - a collaborative partner that works *with* you, not *for* you.

---

## Quick Start

### Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install google-adk
```

### Setup

Create `blogger/.env`:
```bash
GOOGLE_API_KEY=your_key_here
```

### Run

**Web UI (Recommended):**
```bash
adk web
```

**CLI:**
```bash
adk run blogger
```

---

## How It Works

### The 3-Step Process

Your blog post goes through three collaborative steps:

```
1. 🏗️ Architect    Draft → Outline
   Brainstorm structure together, approve outline

2. 🎨 Curator      Outline → Organized Sections
   Filter and organize content, validate integrity

3. ✍️ Writer       Sections → Polished Post
   Iterative polishing with your feedback
```

*For architecture details, see [AGENTS.md](AGENTS.md)*

---

## Example Session

```bash
$ adk web

You: Create a blog post from posts/my-post/draft.md

Coordinator: I've loaded your draft. I see themes about AI adoption
             and organizational challenges. Let me call the Architect
             to help structure this.

Architect: I see two possible angles:
           A) Journey arc (Hype → Reality → Lessons)
           B) Myth-busting (Promises vs Reality)
           Which fits your message better?

You: B - I want to challenge assumptions

Architect: Perfect. Here's a proposed structure...
           ## 1. The Productivity Myth
           ## 2. Hidden Team Costs
           ## 3. What Actually Works

           What do you think?

You: Great! Can we split section 2 into two parts?

Architect: Good idea. Here's the revised version... [shows updated outline]

You: Perfect, save it!

Coordinator: ✓ Saved to posts/my-post/1-outline.md
             Ready for Step 2 when you are!
```

---

## Development

### Testing Agents

```bash
# Test individual agents
python -m blogger.playground --agent architect
python -m blogger.playground --agent curator
python -m blogger.playground --agent scribr
```

### Building New Agents

See [AGENTS.md](AGENTS.md) for detailed development guide.

Quick version:

1. Create `blogger/agents/new_agent.py` and `new_agent.md`
2. Register in `blogger/playground.py`
3. Test: `python -m blogger.playground --agent new_agent`
4. Add to coordinator when ready

### Running Tests

```bash
# Unit tests
pytest blogger/tests/ -v

# With coverage
pytest blogger/tests/ --cov=blogger
```

---

## Project Structure

```
ai-blog-partner/
├── blogger/
│   ├── coordinator.py         # Main entry (adk web/run)
│   ├── playground.py          # Agent testing
│   ├── agents/                # Agent code + instructions
│   ├── utils/                 # Tools & utilities
│   └── tests/                 # pytest tests
├── posts/{blog_id}/           # Your drafts + generated files
└── progress/                  # Development tracking
    ├── PROGRESS.md            # Current status
    └── plans/                 # Task plans
```

---

## The Agent Team

**Coordinator**
Guides you through the 3-step process. Calls specialized agents when needed.

**Architect** (Step 1)
Brainstorms outline structures with you. Uses Scribr sub-agent to polish titles.

**Curator** (Step 2)
Filters draft content against outline, organizes into sections, validates integrity.

**Writer** (Step 3)
Polishes sections iteratively based on your feedback.

**Scribr**
Enforces technical writing style. Removes hype words: "delve", "leverage", "revolutionary".

**Linguist**
Grammar and clarity coach. Fixes non-native patterns, explains improvements.

---

## Key Features

**File-Based Workflow**
Everything is readable markdown. No hidden state.

**Version-Aware**
Compare and iterate on multiple versions:
```bash
You: Compare outline_v1.md and outline_v3.md

Architect: In v1, generic titles. In v3, emotional hooks.
           Structure is much stronger now.
```

**No Hype Enforcement**
Scribr removes AI-isms and marketing speak.

**Validation-First**
Curator validates content integrity - nothing gets lost.

---

## Documentation

- **README.md** (this file) - Getting started
- **AGENTS.md** - Architecture & development protocol (for LLMs & developers)
- **progress/PROGRESS.md** - Current roadmap

---

## Author

**Jérôme Abel**
- [dev.jeromeabel.net](https://dev.jeromeabel.net/)
- [@jeromeabel](https://github.com/jeromeabel)

---

## License

See LICENSE file.
