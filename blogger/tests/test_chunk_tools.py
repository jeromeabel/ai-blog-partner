import pytest
from blogger.utils.tools import split_draft_into_chunks, extract_chunk_context

def test_split_draft_into_chunks_structure():
    """Test chunk extraction preserves structure and types."""
    draft = """# Heading

> "Quote here" — Author

My commentary on the quote.

```python
def code_block():
    pass
```

Another commentary.
"""
    chunks = split_draft_into_chunks(draft)
    
    # Debug info
    for c in chunks:
        print(f"{c['id']}: {c['type']} - {c['text'][:20]}...")

    assert len(chunks) == 5
    
    # 1. Heading
    assert chunks[0]["type"] == "heading"
    assert chunks[0]["text"] == "# Heading"
    assert chunks[0]["id"] == "1"
    
    # 2. Quote
    assert chunks[1]["type"] == "quote"
    assert ">" in chunks[1]["text"]
    assert "Author" in chunks[1]["text"]
    
    # 3. Commentary
    assert chunks[2]["type"] == "commentary"
    assert "My commentary" in chunks[2]["text"]
    
    # 4. Code
    assert chunks[3]["type"] == "code"
    assert "python" in chunks[3]["text"]
    assert "def code_block" in chunks[3]["text"]
    
    # 5. Commentary
    assert chunks[4]["type"] == "commentary"
    assert "Another commentary" in chunks[4]["text"]

def test_quote_attribution_handling():
    """Test that attribution lines are kept with the quote."""
    draft = """
> Quote text
- Author Name

Next paragraph.
"""
    chunks = split_draft_into_chunks(draft)
    
    assert len(chunks) == 2
    assert chunks[0]["type"] == "quote"
    assert "Author Name" in chunks[0]["text"]
    assert chunks[1]["type"] == "commentary"

def test_multiple_paragraphs_commentary():
    """Test that adjacent non-separated lines are one chunk, but blank lines split chunks."""
    draft = """
Para 1 line 1.
Para 1 line 2.

Para 2.
"""
    chunks = split_draft_into_chunks(draft)
    
    assert len(chunks) == 2
    assert chunks[0]["type"] == "commentary"
    assert "line 2" in chunks[0]["text"]
    assert chunks[1]["type"] == "commentary"
    assert "Para 2" in chunks[1]["text"]

def test_empty_input():
    assert split_draft_into_chunks("") == []
    assert split_draft_into_chunks(None) == []

def test_extract_chunk_context():
    chunks = [
        {"id": "1", "text": "A"},
        {"id": "2", "text": "B"},
        {"id": "3", "text": "C"}
    ]
    
    # Middle chunk
    ctx = extract_chunk_context(chunks, "2")
    assert ctx["chunk"]["text"] == "B"
    assert ctx["prev_chunk"]["text"] == "A"
    assert ctx["next_chunk"]["text"] == "C"
    
    # First chunk
    ctx = extract_chunk_context(chunks, "1")
    assert ctx["chunk"]["text"] == "A"
    assert ctx["prev_chunk"] is None
    assert ctx["next_chunk"]["text"] == "B"
    
    # Last chunk
    ctx = extract_chunk_context(chunks, "3")
    assert ctx["chunk"]["text"] == "C"
    assert ctx["prev_chunk"]["text"] == "B"
    assert ctx["next_chunk"] is None
    
    # Invalid ID
    ctx = extract_chunk_context(chunks, "99")
    assert ctx["chunk"] is None
    assert "error" in ctx

def test_calculate_chunk_similarity():
    """Test Jaccard similarity between chunks."""
    from blogger.utils.tools import calculate_chunk_similarity
    
    # Identical
    assert calculate_chunk_similarity("hello world", "hello world") == 1.0
    
    # Very similar
    sim = calculate_chunk_similarity(
        "Debugging is about understanding errors deeply",
        "Errors help us understand debugging better"
    )
    assert sim > 0.2
    
    # Different
    sim_diff = calculate_chunk_similarity(
        "Debugging is hard",
        "Python is a programming language"
    )
    assert sim_diff < 0.2
    
    # Empty
    assert calculate_chunk_similarity("", "test") == 0.0

def test_map_chunk_connections():
    """Test connection mapping based on similarity."""
    from blogger.utils.tools import map_chunk_connections
    chunks = [
        {"id": "1", "text": "Debugging errors deeply"},
        {"id": "2", "text": "Errors help debugging"},
        {"id": "3", "text": "Python language features"},
    ]
    # Use low threshold to catch connections
    connections = map_chunk_connections(chunks, threshold=0.3)
    
    assert "2" in connections["1"]
    assert "1" in connections["2"]
    assert "3" not in connections["1"]
    assert "3" not in connections["2"]

def test_split_draft_with_nested_structure_edge_case():
    """Test weird spacing."""
    draft = """# H1
    
Text
    
> Quote
> Continued

Text 2
"""
    chunks = split_draft_into_chunks(draft)
    # H1, Text, Quote, Text 2
    assert len(chunks) == 4
    assert chunks[0]["type"] == "heading"
    assert chunks[1]["type"] == "commentary"
    assert chunks[2]["type"] == "quote"
    assert chunks[3]["type"] == "commentary"
