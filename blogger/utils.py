from pathlib import Path


def read_instructions(filename: str) -> str:
    """Reads instructions from a file."""
    current_dir = Path(__file__).parent
    instruction_path = current_dir / "instructions" / filename
    with open(instruction_path, "r") as f:
        return f.read()
