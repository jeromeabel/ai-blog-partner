from pathlib import Path

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
