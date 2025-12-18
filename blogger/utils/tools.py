import re
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

from google import genai

from blogger.utils.text_utils import (
    check_content_integrity,
    check_heading_order,
    check_reorganization_integrity,
    extract_headings,
    find_best_heading_match,
    split_text_by_headings,
)

CURRENT_DIR = Path(__file__).parent.parent.parent
POSTS_DIR = CURRENT_DIR / "posts"
draft_filename = "draft.md"


# ============================================================================
# Workflow Discovery Tools: Agent autonomy and context inference
# ============================================================================
#
# These tools enable agents to discover workflow state from the file system
# without requiring users to specify blog_id in every message.
# ============================================================================

def get_workflow_status_tool() -> dict:
    """
    Discover all blogs and their workflow progress.

    Use this when:
    - User says "continue" or "next step" without specifying blog_id
    - Starting a session and need to find what to work on
    - User asks "where did we leave off?"

    Returns workflow state for all blogs in posts/ directory:
    - Which steps are complete (has 1-outline.md, 2-draft_organized.md, etc.)
    - Last modified timestamps
    - Recommended next action

    Returns:
        Success: {
            "status": "success",
            "blogs": [
                {
                    "blog_id": "my-post",
                    "current_step": 2,
                    "completed_steps": [1],
                    "next_action": "Run Curator (Step 2)",
                    "last_modified": "2025-12-18T14:30:00",
                    "files": {...}
                }
            ],
            "recommended": "my-post"  # Most recently modified
        }
        Error: {"status": "error", "message": "..."}

    Example:
        >>> get_workflow_status_tool()
        {
            "status": "success",
            "blogs": [{"blog_id": "my-ai-journey-2", "current_step": 2, ...}],
            "recommended": "my-ai-journey-2"
        }
    """
    try:
        if not POSTS_DIR.exists():
            return {
                "status": "error",
                "message": f"Posts directory not found: {POSTS_DIR}"
            }

        blogs = []
        for blog_dir in POSTS_DIR.iterdir():
            if not blog_dir.is_dir():
                continue

            blog_id = blog_dir.name
            files = {
                "draft": (blog_dir / "draft.md").exists(),
                "outline": (blog_dir / "1-outline.md").exists(),
                "organized": (blog_dir / "2-draft_organized.md").exists(),
                "final": (blog_dir / "3-final.md").exists(),
            }

            # Determine current step based on completed files
            if files["final"]:
                current_step = 3
                next_action = "Complete!"
            elif files["organized"]:
                current_step = 3
                next_action = "Run Writer (Step 3)"
            elif files["outline"]:
                current_step = 2
                next_action = "Run Curator (Step 2)"
            elif files["draft"]:
                current_step = 1
                next_action = "Run Architect (Step 1)"
            else:
                current_step = 0
                next_action = "Create draft.md"

            completed_steps = []
            if files["outline"]:
                completed_steps.append(1)
            if files["organized"]:
                completed_steps.append(2)
            if files["final"]:
                completed_steps.append(3)

            # Get last modified time (check all step files)
            timestamps = []
            for filename in ["draft.md", "1-outline.md", "2-draft_organized.md", "3-final.md"]:
                filepath = blog_dir / filename
                if filepath.exists():
                    timestamps.append(filepath.stat().st_mtime)

            last_modified = max(timestamps) if timestamps else 0

            blogs.append({
                "blog_id": blog_id,
                "current_step": current_step,
                "completed_steps": completed_steps,
                "next_action": next_action,
                "last_modified": last_modified,
                "last_modified_human":
                    __import__("datetime").datetime.fromtimestamp(last_modified).isoformat()
                    if last_modified else "never",
                "files": files,
            })

        # Sort by last modified (most recent first)
        blogs.sort(key=lambda b: b["last_modified"], reverse=True)

        # Recommend most recently modified blog
        recommended = blogs[0]["blog_id"] if blogs else None

        return {
            "status": "success",
            "blogs": blogs,
            "recommended": recommended,
            "total_blogs": len(blogs),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get workflow status: {str(e)}"
        }


def infer_blog_id_tool(hint: str = None) -> dict:
    """
    Infer which blog the user wants to work on.

    Use this when user mentions a blog indirectly:
    - "Continue where we left off"
    - "Work on my AI journey post"
    - "The blog about agents"

    Args:
        hint: Optional text hint from user (e.g., "AI journey", "my post")

    Returns:
        Success: {
            "status": "success",
            "blog_id": "my-ai-journey-2",
            "confidence": "high",  # high, medium, low
            "reason": "Only one blog modified recently"
        }
        Multiple matches: {
            "status": "success",
            "candidates": ["blog1", "blog2"],
            "message": "Found multiple matches..."
        }
        Error: {"status": "error", "message": "..."}

    Example:
        >>> infer_blog_id_tool("AI journey")
        {"status": "success", "blog_id": "my-ai-journey-2", "confidence": "high"}
    """
    try:
        # Get all blogs
        status = get_workflow_status_tool()
        if status["status"] == "error":
            return status

        blogs = status["blogs"]
        if not blogs:
            return {
                "status": "error",
                "message": "No blogs found in posts/ directory. Create a draft.md first."
            }

        # Case 1: Only one blog exists
        if len(blogs) == 1:
            return {
                "status": "success",
                "blog_id": blogs[0]["blog_id"],
                "confidence": "high",
                "reason": "Only one blog found",
                "blog_info": blogs[0],
            }

        # Case 2: Hint provided - fuzzy match blog_id
        if hint:
            hint_lower = hint.lower()
            matches = [
                b for b in blogs
                if hint_lower in b["blog_id"].lower()
            ]

            if len(matches) == 1:
                return {
                    "status": "success",
                    "blog_id": matches[0]["blog_id"],
                    "confidence": "high",
                    "reason": f"Matched hint '{hint}' to blog_id",
                    "blog_info": matches[0],
                }
            elif len(matches) > 1:
                return {
                    "status": "success",
                    "candidates": [m["blog_id"] for m in matches],
                    "confidence": "low",
                    "message": f"Found {len(matches)} blogs matching '{hint}': {', '.join([m['blog_id'] for m in matches])}. Please specify."
                }

        # Case 3: Multiple blogs, no hint - recommend most recent
        most_recent = blogs[0]
        return {
            "status": "success",
            "blog_id": most_recent["blog_id"],
            "confidence": "medium",
            "reason": "Most recently modified blog",
            "blog_info": most_recent,
            "alternatives": [b["blog_id"] for b in blogs[1:3]],  # Show top 3
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to infer blog_id: {str(e)}"
        }


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
    draft_path = POSTS_DIR / blog_id / draft_filename
    if not draft_path.exists():
        return {
            "status": "error",
            "message": f"Draft file not found for blog_id '{blog_id}'. Check the blog_id and ensure draft.md exists in posts/{blog_id}/",
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
        output_path = POSTS_DIR / blog_id / f"{step_name}.md"
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
    Checks for content.md, index.md, or final.md in posts/<blog_id>/.

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
        path = POSTS_DIR / blog_id / filename
        if path.exists():
            content_path = path
            break

    if not content_path:
        return {
            "status": "error",
            "message": f"Content file not found for blog_id '{blog_id}'. Checked: {', '.join(possible_files)} in posts/{blog_id}/",
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
        file_path: Path to the file (e.g., "posts/my-ai-journey-2/outline_v1.md")

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
                "message": f"File not found: {file_path}. Make sure the path is correct.",
            }

        if not path.suffix == ".md":
            return {
                "status": "error",
                "message": "Can only read markdown (.md) files for safety.",
            }

        with open(path, "r") as f:
            content = f.read()

        return {
            "status": "success",
            "path": str(path),
            "content": content,
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to read file: {str(e)}"}


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
        return {"status": "error", "message": "URL must start with http:// or https://"}

    try:
        # Set a user agent to avoid 403s from some sites
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            # Read and decode
            html_content = response.read().decode("utf-8", errors="ignore")

            # Basic HTML cleanup (remove scripts, styles, tags)
            # 1. Remove script and style elements
            clean_text = re.sub(
                r"<(script|style)[^>]*>.*?</\1>", "", html_content, flags=re.DOTALL
            )
            # 2. Remove HTML tags
            clean_text = re.sub(r"<[^>]+>", " ", clean_text)
            # 3. Collapse whitespace
            clean_text = re.sub(r"\s+", " ", clean_text).strip()

            return {
                "status": "success",
                "url": url,
                "content": clean_text[:50000],  # Limit size
            }
    except Exception as e:
        return {"status": "error", "message": f"Failed to fetch URL: {str(e)}"}


# ============================================================================

# ============================================================================
# Phase 2 Tools: Validation (ADK Pattern)
# ============================================================================
#
# In the ADK pattern:
# - Tools = Pure I/O and validation (NO LLM calls)
# - Agents = Do the thinking (filtering, organizing)  
#
# The Curator agent uses these validation tools to check its own work.
# ============================================================================

def validate_content_split_tool(
    original_content: str,
    split_part1: str,
    split_part2: str
) -> dict:
    """
    Validate that content was split correctly without loss or addition.

    Use this tool to verify that content filtering preserved all original content
    and didn't add hallucinated text. This is a pure validation function.

    Args:
        original_content: The original full content
        split_part1: First part of the split (e.g., draft_ok)
        split_part2: Second part of the split (e.g., draft_not_ok)

    Returns:
        Success: {
            "status": "success",
            "valid": True,
            "message": "Content split is valid"
        }
        Error: {
            "status": "error",
            "valid": False,
            "message": "Specific error (lost content, added content, duplicates)"
        }
    """
    is_valid, error_msg = check_content_integrity(
        original_content, split_part1, split_part2
    )

    if is_valid:
        return {
            "status": "success",
            "valid": True,
            "message": "Content split is valid - all content preserved, no additions or duplicates"
        }
    else:
        return {
            "status": "error",
            "valid": False,
            "message": error_msg
        }


def validate_organization_tool(
    draft_ok: str,
    outline: str,
    organized_content: str
) -> dict:
    """
    Validate that organized content matches outline structure and preserves content.

    Runs multiple validation checks:
    1. Content integrity: All draft_ok content exists in organized (no loss)
    2. Heading order: Section headings match outline order

    Use this tool after reorganizing content to verify correctness before saving.

    Args:
        draft_ok: The original in-scope content
        outline: The approved outline structure
        organized_content: The reorganized content to validate

    Returns:
        Success: {
            "status": "success",
            "valid": True,
            "checks": {
                "integrity": True,
                "heading_order": True
            },
            "message": "Organization is valid"
        }
        Error: {
            "status": "error",
            "valid": False,
            "checks": {
                "integrity": True/False,
                "heading_order": True/False
            },
            "errors": [...list of specific errors...]
        }
    """
    errors = []
    checks = {}

    # Check 1: Content integrity
    integrity_valid, integrity_msg = check_reorganization_integrity(
        draft_ok, outline, organized_content
    )
    checks["integrity"] = integrity_valid
    if not integrity_valid:
        errors.append(f"Integrity: {integrity_msg}")

    # Check 2: Heading order
    heading_valid, heading_msg = check_heading_order(outline, organized_content)
    checks["heading_order"] = heading_valid
    if not heading_valid:
        errors.append(f"Heading order: {heading_msg}")

    # Return result
    if integrity_valid and heading_valid:
        return {
            "status": "success",
            "valid": True,
            "checks": checks,
            "message": "Organization is valid - content preserved and headings match outline"
        }
    else:
        return {
            "status": "error",
            "valid": False,
            "checks": checks,
            "errors": errors,
            "message": f"Organization validation failed: {'; '.join(errors)}"
        }
