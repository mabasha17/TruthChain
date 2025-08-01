"""
Complete fact-checking using free heuristics and local processing.
"""

import re
from typing import Dict, List
import config

class FactChecker:
    """Complete fact-checking using free heuristics."""
    
    def __init__(self):
        # No OpenAI dependency - completely free
        self.misinfo_keywords = [
            'fake news', 'conspiracy', 'hoax', 'debunked', 'false claim',
            'unverified', 'anonymous sources', 'rumor', 'allegedly',
            'sources say', 'insider claims', 'exclusive scoop'
        ]
        
        self.fact_check_indicators = [
            'fact-check', 'verified', 'confirmed', 'official statement',
            'police report', 'court documents', 'government data',
            'peer-reviewed', 'study published', 'research shows',
            'according to official', 'confirmed by', 'verified by'
        ]
        
        self.sensationalist_words = [
            'shocking', 'amazing', 'incredible', 'unbelievable',
            'you won\'t believe', 'viral', 'trending', 'breaking',
            'exclusive', 'secret', 'hidden', 'revealed',
            'mind-blowing', 'stunning', 'outrageous'
        ]
    
    def detect_misinformation(self, article: Dict) -> Dict:
        """Detect potential misinformation using comprehensive heuristics."""
        title = article.get('title', '').lower()
        content = article.get('content', '').lower()
        source = article.get('url', '').lower()
        
        risk_factors = 0
        concerns = []
        evidence = []
        
        # Check for sensationalist language
        sensational_count = sum(1 for word in self.sensationalist_words if word in title)
        if sensational_count > 0:
            risk_factors += sensational_count * 0.2
            concerns.append(f'Sensationalist language ({sensational_count} instances)')
            evidence.append(f'Found sensationalist words: {[w for w in self.sensationalist_words if w in title]}')
        
        # Check for misinformation keywords
        misinfo_count = sum(1 for keyword in self.misinfo_keywords if keyword in content)
        if misinfo_count > 0:
            risk_factors += misinfo_count * 0.3
            concerns.append(f'Misinformation indicators ({misinfo_count} instances)')
            evidence.append(f'Found misinfo keywords: {[k for k in self.misinfo_keywords if k in content]}')
        
        # Check for unverified claims
        unverified_indicators = ['sources say', 'anonymous', 'allegedly', 'rumored', 'unconfirmed']
        unverified_count = sum(1 for indicator in unverified_indicators if indicator in content)
        if unverified_count > 0:
            risk_factors += unverified_count * 0.25
            concerns.append(f'Unverified claims ({unverified_count} instances)')
            evidence.append(f'Found unverified indicators: {[i for i in unverified_indicators if i in content]}')
        
        # Check source credibility
        if any(unreliable in source for unreliable in config.UNRELIABLE_SOURCES.keys()):
            risk_factors += 0.4
            concerns.append('Unreliable source detected')
            evidence.append(f'Source domain: {source}')
        
        # Check for fact-checking indicators (positive)
        fact_check_count = sum(1 for indicator in self.fact_check_indicators if indicator in content)
        if fact_check_count > 0:
            risk_factors -= fact_check_count * 0.1  # Reduce risk
            evidence.append(f'Found fact-checking indicators: {[i for i in self.fact_check_indicators if i in content]}')
        
        # Calculate final risk score
        risk_score = max(0.0, min(1.0, risk_factors))
        
        # Determine recommendation
        if risk_score >= 0.7:
            recommendation = 'fact-check'
            action = 'High risk - verify with multiple sources'
        elif risk_score >= 0.4:
            recommendation = 'verify'
            action = 'Moderate risk - check additional sources'
        else:
            recommendation = 'trust'
            action = 'Low risk - appears reliable'
        
        return {
            'misinfo_risk': risk_score,
            'concerns': concerns,
            'evidence': evidence,
            'recommendation': recommendation,
            'action': action,
            'analysis': f'Comprehensive analysis: {len(concerns)} risk factors, {len(evidence)} evidence points'
        }
    
    def fact_check_query(self, query: str, context: str, articles: List[Dict]) -> Dict:
        """Provide comprehensive fact-checked response."""
        relevant_info = context[:1000] if context else "No information available"
        
        # Analyze query complexity
        query_words = query.lower().split()
        complexity_score = len(query_words) / 10.0  # Simple heuristic
        
        # Count sources and calculate diversity
        sources = [article.get('url', '') for article in articles if article.get('url')]
        source_diversity = min(len(set(sources)) / max(len(sources), 1), 1.0)
        
        # Calculate credibility scores
        credibility_scores = []
        for article in articles:
            cred = article.get('credibility', {}).get('overall_score', 0.5)
            credibility_scores.append(cred)
        
        avg_credibility = sum(credibility_scores) / len(credibility_scores) if credibility_scores else 0.5
        
        # Generate comprehensive answer
        answer = f"Based on analysis of {len(articles)} news articles:\n\n"
        answer += f"{relevant_info[:500]}...\n\n"
        answer += f"Sources analyzed: {len(sources)} articles from {len(set(sources))} different sources"
        
        # Calculate confidence based on multiple factors
        confidence = min(50 + (len(sources) * 5) + (avg_credibility * 20) + (source_diversity * 10), 85)
        
        # Generate evidence summary
        evidence_summary = f"Information from {len(sources)} news sources"
        if avg_credibility > 0.7:
            evidence_summary += " with high credibility scores"
        elif avg_credibility < 0.4:
            evidence_summary += " with mixed credibility"
        
        # Generate limitations
        limitations = []
        if len(sources) < 3:
            limitations.append("Limited number of sources")
        if avg_credibility < 0.6:
            limitations.append("Mixed source credibility")
        if complexity_score > 0.8:
            limitations.append("Complex query may require more analysis")
        
        limitations_text = "; ".join(limitations) if limitations else "Standard limitations apply"
        
        # Generate recommendations
        recommendations = []
        if len(sources) < 5:
            recommendations.append("Check additional sources")
        if avg_credibility < 0.7:
            recommendations.append("Verify with fact-checking websites")
        if any('breaking' in article.get('title', '').lower() for article in articles):
            recommendations.append("Breaking news may need time for verification")
        
        recommendations_text = "; ".join(recommendations) if recommendations else "Standard fact-checking recommended"
        
        return {
            'answer': answer,
            'confidence': int(confidence),
            'evidence': evidence_summary,
            'limitations': limitations_text,
            'recommendations': recommendations_text,
            'sources': sources,
            'full_response': answer,
            'source_count': len(sources),
            'avg_credibility': avg_credibility,
            'source_diversity': source_diversity
        }
    
    def get_misinfo_label(self, risk: float) -> str:
        """Get misinformation risk label."""
        if risk >= 0.8:
            return "High Risk"
        elif risk >= 0.6:
            return "Moderate Risk"
        elif risk >= 0.4:
            return "Low Risk"
        else:
            return "Likely Factual"
    
    def get_misinfo_color(self, risk: float) -> str:
        """Get misinformation risk color."""
        if risk >= 0.8:
            return "red"
        elif risk >= 0.6:
            return "orange"
        elif risk >= 0.4:
            return "yellow"
        else:
            return "green"
    
    def analyze_articles_batch(self, articles: List[Dict]) -> List[Dict]:
        """Analyze a batch of articles."""
        analyzed_articles = []
        
        for article in articles:
            misinfo_analysis = self.detect_misinformation(article)
            article['misinfo_analysis'] = misinfo_analysis
            analyzed_articles.append(article)
        
        return analyzed_articles 