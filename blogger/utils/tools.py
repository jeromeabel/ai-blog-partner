import re
import shutil
import urllib.request
from collections import Counter
from datetime import datetime
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


# ============================================================================
# Phase 3 Tools: Section Manipulation
# ============================================================================

def read_section_tool(blog_id: str, section_heading: str) -> dict:
    """
    Extract a specific section with surrounding context from 2-draft_organized.md.

    Use this when the Writer agent needs to focus on polishing one section
    at a time. It provides the section content plus the titles of the 
    previous and next sections for context.

    Args:
        blog_id: Unique identifier for the blog
        section_heading: The heading of the section to read (e.g., "Introduction")

    Returns:
        Success: {
            "status": "success",
            "section_heading": "...",
            "section_content": "...",
            "prev_section": "...",
            "next_section": "..."
        }
        Error: {"status": "error", "message": "..."}
    """
    try:
        organized_path = POSTS_DIR / blog_id / "2-draft_organized.md"
        if not organized_path.exists():
            return {
                "status": "error",
                "message": f"Organized draft not found for blog '{blog_id}'. Run Curator (Step 2) first."
            }

        with open(organized_path, "r") as f:
            content = f.read()

        headings = extract_headings(content, level=2)
        if not headings:
            return {
                "status": "error",
                "message": "No sections (## headings) found in the organized draft."
            }

        # Find best match for the requested heading
        match = find_best_heading_match(section_heading, headings)
        if not match:
            available = [h['title'] for h in headings]
            return {
                "status": "error",
                "message": f"Section '{section_heading}' not found. Available sections: {', '.join(available)}"
            }

        # Split content by headings
        positions = [h['line_num'] for h in headings]
        chunks = split_text_by_headings(content, positions)

        # Map heading index to chunk index
        has_pre_content = positions[0] > 0
        chunk_offset = 1 if has_pre_content else 0
        match_idx = headings.index(match)
        
        section_content = chunks[match_idx + chunk_offset]
        
        # Get context (prev/next titles)
        prev_section = headings[match_idx - 1]['title'] if match_idx > 0 else None
        next_section = headings[match_idx + 1]['title'] if match_idx < len(headings) - 1 else None

        return {
            "status": "success",
            "section_heading": match['title'],
            "section_content": section_content,
            "prev_section": prev_section,
            "next_section": next_section
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to read section: {str(e)}"}


def save_section_tool(blog_id: str, section_heading: str, polished_content: str) -> dict:
    """
    Replace a section's content with its polished version in 2-draft_organized.md.

    Args:
        blog_id: Unique identifier for the blog
        section_heading: The original heading of the section to replace
        polished_content: The new, polished content for the section (must include heading)

    Returns:
        Success: {"status": "success", "blog_id": "...", "path": "...", "message": "..."}
        Error: {"status": "error", "message": "..."}
    """
    try:
        organized_path = POSTS_DIR / blog_id / "2-draft_organized.md"
        if not organized_path.exists():
            return {
                "status": "error",
                "message": f"Organized draft not found for blog '{blog_id}'."
            }

        with open(organized_path, "r") as f:
            content = f.read()

        headings = extract_headings(content, level=2)
        match = find_best_heading_match(section_heading, headings)
        if not match:
            return {"status": "error", "message": f"Section '{section_heading}' not found."}

        # Validation: Polished content must have a heading
        if not polished_content.strip().startswith('## '):
            return {
                "status": "error",
                "message": "Polished content must include the section heading (e.g., '## Title')."
            }

        # Validation: Heading must match the target section (fuzzy check)
        new_headings = extract_headings(polished_content, level=2)
        if not new_headings:
            return {"status": "error", "message": "No heading found in polished content."}
        
        # We use a relaxed fuzzy match here (0.7) to allow for minor title improvements by the Writer
        from blogger.utils.text_utils import fuzzy_match_score
        if fuzzy_match_score(match['title'], new_headings[0]['title']) < 0.7:
            return {
                "status": "error",
                "message": f"Heading in polished content ('{new_headings[0]['title']}') does not match target section ('{match['title']}')."
            }

        # Reconstruct the document
        positions = [h['line_num'] for h in headings]
        chunks = split_text_by_headings(content, positions)

        has_pre_content = positions[0] > 0
        chunk_offset = 1 if has_pre_content else 0
        match_idx = headings.index(match)

        # Replace the specific chunk
        chunks[match_idx + chunk_offset] = polished_content.strip()

        # Join chunks back together
        new_content = '\n'.join(chunks)

        with open(organized_path, "w") as f:
            f.write(new_content)

        return {
            "status": "success",
            "blog_id": blog_id,
            "path": str(organized_path),
            "message": f"Section '{match['title']}' updated successfully."
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save section: {str(e)}"}


def finalize_post_tool(blog_id: str) -> dict:
    """
    Create the final polished post by copying 2-draft_organized.md to 3-final.md.

    Args:
        blog_id: Unique identifier for the blog

    Returns:
        Success: {"status": "success", "final_path": "...", "message": "..."}
        Error: {"status": "error", "message": "..."}
    """
    try:
        source_path = POSTS_DIR / blog_id / "2-draft_organized.md"
        dest_path = POSTS_DIR / blog_id / "3-final.md"

        if not source_path.exists():
            return {
                "status": "error",
                "message": f"Organized draft not found: {source_path}. Complete Step 2 first."
            }

        # Read content to add metadata
        with open(source_path, "r") as f:
            content = f.read()

        # Add metadata footer
        footer = f"\n\n---\n*Generated by AI Blog Partner on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        with open(dest_path, "w") as f:
            f.write(content + footer)

        return {
            "status": "success",
            "final_path": str(dest_path),
            "message": f"Final post created successfully at {dest_path}"
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to finalize post: {str(e)}"}
# ============================================================================
# ============================================================================
# Phase 4 Tools: Content Analysis (Light Mode)
# ============================================================================

def detect_draft_complexity(draft_text: str) -> dict:
    """
    Calculate complexity metrics and score for a draft.

    Pure function (NO LLM).

    Args:
        draft_text: The raw draft content

    Returns:
        dict: Metrics and complexity score
    """
    if not draft_text:
        return {
            "score": 0,
            "suggested_mode": "light",
            "metrics": {
                "paragraph_count": 0,
                "quote_count": 0,
                "code_block_count": 0,
                "languages": [],
                "source_count": 0
            }
        }

    # Use regex to split by blank lines (even if they contain spaces)
    paragraphs = re.split(r'\n\s*\n', draft_text.strip())
    paragraphs = [p for p in paragraphs if p.strip()]
    paragraph_count = len(paragraphs)
    
    quotes = extract_quotes_with_sources(draft_text)
    quote_count = len(quotes)
    
    code_blocks = count_code_blocks(draft_text)
    code_block_count = code_blocks["count"]
    
    unique_sources = len(set(q["source"] for q in quotes if q["source"] != "Unknown"))
    
    # Heuristic complexity score (0-10)
    # Weights: quotes(0.4), code(0.3), paragraph density(0.3)
    quote_score = min(10, quote_count * 0.8)
    code_score = min(10, code_block_count * 2.0)
    density_score = min(10, paragraph_count / 10.0)
    
    score = (quote_score * 0.4) + (code_score * 0.3) + (density_score * 0.3)
    score = round(min(10, score), 1)
    
    return {
        "score": score,
        "suggested_mode": "light",  # Phase 4 always suggests light
        "metrics": {
            "paragraph_count": paragraph_count,
            "quote_count": quote_count,
            "code_block_count": code_block_count,
            "languages": code_blocks["languages"],
            "source_count": unique_sources
        }
    }


def extract_quotes_with_sources(draft_text: str) -> list[dict]:
    """
    Extract quotes and attempt to find their sources.

    Detects:
    - "Quote" — Author
    - > Quote
    - - Source: Author
    - Smart quotes and markdown formatting

    Args:
        draft_text: The raw draft content

    Returns:
        list[dict]: List of {text, source, line_number}
    """
    quotes = []
    lines = draft_text.splitlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Pattern 1: Blockquotes (single or multi-line)
        if line.startswith(">"):
            start_line = i
            quote_lines = []
            
            # Consume consecutive blockquote lines
            while i < len(lines) and lines[i].strip().startswith(">"):
                # Remove '>' and strip
                cleaned = lines[i].strip()[1:].strip()
                if cleaned: # Skip empty > lines if they are just spacers
                    quote_lines.append(cleaned)
                i += 1
            
            # Join content
            full_quote_text = " ".join(quote_lines)
            source = "Unknown"
            
            # Check for attribution inside the blockquote text (at the end)
            # Regex to find attribution at end of string: "Quote" — Author
            # Handles - or — or --
            match = re.search(r'(.*?)\s*(?:—|--|-)\s*(.*)$', full_quote_text)
            if match:
                # Potential attribution found
                # Verify the "source" part isn't too long (avoid false positives like hyphenated words)
                candidate_text = match.group(1).strip()
                candidate_source = match.group(2).strip()
                
                # Heuristic: Source usually short (< 50 chars) and Quote is distinct
                if len(candidate_source) < 50:
                    full_quote_text = candidate_text
                    source = candidate_source
            
            # If no internal attribution, check the *next* line in the draft
            if source == "Unknown" and i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith(("- ", "— ", "-- ")):
                    source = next_line.lstrip("-— ").strip()
                    if source.lower().startswith("source:"):
                        source = source[7:].strip()
                    i += 1
                elif next_line.startswith(("http://", "https://")):
                    source = next_line
                    i += 1
                elif next_line.startswith("[") and "](" in next_line:
                    source = next_line
                    i += 1
            
            # Clean Markdown (bold, italic, smart quotes)
            # Remove * and _
            full_quote_text = re.sub(r'[\*_]', '', full_quote_text)
            # Remove surrounding quotes if present (standard or smart)
            full_quote_text = full_quote_text.strip(' "“”')

            if full_quote_text:
                quotes.append({
                    "text": full_quote_text,
                    "source": source,
                    "line_number": start_line
                })
            
            continue # Already advanced i
        
        # Pattern 4: Narrative Attribution ("Author says...")
        # Matches: Simon Willison says... "Quote"
        # Be conservative: Require 2 Capitalized Words for author
        matches_narrative = re.findall(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:aptly )?(?:says|said|wrote|writes|notes|claims|argues).*?[“"]([^”"]+)[”"]', line)
        for src, text in matches_narrative:
            clean_text = re.sub(r'[\*_]', '', text.strip())
            quotes.append({
                "text": clean_text,
                "source": src.strip(),
                "line_number": i
            })

        # Pattern 2: Inline quotes with attribution
        # Enhance regex to support smart quotes and diverse dashes
        # Matches: "Quote" — Author OR “Quote” — Author
        matches = re.findall(r'[“"]([^”"]+)[”"]\s*(?:—|--|-)\s*([^,\.\n]+)', line)
        for text, src in matches:
             # Clean markdown inside inline quote too
            clean_text = re.sub(r'[\*_]', '', text.strip())
            quotes.append({
                "text": clean_text,
                "source": src.strip(),
                "line_number": i
            })
            
        # Pattern 3: Simple quoted text with [source: ...]
        if not matches:
             # Support smart quotes here too
            simple_matches = re.findall(r'[“"]([^”"]+)[”"]\s*\[source:\s*([^\]]+)\]', line)
            for text, src in simple_matches:
                clean_text = re.sub(r'[\*_]', '', text.strip())
                quotes.append({
                    "text": clean_text,
                    "source": src.strip(),
                    "line_number": i
                })

        i += 1
        
    return quotes


def count_code_blocks(draft_text: str) -> dict:
    """
    Count markdown code blocks and identify languages.

    Args:
        draft_text: The raw draft content

    Returns:
        dict: {count, languages}
    """
    # Regex for markdown code fences
    pattern = r"```(\w*)\n"
    matches = re.findall(pattern, draft_text)
    
    # Matches both start and end fences, so divide by 2
    # Filter out empty strings from languages (closing fences usually have no language)
    languages = [L for L in matches if L]
    
    return {
        "count": len(matches) // 2,
        "languages": list(set(languages))
    }


def extract_main_topics(draft_text: str) -> list[str]:
    """
    Extract potential main topics using keyword frequency.

    Pure function (NO LLM).

    Args:
        draft_text: The raw draft content

    Returns:
        list[str]: Top 3-5 keywords
    """
    if not draft_text:
        return []

    # Simple stop words
    stop_words = {
        "the", "and", "a", "to", "of", "in", "i", "is", "that", "it", "on", "you", 
        "this", "for", "with", "was", "as", "are", "with", "but", "have", "not",
        "be", "at", "or", "from", "an", "my", "by"
    }
    
    # Clean and tokenize
    words = re.findall(r'\b\w{4,}\b', draft_text.lower())
    filtered_words = [w for w in words if w not in stop_words]
    
    if not filtered_words:
        return []
        
    counts = Counter(filtered_words)
    
    # Return top 5
    return [word for word, count in counts.most_common(5)]


def save_analysis_tool(blog_id: str, analysis_data: dict) -> dict:
    """
    Generate and save 0-analysis.md with YAML front-matter.
    
    Supports both 'light' and 'deep' modes.

    Args:
        blog_id: Unique identifier for the blog
        analysis_data: Data structure from Analyzer agent

    Returns:
        Success: {"status": "success", "path": "..."}
        Error: {"status": "error", "message": "..."}
    """
    try:
        # Expected analysis_data structure:
        # {
        #   "type": "narrative"|"practical"|"mixed",
        #   "complexity": "low"|"medium"|"high",
        #   "metrics": {...},
        #   "topics": [...],
        #   "recommended_mode": "quote-driven"|"topic-driven",
        #   "summary": "Human-readable summary...",
        #   "mode": "light"|"deep",
        #   # Deep mode only:
        #   "chunks": [{id, score, text, ...}],
        #   "narrative_flows": [{name, description, sequence, avg_score}],
        #   "connections": {chunk_id: [connected_ids]}
        # }
        
        mode = analysis_data.get('mode', 'light')
        metrics = analysis_data.get("metrics", {})
        chunks = analysis_data.get("chunks", [])
        
        # Calculate deep metrics if available
        total_chunks = len(chunks)
        high_scoring_chunks = len([c for c in chunks if float(c.get('score', 0)) >= 8.0])
        
        # Build topics list for YAML
        topics_yaml = ""
        for t in analysis_data.get('topics', []):
            topics_yaml += f"  - {t}\n"
            
        # Build topics list for Markdown
        topics_md = ""
        for i, t in enumerate(analysis_data.get('topics', [])):
            topics_md += f"{i+1}. **{t.title()}**\n"
            
        # Build YAML Content
        yaml_content = f"""--- 
type: {analysis_data.get('type', 'mixed')}
complexity: {analysis_data.get('complexity', 'medium')}
mode: {mode}
detected_quote_count: {metrics.get('quote_count', 0)}
detected_code_blocks: {metrics.get('code_block_count', 0)}
main_topics:
{topics_yaml.rstrip()}
recommended_architect_mode: {analysis_data.get('recommended_mode', 'topic-driven')}"""

        if mode == 'deep':
            yaml_content += f"""
total_chunks: {total_chunks}
high_scoring_chunks: {high_scoring_chunks}
narrative_flows:"""
            for flow in analysis_data.get('narrative_flows', []):
                yaml_content += f"\n  - {flow.get('name', 'unnamed')}"
                
        yaml_content += "\n---\n"

        # Build Markdown Content
        md_content = f"""
# Draft Analysis ({mode.title()})

## Summary
{analysis_data.get('summary', 'No summary provided.')}

## Detected Topics
{topics_md.rstrip()}

## Complexity Assessment
- **Score:** {analysis_data.get('score', 'N/A')}/10
- **Rationale:** {analysis_data.get('rationale', 'Based on content metrics.')}
"""

        # Add Deep Analysis Sections
        if mode == 'deep':
            md_content += "\n## Content Chunks\n"
            
            # Group chunks by score
            high = [c for c in chunks if float(c.get('score', 0)) >= 8.0]
            mid = [c for c in chunks if 5.0 <= float(c.get('score', 0)) < 8.0]
            low = [c for c in chunks if float(c.get('score', 0)) < 5.0]
            
            md_content += f"\n### High-Scoring Chunks (>=8.0) - {len(high)} total\n"
            for c in high:
                md_content += f"\n**Chunk #{c['id']}** [{c['type'].title()}] (Score: {c['score']}/10)\n"
                md_content += f"> {c['text'][:200]}..." if len(c['text']) > 200 else f"> {c['text']}"
                md_content += f"\n> **Rationale:** {c.get('rationale', 'N/A')}\n"
                
            md_content += f"\n### Mid-Scoring Chunks (5.0-7.9) - {len(mid)} total\n"
            for c in mid:
                md_content += f"\n**Chunk #{c['id']}** (Score: {c['score']}/10)\n"
                
            md_content += f"\n### Low-Scoring Chunks (<5.0) - {len(low)} total\n"
            for c in low:
                md_content += f"\n**Chunk #{c['id']}** (Score: {c['score']}/10)\n"

            md_content += "\n## Suggested Narrative Flows\n"
            for flow in analysis_data.get('narrative_flows', []):
                md_content += f"\n### {flow.get('name', 'Unnamed Flow')} (Avg Score: {flow.get('avg_score', 'N/A')})\n"
                md_content += f"**Structure:** {flow.get('description', '')}\n"
                md_content += "```\n"
                # Add sequence visualizer if available
                seq = flow.get('chunk_sequence', [])
                if seq:
                    md_content += " -> ".join([f"#{cid}" for cid in seq[:10]])
                    if len(seq) > 10:
                        md_content += "..."
                md_content += "\n```\n"

        md_content += "\n---\n*This analysis was generated automatically. Review the summary, then proceed to Architect for outline creation.*"
        
        full_content = yaml_content + md_content
        
        output_path = POSTS_DIR / blog_id / "0-analysis.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            f.write(full_content)
            
        return {
            "status": "success",
            "blog_id": blog_id,
            "path": str(output_path)
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save analysis: {str(e)}"}


def read_analysis_tool(blog_id: str) -> dict:
    """
    Read 0-analysis.md and parse its YAML front-matter.
    
    Handles both light and deep mode formats.

    Args:
        blog_id: Unique identifier for the blog

    Returns:
        Success: {"status": "success", "data": {...}, "summary": "...", "chunks": [...]}
        Error: {"status": "error", "message": "..."}
    """
    try:
        analysis_path = POSTS_DIR / blog_id / "0-analysis.md"
        if not analysis_path.exists():
            return {"status": "error", "message": f"Analysis file not found for blog '{blog_id}'."}
            
        with open(analysis_path, "r") as f:
            content = f.read()
            
        if not content.startswith("---"):
            return {"status": "error", "message": "Invalid analysis file format (missing front-matter)."}
            
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {"status": "error", "message": "Invalid analysis file format (incomplete front-matter)."}
            
        yaml_text = parts[1]
        body_text = parts[2].strip()
        
        # Improved YAML-ish parser
        data = {}
        current_key = None
        for line in yaml_text.strip().split("\n"):
            line = line.rstrip()
            if not line: continue
            
            if line.startswith("  - "): # List item
                if current_key and current_key in data and isinstance(data[current_key], list):
                    data[current_key].append(line[4:].strip())
                continue
                
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                
                if not val: # Start of a list
                    data[key] = []
                    current_key = key
                else:
                    data[key] = val
                    current_key = key
        
        # Extract chunks from the Markdown body if mode is deep
        chunks = []
        if data.get('mode') == 'deep':
            # Look for "## Content Chunks" section
            if "## Content Chunks" in body_text:
                chunk_section = body_text.split("## Content Chunks")[1]
                # Regex to find Chunk #ID [Type] (Score: X/10)
                # and the following blockquote
                chunk_matches = re.finditer(
                    r"\*\*Chunk #(\d+)\*\*(?:\s+\[(\w+)\])?\s+\(Score:\s+([\d\.]+)/10\)\n>\s+(.*?)(?=\n\n\*\*Chunk|## Suggested|$)", 
                    chunk_section, 
                    re.DOTALL
                )
                for m in chunk_matches:
                    chunks.append({
                        "id": m.group(1),
                        "type": m.group(2) or "unknown",
                        "score": m.group(3),
                        "text_preview": m.group(4).strip()
                    })

        return {
            "status": "success",
            "data": data,
            "summary": body_text,
            "chunks": chunks
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to read analysis: {str(e)}"}



# ============================================================================
# Phase 5 Tools: Deep Analysis (Chunking)
# ============================================================================

def split_draft_into_chunks(draft_text: str) -> list[dict]:
    """
    Split draft into analyzable chunks (quotes, commentary, code, headings).
    
    Preserves markdown structure and line numbers.
    Assigns sequential IDs ("1", "2", ...).
    
    Args:
        draft_text: The raw draft content
        
    Returns:
        list[dict]: List of {id, type, text, line_start, line_end}
    """
    if not draft_text:
        return []

    lines = draft_text.splitlines()
    chunks = []
    
    current_lines = []
    current_type = None
    start_line = 0
    in_code_block = False
    
    # Helper to finalize the current chunk
    def finalize_chunk(end_line_idx):
        if not current_lines:
            return
        
        # Determine final type if not set (default to commentary)
        final_type = current_type if current_type else "commentary"
        
        # Join lines
        text = "\n".join(current_lines)
        
        chunks.append({
            "id": str(len(chunks) + 1),
            "type": final_type,
            "text": text,
            "line_start": start_line + 1,  # 1-based indexing
            "line_end": end_line_idx + 1   # 1-based indexing
        })
        
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 1. Code Block Handling
        if stripped.startswith("```"):
            if in_code_block:
                # End of code block
                current_lines.append(line)
                finalize_chunk(i)
                current_lines = []
                current_type = None
                in_code_block = False
            else:
                # Start of code block
                if current_lines:
                    finalize_chunk(i - 1)
                
                start_line = i
                current_lines = [line]
                current_type = "code"
                in_code_block = True
            continue
            
        if in_code_block:
            current_lines.append(line)
            continue
            
        # 2. Empty Line Handling
        if not stripped:
            if current_lines:
                finalize_chunk(i - 1)
                current_lines = []
                current_type = None
            continue
            
        # 3. Heading Handling
        if stripped.startswith("#"):
            if current_lines:
                finalize_chunk(i - 1)
            
            # Headings are their own chunks
            start_line = i
            current_lines = [line]
            current_type = "heading"
            finalize_chunk(i)
            current_lines = []
            current_type = None
            continue
            
        # 4. Quote Handling
        if stripped.startswith(">"):
            if current_type != "quote" and current_lines:
                finalize_chunk(i - 1)
                current_lines = []
                
            if not current_lines:
                start_line = i
                current_type = "quote"
                
            current_lines.append(line)
            continue
            
        # 5. Attribution Handling (for quotes)
        # Check if this line is an attribution for the preceding quote
        # E.g., "- Author Name" or "— Author Name"
        if current_type == "quote" and stripped.startswith(("-", "—", "--")):
            current_lines.append(line)
            continue
            
        # 6. Normal Text (Commentary)
        # If we were in a quote, this is a new commentary chunk
        if current_type == "quote":
            finalize_chunk(i - 1)
            current_lines = []
            current_type = None
            
        if not current_lines:
            start_line = i
            current_type = "commentary"
            
        current_lines.append(line)
        
    # Finalize any remaining lines
    if current_lines:
        finalize_chunk(len(lines) - 1)
        
    return chunks


def extract_chunk_context(chunks: list[dict], chunk_id: str) -> dict:
    """
    Get a chunk and its immediate neighbors by ID.
    
    Args:
        chunks: List of chunk dicts
        chunk_id: The ID to find
        
    Returns:
        dict: {chunk, prev_chunk, next_chunk} (neighbors can be None)
    """
    target_index = -1
    for i, chunk in enumerate(chunks):
        if chunk["id"] == chunk_id:
            target_index = i
            break
            
    if target_index == -1:
        return {
            "chunk": None,
            "prev_chunk": None,
            "next_chunk": None,
            "error": "Chunk ID not found"
        }
        
    return {
        "chunk": chunks[target_index],
        "prev_chunk": chunks[target_index - 1] if target_index > 0 else None,
        "next_chunk": chunks[target_index + 1] if target_index < len(chunks) - 1 else None
    }


def calculate_chunk_similarity(chunk1_text: str, chunk2_text: str) -> float:
    """
    Calculate Jaccard similarity between two text chunks.
    
    Args:
        chunk1_text: Text of first chunk
        chunk2_text: Text of second chunk
        
    Returns:
        float: Similarity score between 0.0 and 1.0
    """
    if not chunk1_text or not chunk2_text:
        return 0.0
        
    # Basic tokenization: lowercase, alpha-numeric only, 3+ chars
    def tokenize(text):
        tokens = re.findall(r'\b\w{3,}\b', text.lower())
        # Filter out very common words (subset of topics tool stop words)
        stop_words = {"the", "and", "for", "with", "that", "this", "from"}
        return set(t for t in tokens if t not in stop_words)
        
    set1 = tokenize(chunk1_text)
    set2 = tokenize(chunk2_text)
    
    if not set1 or not set2:
        return 0.0
        
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return float(intersection) / union


def map_chunk_connections(chunks: list[dict], threshold: float = 0.2) -> dict:
    """
    Find thematic connections between chunks based on text similarity.
    
    Args:
        chunks: List of chunk dicts (must have 'id' and 'text')
        threshold: Minimum similarity to consider a connection
        
    Returns:
        dict: {chunk_id: [list of connected chunk_ids]}
    """
    connections = {c["id"]: [] for c in chunks}
    
    # Compare all pairs (n^2, but okay for typical blog draft size of 20-50 chunks)
    for i in range(len(chunks)):
        for j in range(i + 1, len(chunks)):
            c1 = chunks[i]
            c2 = chunks[j]
            
            sim = calculate_chunk_similarity(c1["text"], c2["text"])
            
            if sim >= threshold:
                connections[c1["id"]].append(c2["id"])
                connections[c2["id"]].append(c1["id"])
                
    return connections


