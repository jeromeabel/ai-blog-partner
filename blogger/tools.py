from pathlib import Path
import urllib.request
from urllib.error import URLError, HTTPError
import re
from google import genai

from blogger.text_utils import (
    extract_headings,
    find_best_heading_match,
    split_text_by_headings,
    check_content_integrity,
)

CURRENT_DIR = Path(__file__).parent.parent
INPUTS_DIR = CURRENT_DIR / "inputs"
OUTPUTS_DIR = CURRENT_DIR / "outputs"
draft_filename = "draft.md"


def read_draft_tool(blog_id: str) -> dict:
    """
    Retrieves the raw draft content for a blog post.

    Use this to load the initial draft markdown file that needs to be processed
    through the blog writing pipeline.

    Args:
        blog_id: Unique identifier for the blog (e.g., "my-ai-journey-2")

    Returns:
        Success: {"status": "success", "content": "...", "blog_id": "...", "path": "..."}
        Error: {"status": "error", "message": "Actionable error description"}
    """
    draft_path = INPUTS_DIR / blog_id / draft_filename
    if not draft_path.exists():
        return {
            "status": "error",
            "message": f"Draft file not found for blog_id '{blog_id}'. Check the blog_id and ensure draft.md exists in inputs/{blog_id}/",
        }
    try:
        with open(draft_path, "r") as f:
            content = f.read()
        return {
            "status": "success",
            "blog_id": blog_id,
            "path": str(draft_path),
            "content": content,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read draft file: {str(e)}",
        }


def save_step_tool(blog_id: str, step_name: str, content: str) -> dict:
    """
    Saves content from a pipeline step to a markdown file.

    Use this to persist the output of any pipeline step (e.g., outlines,
    organized draft, polished content) for the given blog.

    Args:
        blog_id: Unique identifier for the blog (e.g., "my-ai-journey-2")
        step_name: Name of the step (e.g., "draft_ok")
        content: Content to save for the step

    Returns:
        Success: {"status": "success", "blog_id": "...", "path": "...", "step_name": "..."}
        Error: {"status": "error", "message": "Actionable error description"}
    """
    try:
        output_path = OUTPUTS_DIR / blog_id / f"{step_name}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(content)

        return {
            "status": "success",
            "blog_id": blog_id,
            "path": str(output_path),
            "step_name": step_name,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to save step '{step_name}' for blog '{blog_id}': {str(e)}",
        }


def read_previous_content_tool(blog_id: str) -> dict:
    """
    Retrieves the content of a previous blog post.

    Use this to load the content of a previous blog post to avoid overlap.
    Checks for content.md, index.md, or final.md in inputs/<blog_id>/.

    Args:
        blog_id: Unique identifier for the previous blog (e.g., "my-ai-journey-1")

    Returns:
        Success: {"status": "success", "content": "...", "blog_id": "...", "path": "..."}
        Error: {"status": "error", "message": "Actionable error description"}
    """
    # Try multiple possible filenames
    possible_files = ["content.md", "index.md", "final.md", "draft.md"]
    content_path = None
    
    for filename in possible_files:
        path = INPUTS_DIR / blog_id / filename
        if path.exists():
            content_path = path
            break
            
    if not content_path:
        return {
            "status": "error",
            "message": f"Content file not found for blog_id '{blog_id}'. Checked: {', '.join(possible_files)} in inputs/{blog_id}/",
        }
    try:
        with open(content_path, "r") as f:
            content = f.read()
        return {
            "status": "success",
            "blog_id": blog_id,
            "path": str(content_path),
            "content": content,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read content file: {str(e)}",
        }


def read_file_tool(file_path: str) -> dict:
    """
    Reads any markdown file from the project.

    Use this to read outline drafts, previous versions, or any other markdown files
    the user references. Accepts both relative paths (from project root) and full paths.

    Args:
        file_path: Path to the file (e.g., "outputs/my-ai-journey-2/outline_v1.md")

    Returns:
        Success: {"status": "success", "content": "...", "path": "..."}
        Error: {"status": "error", "message": "..."}
    """
    try:
        path = Path(file_path)
        # If relative path, resolve from project root
        if not path.is_absolute():
            path = CURRENT_DIR / file_path

        if not path.exists():
            return {
                "status": "error",
                "message": f"File not found: {file_path}. Make sure the path is correct."
            }

        if not path.suffix == ".md":
            return {
                "status": "error",
                "message": "Can only read markdown (.md) files for safety."
            }

        with open(path, "r") as f:
            content = f.read()

        return {
            "status": "success",
            "path": str(path),
            "content": content,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read file: {str(e)}"
        }


def fetch_webpage_tool(url: str) -> dict:
    """
    Fetches the text content from a URL.

    Use this to read previous blog posts or other reference material from the web.

    Args:
        url: The URL to fetch (must start with http:// or https://)

    Returns:
        Success: {"status": "success", "content": "...", "url": "..."}
        Error: {"status": "error", "message": "..."}
    """
    if not url.startswith(("http://", "https://")):
        return {
            "status": "error",
            "message": "URL must start with http:// or https://"
        }

    try:
        # Set a user agent to avoid 403s from some sites
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            # Read and decode
            html_content = response.read().decode('utf-8', errors='ignore')

            # Basic HTML cleanup (remove scripts, styles, tags)
            # 1. Remove script and style elements
            clean_text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html_content, flags=re.DOTALL)
            # 2. Remove HTML tags
            clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
            # 3. Collapse whitespace
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()

            return {
                "status": "success",
                "url": url,
                "content": clean_text[:50000] # Limit size
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch URL: {str(e)}"
        }


# ============================================================================
# Phase 2 Tools: Content Filtering and Organization
# ============================================================================


def _llm_filter_content(draft: str, outline: str) -> dict:
    """
    Internal LLM helper to filter draft content into in-scope and out-of-scope sections.

    Args:
        draft: The raw draft content
        outline: The approved outline

    Returns:
        {"draft_ok": "...", "draft_not_ok": "..."}
    """
    prompt = f"""You are a content curator helping organize blog post drafts.

Given a DRAFT and an OUTLINE, your job is to split the draft content into two parts:

1. **IN-SCOPE (draft_ok):** Content that matches the outline's topics and should be included in this blog post.
2. **OUT-OF-SCOPE (draft_not_ok):** Content about future topics, tangents, or ideas that don't fit the current outline.

**CRITICAL RULES:**
- PRESERVE ALL CONTENT EXACTLY. Do not rewrite, summarize, or modify any text.
- Every paragraph from the draft must appear in EITHER draft_ok OR draft_not_ok (never both, never lost).
- Only split by paragraphs. Keep all text within paragraphs intact.
- Focus on topic matching: Does this paragraph discuss a topic covered in the outline?

**OUTLINE:**
```markdown
{outline}
```

**DRAFT:**
```markdown
{draft}
```

**OUTPUT FORMAT:**
Return your response as two markdown sections:

---IN-SCOPE---
[All in-scope paragraphs here, exactly as they appear in the draft]

---OUT-OF-SCOPE---
[All out-of-scope paragraphs here, exactly as they appear in the draft]

Now split the content:"""

    try:
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=prompt
        )
        result_text = response.text

        # Parse the response
        if not result_text:
            return {
                "status": "error",
                "message": "LLM returned empty response"
            }

        if "---IN-SCOPE---" not in result_text or "---OUT-OF-SCOPE---" not in result_text:
            return {
                "status": "error",
                "message": "LLM response missing required sections (IN-SCOPE/OUT-OF-SCOPE)"
            }

        parts = result_text.split("---IN-SCOPE---")[1]
        in_scope_part, out_scope_part = parts.split("---OUT-OF-SCOPE---")

        draft_ok = in_scope_part.strip()
        draft_not_ok = out_scope_part.strip()

        return {
            "status": "success",
            "draft_ok": draft_ok,
            "draft_not_ok": draft_not_ok
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"LLM filtering failed: {str(e)}"
        }


def filter_scope_tool(blog_id: str) -> dict:
    """
    Filter draft content into in-scope (matches outline) and out-of-scope (future topics).

    Uses an LLM to analyze the draft against the outline and split content into:
    - draft_ok.md: Content that fits the current outline
    - draft_not_ok.md: Content for future posts or topics outside the outline

    This is Phase 2.1 of the pipeline. User should review both files at the checkpoint
    before proceeding to organization (Phase 2.2).

    Args:
        blog_id: Unique identifier for the blog (e.g., "my-ai-journey-2")

    Returns:
        Success: {
            "status": "success",
            "blog_id": "...",
            "draft_ok_path": "...",
            "draft_not_ok_path": "...",
            "ok_count": N,     # Number of paragraphs in draft_ok
            "not_ok_count": M  # Number of paragraphs in draft_not_ok
        }
        Error: {"status": "error", "message": "Actionable error description"}
    """
    # 1. Read draft and outline
    draft_path = INPUTS_DIR / blog_id / draft_filename
    outline_path = OUTPUTS_DIR / blog_id / "outline.md"

    if not draft_path.exists():
        return {
            "status": "error",
            "message": f"Draft file not found for blog_id '{blog_id}'. Expected: {draft_path}"
        }

    if not outline_path.exists():
        return {
            "status": "error",
            "message": f"Outline file not found for blog_id '{blog_id}'. Expected: {outline_path}. Run Step 1 (Architect) first."
        }

    try:
        with open(draft_path, "r") as f:
            draft_content = f.read()
        with open(outline_path, "r") as f:
            outline_content = f.read()
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read input files: {str(e)}"
        }

    # 2. Call LLM to filter content
    filter_result = _llm_filter_content(draft_content, outline_content)
    if filter_result["status"] == "error":
        return filter_result

    draft_ok = filter_result["draft_ok"]
    draft_not_ok = filter_result["draft_not_ok"]

    # 3. Validate integrity (no content lost or added)
    is_valid, error_msg = check_content_integrity(draft_content, draft_ok, draft_not_ok)
    if not is_valid:
        return {
            "status": "error",
            "message": f"Content integrity check failed: {error_msg}. The LLM may have rewritten or lost content."
        }

    # 4. Save outputs
    try:
        draft_ok_path = OUTPUTS_DIR / blog_id / "draft_ok.md"
        draft_not_ok_path = OUTPUTS_DIR / blog_id / "draft_not_ok.md"

        draft_ok_path.parent.mkdir(parents=True, exist_ok=True)

        with open(draft_ok_path, "w") as f:
            f.write(draft_ok)
        with open(draft_not_ok_path, "w") as f:
            f.write(draft_not_ok)

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to save filtered content: {str(e)}"
        }

    # 5. Return success with stats
    ok_paragraphs = [p for p in draft_ok.split("\n\n") if p.strip()]
    not_ok_paragraphs = [p for p in draft_not_ok.split("\n\n") if p.strip()]

    return {
        "status": "success",
        "blog_id": blog_id,
        "draft_ok_path": str(draft_ok_path),
        "draft_not_ok_path": str(draft_not_ok_path),
        "ok_count": len(ok_paragraphs),
        "not_ok_count": len(not_ok_paragraphs)
    }
