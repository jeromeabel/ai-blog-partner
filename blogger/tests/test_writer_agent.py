import asyncio
from blogger.agents.writer import writer

def test_writer_instantiation():
    assert writer.name == "writer"
    assert len(writer.tools) >= 5
    assert len(writer.sub_agents) == 1
    assert writer.sub_agents[0].name == "scribr"
    print("✅ Writer agent instantiation test passed!")

if __name__ == "__main__":
    test_writer_instantiation()
