from pathlib import Path


def read_instructions(filename: str) -> str:
    """Reads instructions from the agents directory."""
    # Current dir is blogger/utils/
    # Instructions are now in blogger/agents/
    current_dir = Path(__file__).parent
    instruction_path = current_dir.parent / "agents" / filename
    
    if not instruction_path.exists():
        raise FileNotFoundError(f"Instruction file not found: {instruction_path}")
        
    with open(instruction_path, "r") as f:
        return f.read()
