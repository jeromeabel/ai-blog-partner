import pytest
from blogger.utils.tools import extract_quotes_with_sources

def test_extract_quotes_same_line_attribution():
    draft = '> "Debugging is hard." — Brian Kernighan'
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) == 1
    assert quotes[0]["text"] == 'Debugging is hard.'
    assert quotes[0]["source"] == "Brian Kernighan"

def test_extract_quotes_smart_quotes_and_markdown():
    draft = '> _**“A lot of engineers don’t review much code.”**_'
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) == 1
    # We want the clean text
    assert "A lot of engineers" in quotes[0]["text"]
    assert "“" not in quotes[0]["text"]
    
def test_inline_author_says_pattern():
    draft = 'As Simon Willison aptly says, think of an LLM pair programmer as “over-confident and prone to mistakes”.'
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) > 0
    assert "over-confident" in quotes[0]["text"]
    assert "Simon Willison" in quotes[0]["source"]

def test_multi_line_blockquote():
    draft = """> "Quote line 1.
>
> Quote line 2." — Author
"""
    quotes = extract_quotes_with_sources(draft)
    # Ideally should be one quote
    assert len(quotes) == 1
    assert "Quote line 1" in quotes[0]["text"]
    assert "Quote line 2" in quotes[0]["text"]
    assert quotes[0]["source"] == "Author"

def test_extract_quotes_with_url_source():
    draft = '“Stay hungry, stay foolish” [source: https://en.wikipedia.org/wiki/Stay_Hungry,_Stay_Foolish]'
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) == 1
    assert "Stay hungry" in quotes[0]["text"]
    assert "https://" in quotes[0]["source"]

def test_blockquote_with_url_source():
    draft = """> "Focus is a matter of saying no."
> — https://apple.com/steve-jobs"""
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) == 1
    assert "Focus is a matter" in quotes[0]["text"]
    assert "https://apple.com" in quotes[0]["source"]

def test_blockquote_followed_by_url():
    draft = """> "Quote about AI."
https://example.com/ai-quote"""
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) == 1
    assert "Quote about AI" in quotes[0]["text"]
    assert "https://example.com/ai-quote" == quotes[0]["source"]

def test_blockquote_followed_by_markdown_link():
    draft = """> "Another quote."
[Source Title](https://example.com/source)"""
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) == 1
    assert "Another quote" in quotes[0]["text"]
    assert "[Source Title](https://example.com/source)" == quotes[0]["source"]