from pathlib import Path

CURRENT_DIR = Path(__file__).parent.parent
INPUTS_DIR = CURRENT_DIR / "inputs"
OUTPUTS_DIR = CURRENT_DIR / "outputs"
draft_filename = "draft.md"


def read_draft(blog_id: str) -> str:
    draft_path = INPUTS_DIR / blog_id / draft_filename
    if not draft_path.exists():
        raise FileNotFoundError(f"Draft file not found for blog {blog_id}")
    with open(draft_path, "r") as f:
        return f.read()


def save_step_output(blog_id: str, step_name: str, content: str) -> None:
    output_path = OUTPUTS_DIR / blog_id / f"{step_name}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)
