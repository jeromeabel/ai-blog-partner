import pytest
from blogger.utils.tools import (
    detect_draft_complexity,
    extract_quotes_with_sources,
    count_code_blocks,
    extract_main_topics,
)

def test_detect_draft_complexity_narrative():
    """Test complexity detection for quote-heavy narrative draft"""
    draft = """
    "Errors are teachers" — Karpathy
    This reminded me of my debugging struggles.
    "Constraints enable creativity" — My insight
    
    > Life is what happens when you're making other plans.
    - John Lennon
    
    It was a long journey of learning and discovery.
    """
    result = detect_draft_complexity(draft)
    # Heuristic: 3 quotes should give a reasonable score
    assert result["metrics"]["quote_count"] == 3
    assert result["metrics"]["paragraph_count"] >= 3
    assert "score" in result
    assert "suggested_mode" in result

def test_detect_draft_complexity_practical():
    """Test complexity detection for technical draft"""
    draft = """
    Here's how to debug Python:
    
    ```python
    def debug():
        print("test")
    ```
    
    Step 1: Add logging...
    
    ```javascript
    console.log("debug");
    ```
    """
    result = detect_draft_complexity(draft)
    assert result["metrics"]["code_block_count"] == 2
    assert "python" in result["metrics"]["languages"]
    assert "javascript" in result["metrics"]["languages"]

def test_extract_quotes_with_sources():
    """Test quote extraction with various attribution formats"""
    draft = """
    "Quote 1" — Author Name
    
    > Quote 2
    - Source: Blog Post
    
    "Quote 3" [source: https://example.com]
    
    Normal paragraph without quotes.
    """
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) == 3
    
    assert quotes[0]["text"] == "Quote 1"
    assert quotes[0]["source"] == "Author Name"
    
    assert "Quote 2" in quotes[1]["text"]
    assert "Blog Post" in quotes[1]["source"]
    
    assert quotes[2]["text"] == "Quote 3"
    assert quotes[2]["source"] == "https://example.com"

def test_count_code_blocks():
    """Test code block detection"""
    draft = """
    ```python
    print("hello")
    ```
    
    Some text
    
    ```javascript
    console.log("world")
    ```
    
    ```
    plain code
    ```
    """
    result = count_code_blocks(draft)
    assert result["count"] == 3
    assert "python" in result["languages"]
    assert "javascript" in result["languages"]
    # We filter out empty strings in the tool now
    assert "" not in result["languages"]

def test_extract_main_topics():
    """Test basic topic extraction (frequency based)"""
    draft = """
    Debugging is essential for software development. 
    When debugging, we look for bugs in the code.
    Effective debugging requires patience and the right tools.
    Software engineering is about more than just writing code; it's about debugging it too.
    """
    topics = extract_main_topics(draft)
    assert len(topics) >= 1
    # "debugging" should be a top topic
    assert any("debug" in t.lower() for t in topics)

def test_edge_cases():
    """Test tools with empty or minimal content"""
    empty_draft = ""
    assert detect_draft_complexity(empty_draft)["metrics"]["quote_count"] == 0
    assert len(extract_quotes_with_sources(empty_draft)) == 0
    assert count_code_blocks(empty_draft)["count"] == 0
    assert len(extract_main_topics(empty_draft)) == 0
