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
├── blogger/              # Main package
│   ├── agents.py         # Agent definitions (Scribr, Linguist)
│   ├── instructions/     # Markdown system prompts for agents
│   └── tools.py          # (Planned) File & System tools
├── inputs/               # Your raw drafts go here
├── outputs/              # AI-generated results go here
└── PROGRESS.md           # Project status and learning log
```

## 🚀 Getting Started

1.  **Setup Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install google-adk
    ```

2.  **Configure:**
    Create a `.env` file with your API key:
    ```bash
    GOOGLE_API_KEY=your_key_here
    ```

3.  **Run (Coming Soon):**
    *Current Status: In Development (Phase 1)*

## 🧠 Learning Journey
This project is built using a "Teacher/Student" protocol to master the Google ADK. Check [PROGRESS.md](PROGRESS.md) to see what we've learned!

## 👤 Author
**Jérôme Abel**
*   🌐 Website: [dev.jeromeabel.net](https://dev.jeromeabel.net/)
*   🐙 GitHub: [@jeromeabel](https://github.com/jeromeabel)