"""
AI Blog Partner - Validation Checkers

Custom validation agents for LoopAgent quality control.
These agents check if outputs meet quality criteria and signal
the loop to exit (escalate=True) or retry.

Official ADK Docs:
- https://google.github.io/adk-docs/agents/custom-agents/
- https://google.github.io/adk-docs/events/
"""

from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai import types

from blogger.validation_utils import (
    check_content_integrity,
    check_outline_structure,
    normalize_and_split,
)


class OutlineValidationChecker(BaseAgent):
    """
    Validates blog outline quality for LoopAgent

    Checks:
    - Outline exists in session state (key: "blog_outline")
    - Has at least 3 sections (## markdown headings)
    - Contains Introduction and Conclusion sections

    Returns:
    - escalate=True if valid (exit loop)
    - continue loop if invalid (retry)
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # 1. Get outline from session state
        outline_text = ctx.session.state.get("blog_outline", "")

        # 2. Check outline structure using pure function
        is_valid, reasons = check_outline_structure(outline_text)

        # 3. Yield Event with escalate=True if valid, else regular Event
        if is_valid:
            # ✅ Quality check PASSED - exit loop
            # Count sections for success message
            sections = [line for line in outline_text.split("\n") if line.startswith("## ")]
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"✅ Outline validation passed: {len(sections)} sections found (intro, conclusion present)"
                        )
                    ]
                ),
                actions=EventActions(escalate=True),  # Stop Loop
            )
        else:
            # ❌ Quality check FAILED - continue loop (retry)
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"❌ Outline validation failed: {', '.join(reasons)}"
                        )
                    ]
                ),
                # ❌ No escalate - signals: CONTINUE LOOP (retry)
            )


class ContentSplitValidationChecker(BaseAgent):
    """
    Validates content split completeness and integrity.

    Checks:
    - Both draft_ok and draft_not_ok exist in session state
    - Combined length approximately equals original draft (±10%)
    - All content from raw_draft exists in draft_ok OR draft_not_ok (no lost content)
    - No new content was added (LLM should copy-paste, not generate)

    Returns:
    - escalate=True if valid (exit loop)
    - continue loop if invalid (retry)
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # 1. Get split content and original draft from session state
        content_split = ctx.session.state.get("content_split", {})
        raw_draft = ctx.session.state.get("raw_draft", "")

        # Extract the split parts
        draft_ok = (
            content_split.get("draft_ok", "") if isinstance(content_split, dict) else ""
        )
        draft_not_ok = (
            content_split.get("draft_not_ok", "")
            if isinstance(content_split, dict)
            else ""
        )

        # Check if both draft_ok and draft_not_ok exist
        if not draft_ok or not draft_not_ok:
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"❌ Content split incomplete: missing {'draft_ok' if not draft_ok else 'draft_not_ok'}"
                        )
                    ]
                ),
                # ❌ No escalate - signals: CONTINUE LOOP (retry)
            )
            return

        # 3. Compare combined length to original (±10%)
        original_len = len(raw_draft)
        combined_len = len(draft_ok) + len(draft_not_ok)

        if original_len == 0:
            # Edge case: no original draft
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(text="❌ No original draft found in session state")
                    ]
                ),
            )
            return

        variance = abs(combined_len - original_len) / original_len
        length_ok = variance <= 0.10  # Within ±10%

        # 4. Check content integrity (no lost/added/duplicated content)
        integrity_ok, integrity_error = check_content_integrity(
            raw_draft, draft_ok, draft_not_ok
        )

        # 5. Validate: both length AND integrity must pass
        is_valid = length_ok and integrity_ok

        # 6. Yield Event with escalate=True if valid
        if is_valid:
            # ✅ Validation passed (both length and integrity)
            num_raw_paragraphs = len(normalize_and_split(raw_draft))
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"✅ Content split validated: {combined_len} chars (original: {original_len}, variance: {variance:.1%}), {num_raw_paragraphs} paragraphs preserved"
                        )
                    ]
                ),
                actions=EventActions(escalate=True),  # ✅ Signal: STOP LOOP
            )
        else:
            # ❌ Validation failed - collect all failure reasons
            failures = []
            if not length_ok:
                failures.append(f"length variance {variance:.1%} exceeds ±10%")
            if not integrity_ok:
                failures.append(integrity_error)

            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"❌ Content split failed: {'; '.join(failures)}"
                        )
                    ]
                ),
                # No escalate - continue loop
            )
