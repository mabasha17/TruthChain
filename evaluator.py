"""
Simple evaluation module for tracking metrics.
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class QueryMetrics:
    """Metrics for a single query."""
    query: str
    response_time: float
    confidence_score: float
    credibility_score: float
    misinfo_risk: float
    timestamp: datetime
    retrieved_docs: int
    sources_used: List[str]

class SystemEvaluator:
    """Simple system evaluator."""
    
    def __init__(self):
        self.query_history: List[QueryMetrics] = []
        self.start_time = datetime.now()
        self.articles_processed = 0
    
    def log_query(self, query: str, response_time: float, confidence: float, 
                  credibility: float, misinfo_risk: float, retrieved_docs: int, 
                  sources: List[str]) -> None:
        """Log metrics for a single query."""
        metrics = QueryMetrics(
            query=query,
            response_time=response_time,
            confidence_score=confidence,
            credibility_score=credibility,
            misinfo_risk=misinfo_risk,
            timestamp=datetime.now(),
            retrieved_docs=retrieved_docs,
            sources_used=sources
        )
        
        self.query_history.append(metrics)
    
    def log_articles_processed(self, count: int) -> None:
        """Log number of articles processed."""
        self.articles_processed += count
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of system performance."""
        if not self.query_history:
            return {
                'total_queries': 0,
                'avg_response_time': 0.0,
                'success_rate': 100.0,
                'articles_processed': self.articles_processed
            }
        
        avg_response_time = sum(q.response_time for q in self.query_history) / len(self.query_history)
        
        return {
            'total_queries': len(self.query_history),
            'avg_response_time': round(avg_response_time, 2),
            'success_rate': 100.0,
            'articles_processed': self.articles_processed
        }
    
    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.json"
        
        data = {
            'query_history': [asdict(q) for q in self.query_history],
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filename

class QueryTimer:
    """Simple context manager for timing queries."""
    
    def __init__(self, evaluator: SystemEvaluator):
        self.evaluator = evaluator
        self.start_time = None
        self.response_time = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            self.response_time = time.time() - self.start_time

def create_evaluator() -> SystemEvaluator:
    """Create a new system evaluator."""
    return SystemEvaluator() 