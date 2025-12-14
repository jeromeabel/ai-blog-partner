# AI Blog Partner ✍️🤖

A multi-agent system powered by **Google ADK** (Agent Development Kit) to assist in writing high-quality, authentic technical blog posts.

## 🌟 Vision
This isn't just an "AI writer." It's a **Partner System** designed to:
*   Act as a **Senior Technical Editor** (Scribr) who challenges your ideas and structures your narrative.
*   Act as an **English Language Coach** (Linguist) who fixes non-native errors while teaching you *why*.
*   Enforce strict "No-Hype" and "Authenticity" rules to avoid generic AI slop.

## 🏗️ Architecture

### The Multi-Agent System

This system uses **four specialized agents** working together:

#### 1. **Scribr** (The Senior Technical Writer)
- **Role:** Strategic writing partner, editor, and structurer
- **Persona:** Former Junior Frontend Engineer turned Editor - deeply technical, skeptical of hype, radically human
- **Voice:** Authentic, peer-to-peer (Dev-to-Dev), no corporate fluff
- **Core Philosophy:** "System Thinking" meets "Radical Humanism"
- **Responsibilities:**
  - **Strategist:** Brainstorming, finding the "Angle," identifying audience and objections
  - **Drafter:** Structuring the narrative (Inverted Pyramid, RFC, or War Story)
  - **Editor:** Polishing text, enforcing "No-Hype" and "Authenticity" rules

#### 2. **Linguist** (The English Language Coach)
- **Role:** Dedicated language mechanic for non-native speakers
- **Persona:** Supportive peer reviewer
- **Responsibilities:**
  - Implicitly fixing minor errors
  - Identifying "French-to-English" patterns
  - Explaining grammar rules (the "Why")
- **Constraint:** Strictly silent on style and content; focuses ONLY on language mechanics

#### 3. **Orchestrator** (The Workflow Manager)
- **Role:** Manages the 6-step pipeline and state
- **Responsibilities:**
  - Executes the workflow sequentially
  - Handles file operations (reading drafts, saving outputs)
  - Delegates tasks to Scribr and Linguist
  - Uses LoopAgents for automatic quality retries

#### 4. **Validation Agents** (Quality Control)
Custom `BaseAgent` validators that ensure output quality through automatic retries:

- **OutlineValidationChecker:** Validates blog outline structure (3+ sections, intro, conclusion)
- **ContentSplitValidationChecker:** Validates content integrity (no lost/added/duplicated content)

**LoopAgent Pattern:**
```python
robust_outline_step = LoopAgent(
    sub_agents=[
        outline_creator,           # Worker: creates the outline
        OutlineValidationChecker   # Validator: checks quality
    ],
    max_iterations=3  # Retry up to 3 times
)
```

---

### The 6-Step Pipeline

#### **Step 1: Draft to Outlines** ✅ Complete
- **Input:** Raw draft from `inputs/<blog_id>/draft.md`
- **Action:**
  1. `robust_outline_step` (LoopAgent): Scribr analyzes draft and creates outline (with validation retries)
  2. `robust_content_split_step` (LoopAgent): Splits content into matching/unused chunks (with validation retries)
  3. Orchestrator saves outputs using `save_step_tool`
- **Output:** `outlines.md`, `draft_ok.md`, `draft_not_ok.md`
- **Quality Assurance:** Automatic retries on validation failure

#### **Step 2: Organization** ⏳ In Progress
- **Input:** `outlines.md`, `draft_ok.md`
- **Action:** Reorganize text chunks to match outline structure
- **Output:** `draft_organized.md`

#### **Step 3: Drafting & Research**
- **Input:** `outlines.md`, `draft_organized.md`
- **Action:** Iterative writing loop per section
  - Scribr expands/rewrites sections, checking data sources (Google Search)
  - Linguist monitors input/output for language corrections
- **Output:** `draft_nice.md`

#### **Step 4: Polishing**
- **Input:** `draft_nice.md`
- **Action:** Scribr applies final "No-Hype" and style rules
- **Output:** `draft_polished.md`

#### **Step 5: Finalization**
- **Input:** `draft_polished.md`
- **Action:** Formatting, SEO meta descriptions, final checks
- **Output:** `final.md`

#### **Step 6: Illustration (Optional)**
- **Action:** Brainstorming and generating cover art ideas
- **Output:** `illustration_ideas.md`

## 📂 Project Structure

```
├── blogger/                   # Main package
│   ├── agents.py              # Agent definitions (Scribr, Linguist)
│   ├── instructions/          # Markdown system prompts for agents
│   ├── tools.py               # File operation tools (read, save)
│   ├── validation_checkers.py # BaseAgent validators for LoopAgent quality control
│   ├── validation_utils.py    # Pure functions for validation logic (testable)
│   ├── workflow.py            # Orchestrator agent managing 6-step pipeline
│   └── step_agents/           # Step-specific agents
│       └── step_1_outline.py  # Draft to outlines agents (LoopAgents)
├── tests/                     # Unit tests (pytest)
│   └── test_validation_utils.py  # 29 tests, 100% coverage
├── inputs/                    # Your raw drafts go here
│   └── <blog_id>/
│       └── draft.md
├── outputs/                   # AI-generated results go here
│   └── <blog_id>/
│       ├── outlines.md
│       ├── draft_ok.md
│       └── ...
├── learning/                  # Learning materials (Teacher/Student protocol)
│   ├── GUIDE.md               # How to use the learning system
│   ├── PROGRESS.md            # Status tracker & roadmap
│   ├── UPDATE_PROTOCOL.md     # When to update which files
│   ├── lessons/               # Completed concepts (reference material)
│   ├── plans/                 # Current task plan
│   └── archive/               # Old files
├── README.md                  # This file - project overview
└── CLAUDE.md                  # Instructions for Claude Code (AI teacher)
```

## 🚀 Getting Started

### 1. Setup Environment

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install google-adk pytest pytest-cov
```

### 2. Configure API Key

Create a `blogger/.env` file with your Google API key:
```bash
GOOGLE_API_KEY=your_key_here
```

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=blogger --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS
# Or: xdg-open htmlcov/index.html  # On Linux
```

### 4. Run the Agent (Coming Soon)

```bash
# Interactive mode (planned for Phase 3)
adk web

# CLI mode (planned for Phase 3)
adk run blogger_agent
```

**Current Status:** Phase 2.1 Complete (Validation & Testing Infrastructure)

## 🧪 Testing

This project follows test-driven development principles:

- **Unit Tests:** `tests/test_validation_utils.py` (29 tests, 100% coverage)
- **Pure Functions:** Validation logic extracted to `blogger/validation_utils.py` for easy testing
- **Coverage:** Run `pytest --cov=blogger --cov-report=term-missing` to see coverage

**Test Categories:**
- Outline structure validation
- Content integrity checks (no lost/added/duplicated content)
- Edge cases (empty input, whitespace, case sensitivity)

## 🧠 Learning Journey

This project is built using a **"Teacher/Student" protocol** to master Google ADK:

- **Phase 1 (Complete):** Agent definitions, tools, workflow skeleton
- **Phase 2.1 (Complete):** Validation checkers, LoopAgent pattern, testing infrastructure
- **Phase 2.2 (In Progress):** Organization step
- **Phase 2.3-3 (Planned):** Drafting, polishing, SEO, CLI interface

Check [learning/PROGRESS.md](learning/PROGRESS.md) to see what we've learned at each step!

**Learning Materials:** See `learning/` folder for detailed lessons, progress tracking, and task plans.

## 👤 Author
**Jérôme Abel**
*   🌐 Website: [dev.jeromeabel.net](https://dev.jeromeabel.net/)
*   🐙 GitHub: [@jeromeabel](https://github.com/jeromeabel)