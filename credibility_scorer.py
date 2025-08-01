"""
Simple credibility scoring for news sources.
"""

from urllib.parse import urlparse
from typing import Dict, List
import config

class CredibilityScorer:
    """Simple credibility assessment for news sources."""
    
    def __init__(self):
        self.reliable_sources = config.RELIABLE_SOURCES
        self.unreliable_sources = config.UNRELIABLE_SOURCES
        self.weights = config.CREDIBILITY_WEIGHTS
    
    def extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return url.lower()
    
    def score_source_reputation(self, domain: str) -> float:
        """Score source reputation."""
        domain = domain.lower()
        
        if domain in self.reliable_sources:
            return self.reliable_sources[domain]
        
        if domain in self.unreliable_sources:
            return self.unreliable_sources[domain]
        
        return 0.5  # Default for unknown sources
    
    def check_https_secure(self, url: str) -> float:
        """Check if URL uses HTTPS."""
        if url.startswith('https://'):
            return 1.0
        elif url.startswith('http://'):
            return 0.0
        return 0.5
    
    def analyze_content_quality(self, title: str, content: str) -> float:
        """Simple content quality analysis."""
        score = 0.5
        
        text = (title + ' ' + content).lower()
        
        # Check for sensationalist language
        sensationalist_words = [
            'shocking', 'amazing', 'incredible', 'unbelievable',
            'you won\'t believe', 'viral', 'trending', 'breaking'
        ]
        
        sensationalist_count = sum(1 for word in sensationalist_words if word in text)
        
        if sensationalist_count == 0:
            score += 0.2
        elif sensationalist_count <= 2:
            score += 0.1
        else:
            score -= 0.2
        
        # Check for balanced language
        balanced_indicators = [
            'according to', 'reported', 'stated', 'said', 'confirmed'
        ]
        
        balanced_count = sum(1 for phrase in balanced_indicators if phrase in text)
        if balanced_count > 0:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def check_fact_checking_indicators(self, content: str) -> float:
        """Check for fact-checking indicators."""
        score = 0.5
        
        fact_checking_indicators = [
            'fact-check', 'verified', 'confirmed', 'official statement',
            'police report', 'court documents', 'government data'
        ]
        
        content_lower = content.lower()
        indicator_count = sum(1 for indicator in fact_checking_indicators 
                            if indicator in content_lower)
        
        if indicator_count > 0:
            score += 0.2
        if indicator_count > 2:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def estimate_domain_age(self, domain: str) -> float:
        """Simple domain age estimation."""
        if len(domain) > 20:
            return 0.3  # Likely newer
        elif domain.endswith(('.xyz', '.top', '.online')):
            return 0.4  # Newer TLDs
        elif domain.endswith(('.com', '.org', '.net')):
            return 0.7  # Established TLDs
        else:
            return 0.5  # Unknown
    
    def calculate_overall_credibility(self, article: Dict) -> Dict[str, float]:
        """Calculate overall credibility score."""
        url = article.get('url', '')
        domain = self.extract_domain(url)
        title = article.get('title', '')
        content = article.get('content', '')
        
        # Calculate individual scores
        source_reputation = self.score_source_reputation(domain)
        https_secure = self.check_https_secure(url)
        content_quality = self.analyze_content_quality(title, content)
        fact_checking = self.check_fact_checking_indicators(content)
        domain_age = self.estimate_domain_age(domain)
        
        # Calculate weighted score
        weighted_score = (
            source_reputation * self.weights['source_reputation'] +
            https_secure * self.weights['https_secure'] +
            content_quality * self.weights['content_quality'] +
            fact_checking * self.weights['fact_checking'] +
            domain_age * self.weights['domain_age']
        )
        
        return {
            'overall_score': weighted_score,
            'source_reputation': source_reputation,
            'https_secure': https_secure,
            'content_quality': content_quality,
            'fact_checking': fact_checking,
            'domain_age': domain_age,
            'domain': domain
        }
    
    def get_credibility_label(self, score: float) -> str:
        """Get credibility label."""
        if score >= 0.8:
            return "Highly Credible"
        elif score >= 0.6:
            return "Credible"
        elif score >= 0.4:
            return "Moderate"
        elif score >= 0.2:
            return "Low Credibility"
        else:
            return "Unreliable"
    
    def get_credibility_color(self, score: float) -> str:
        """Get credibility color."""
        if score >= 0.8:
            return "green"
        elif score >= 0.6:
            return "lightgreen"
        elif score >= 0.4:
            return "orange"
        elif score >= 0.2:
            return "red"
        else:
            return "darkred"
    
    def score_articles_batch(self, articles: List[Dict]) -> List[Dict]:
        """Score a batch of articles."""
        scored_articles = []
        
        for article in articles:
            credibility_scores = self.calculate_overall_credibility(article)
            article['credibility'] = credibility_scores
            scored_articles.append(article)
        
        return scored_articles 