# Progress

**Current Phase:** Complete (Version 1.0)
**Next Task:** User Feedback & Feature Requests
**Active Plan:** None

---

## Roadmap

### ✅ Phase 1: The Architect
- [x] Playground infrastructure
- [x] Architect agent (draft → outline)
- [x] Scribr sub-agent (title de-hyping)
- [x] File I/O tools

### ✅ Phase 2: The Curator
- [x] Validation utilities
- [x] Validation tools (content split, organization)
- [x] Curator agent (filter & organize)
- [x] Two-phase workflow (Filter → Organize)
- [x] Debugging & refinement (2025-12-18)

### ✅ Phase 3: The Writer
- [x] Section manipulation tools (read, save, finalize)
- [x] Writer agent implementation
- [x] Scribr sub-agent integration
- [x] Section-by-section polishing workflow
- [x] Integration with coordinator & playground

### ✅ Phase 4: The Analyzer (Foundation)
- [x] Content analysis tools
- [x] Gap detection (Light mode analysis)
- [x] Suggestion agent (Analyzer Agent)

### ✅ Phase 5: Analyzer Deep Mode
- [x] Chunk extraction
- [x] Connection mapping
- [x] Deep mode strategy
- [x] Architect & Curator integration

### ✅ Phase 6: Integration & Refinement
- [x] Coordinator sub-agent integration
- [x] Coordinator instructions update
- [x] Roadmap & documentation synchronization

### Feedback & Feature Requests
- Rewrite current section files does not work. The read section tool output draft_organized with chunk, not the most recent version of section like section_1.md
- Difference between SKILLS https://agentskills.io/what-are-skills and Agents in ADK
- Change LLM API: Claude API instead of GEMINI -> models, centralize config? https://google.github.io/adk-docs/agents/models/#using-anthropic-models
- Analysis process too long - Needs to save tokens
- It seems that a lot of events send all characters from draft: time consuming, token consuming?
- Analysis document efficient, useful for next agents?
- Improve chunk process (use of "---", use of "##", use of "###"), keep quotes source, author link or make reference notes as ID. Improve quotes & commentary: If there is a link or a name, it is a reference; if not, it is my note.
- not_ok.md: there are some interesting ideas
- Keep quotes as foot notes in markdown
- Writer can call save_tool
- English coach trigger?
- Does AGENTS.md meets https://agents.md/ recommandations?
- Configure Gemini CLI to use AGENTS.md in .gemini/settings.json: `{ "contextFileName": "AGENTS.md" }`
- FUTURE: save tokens and analyze better with vector base/chunk/RAG

---

## Quick Links

- Architecture: [/AGENTS.md](/AGENTS.md) as the single source of truth for LLM (CLAUDE.md & GEMINI.md should stay symbolic links)
- User Guide: [/README.md](/README.md)
- Lessons Learned: [/progress/lessons/](/progress/lessons/)
- Test Agents: `python -m blogger.playground --agent <name>`
- Test with Verbose: `python -m blogger.playground --agent <name> --verbose`
