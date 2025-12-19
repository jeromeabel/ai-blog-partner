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

### The 4-Step Process

Your blog post goes through four collaborative steps:

```
0. 🔍 Analyzer     Draft → Analysis
   Assess complexity, extract chunks (Deep Mode), map connections

1. 🏗️ Architect    Draft + Analysis → Outline
   Brainstorm structure using analysis insights, approve outline

2. 🎨 Curator      Outline + Analysis → Organized Sections
   Filter and organize content using chunks, validate integrity

3. ✍️ Writer       Sections → Polished Post
   Iterative polishing with your feedback
```

*For architecture details, see [AGENTS.md](AGENTS.md)*

---

## Example Session

```bash
$ adk web

You: Create a blog post from posts/my-post/draft.md

Coordinator: I've loaded your draft. Let's start by analyzing it.

Analyzer: This draft is complex (Score: 8.5/10) with 15 detected quotes.
          I recommend running Deep Analysis to map connections.
          Proceed?

You: Yes, please.

Analyzer: Analysis complete. Found 8 high-scoring "anchor" quotes.

Coordinator: Great. Now I'll call the Architect to build an outline
             using those anchors.

Architect: Based on the analysis, I see two possible angles:
           A) Quote-Driven Journey (Karpathy → You → Lessons)
           B) Thematic Clusters (Philosophy vs Practice)
           Which fits your message better?

You: A - I like the narrative arc.

Architect: Perfect. Here's a proposed structure...
           ## 1. The Teacher's Voice (Anchor: Karpathy Quote)
           ## 2. The Student's Struggle
           ## 3. The Breakthrough

           What do you think?

You: Great! Save it.

Coordinator: ✓ Saved to posts/my-post/1-outline.md
             Ready for Step 2 (Curator) when you are!
```

---

## Development

### Testing Agents

```bash
# Test individual agents
python -m blogger.playground --agent analyzer --mode deep
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
Guides you through the process. Calls specialized agents when needed.

**Analyzer** (Step 0)
Pre-processes drafts. "Deep Mode" extracts chunks and maps connections for complex posts.

**Architect** (Step 1)
Brainstorms outline structures with you. Uses analysis to identify key anchors.

**Curator** (Step 2)
Filters draft content against outline, using analysis chunks for smarter organization.

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
