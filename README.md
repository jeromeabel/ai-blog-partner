# AI Blog Partner ✍️🤖

A multi-agent system powered by **Google ADK** (Agent Development Kit) to assist in writing high-quality, authentic technical blog posts.

## 🌟 Vision
This isn't just an "AI writer." It's a **Partner System** designed to:
*   Act as a **Senior Technical Editor** (Scribr) who challenges your ideas and structures your narrative.
*   Act as an **English Language Coach** (Linguist) who fixes non-native errors while teaching you *why*.
*   Enforce strict "No-Hype" and "Authenticity" rules to avoid generic AI slop.

## 🏗️ Architecture

The system uses a 6-step pipeline managed by an orchestrator:

1.  **Draft to Outlines:** Collaborative brainstorming and structuring.
2.  **Organization:** Auto-rearranging your draft to fit the agreed outline.
3.  **Drafting:** Iterative section-by-section writing with real-time coaching.
4.  **Polishing:** Final style pass (No-Hype check).
5.  **Finalization:** SEO and formatting.
6.  **Illustration:** Cover art generation (Optional).

See [AGENTS.md](AGENTS.md) for detailed agent personas and workflows.

## 📂 Project Structure

```
├── blogger/                   # Main package
│   ├── agents.py              # Agent definitions (Scribr, Linguist)
│   ├── instructions/          # Markdown system prompts for agents
│   ├── tools.py               # File operation tools (read, save)
│   ├── validation_checkers.py # BaseAgent validators for LoopAgent quality control
│   ├── validation_utils.py    # Pure functions for validation logic (testable)
│   └── workflow.py            # Orchestrator agent managing 6-step pipeline
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
├── PROGRESS.md                # Project status and learning log
├── LESSON_*.md                # Step-by-step teaching guides
└── VALIDATION_DESIGN.md       # Content integrity validation design doc
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
- **Phase 2.2-2.3 (In Progress):** Core workflow implementation
- **Phase 3 (Planned):** Polishing, SEO, CLI interface

Check [PROGRESS.md](PROGRESS.md) to see what we've learned at each step!

## 👤 Author
**Jérôme Abel**
*   🌐 Website: [dev.jeromeabel.net](https://dev.jeromeabel.net/)
*   🐙 GitHub: [@jeromeabel](https://github.com/jeromeabel)