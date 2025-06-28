import logging
from urllib.parse import urlparse
from typing import List
from crewai.tools import tool
from duckduckgo_search import DDGS
from newspaper import Article

# Set up logging
logger = logging.getLogger(__name__)

@tool("DuckDuckGo Search Tool")
def duckduckgo_search(query: str) -> List[str]:
    """
    Search for articles using DuckDuckGo and return top URLs.
    
    Args:
        query: The search query string
        
    Returns:
        List of URLs from search results
    """
    try:
        with DDGS() as ddg:
            results = list(ddg.text(query, max_results=8))
        
        urls = [result["href"] for result in results if result.get("href")]
        return urls if urls else ["No valid search results found."]
    
    except Exception as e:
        logger.error(f"Error in DuckDuckGo search: {str(e)}")
        return [f"Error performing search: {str(e)}"]

@tool("Article Content Fetcher")
def fetch_article(url: str) -> str:
    """
    Fetch and parse article content from a given URL with robust error handling.
    
    Args:
        url: The URL of the article to fetch
        
    Returns:
        Article content (truncated to 3000 characters) or error message
    """
    try:
        # Validate URL format
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return f"Invalid URL format: {url}"
        
        # Fetch and parse article
        article = Article(url, timeout=10)
        article.download()
        article.parse()
        
        content = article.text
        
        # Return content with length validation
        if content and len(content) > 50:
            return content[:3000]  # Truncate to 3000 characters
        else:
            return f"Insufficient content from {url}"
            
    except Exception as e:
        logger.error(f"Error fetching article from {url}: {str(e)}")
        return f"Error fetching content from {url}: {str(e)}"

