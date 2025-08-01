"""
Simple configuration settings.
"""

import os

# API Configuration
NEWS_API_BASE_URL = "https://newsapi.org/v2"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# News Settings
DEFAULT_COUNTRY = "us"
DEFAULT_CATEGORY = "general"
DEFAULT_LIMIT = 10
NEWS_CATEGORIES = [
    "general", "business", "technology", "entertainment", 
    "health", "science", "sports", "politics"
]

# RAG Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RETRIEVAL = 5
TEMPERATURE = 0.3

# Credibility Settings
CREDIBILITY_WEIGHTS = {
    "domain_age": 0.2,
    "https_secure": 0.1,
    "source_reputation": 0.3,
    "content_quality": 0.2,
    "fact_checking": 0.2
}

# Known Sources
RELIABLE_SOURCES = {
    "reuters.com": 0.9,
    "ap.org": 0.9,
    "bbc.com": 0.85,
    "npr.org": 0.85,
    "nytimes.com": 0.8,
    "washingtonpost.com": 0.8,
    "wsj.com": 0.8,
    "theguardian.com": 0.75,
    "cnn.com": 0.7,
    "abcnews.go.com": 0.7
}

UNRELIABLE_SOURCES = {
    "infowars.com": 0.1,
    "breitbart.com": 0.2,
    "naturalnews.com": 0.1,
    "beforeitsnews.com": 0.1
}

# UI Settings
STREAMLIT_CONFIG = {
    "page_title": "📰 News RAG with Fact-Checking",
    "page_icon": "📰",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Update Settings
UPDATE_INTERVAL_MINUTES = 30

def get_api_keys():
    """Get API keys from environment."""
    return {
        "news_api_key": os.getenv("NEWS_API_KEY", ""),
        "openai_api_key": os.getenv("OPENAI_API_KEY", "")
    }

def get_news_config():
    """Get news configuration."""
    return {
        "country": os.getenv("NEWS_COUNTRY", DEFAULT_COUNTRY),
        "category": os.getenv("NEWS_CATEGORY", DEFAULT_CATEGORY),
        "limit": int(os.getenv("NEWS_LIMIT", DEFAULT_LIMIT)),
        "categories": NEWS_CATEGORIES
    }

def get_rag_config():
    """Get RAG configuration."""
    return {
        "chunk_size": int(os.getenv("CHUNK_SIZE", CHUNK_SIZE)),
        "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", CHUNK_OVERLAP)),
        "top_k": int(os.getenv("TOP_K_RETRIEVAL", TOP_K_RETRIEVAL)),
        "temperature": float(os.getenv("TEMPERATURE", TEMPERATURE))
    } 