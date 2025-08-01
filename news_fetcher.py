"""
Complete news fetching module - no OpenAI dependencies.
"""

import requests
import streamlit as st
from typing import List, Dict
from credibility_scorer import CredibilityScorer
from fact_checker import FactChecker
import config

def fetch_news(api_key: str, country: str = 'us', category: str = 'general', limit: int = 10) -> List[Dict]:
    """Fetch news articles."""
    if not api_key:
        st.error("NewsAPI key is required")
        return []
    
    try:
        url = f"{config.NEWS_API_BASE_URL}/top-headlines"
        params = {
            'country': country,
            'category': category,
            'pageSize': limit,
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'ok':
            st.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            return []
        
        articles = []
        for item in data.get('articles', []):
            content = item.get('description') or item.get('content', '')
            if content and item.get('title'):
                articles.append({
                    'title': item['title'],
                    'content': content,
                    'url': item.get('url', ''),
                    'source': item.get('source', {}).get('name', ''),
                    'published_at': item.get('publishedAt', ''),
                    'author': item.get('author', '')
                })
        
        return articles
        
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

def process_articles(articles: List[Dict]) -> List[Dict]:
    """Process articles with credibility scoring and misinformation detection."""
    if not articles:
        return []
    
    # Score credibility
    credibility_scorer = CredibilityScorer()
    scored_articles = credibility_scorer.score_articles_batch(articles)
    
    # Detect misinformation
    fact_checker = FactChecker()
    try:
        scored_articles = fact_checker.analyze_articles_batch(scored_articles)
    except Exception as e:
        st.warning(f"Misinformation detection failed: {str(e)}")
    
    return scored_articles

def get_news_categories() -> List[str]:
    """Get available news categories."""
    return config.NEWS_CATEGORIES

def get_news_config() -> Dict:
    """Get news configuration."""
    return config.get_news_config()