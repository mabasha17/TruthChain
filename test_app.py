"""
Simple test script to verify the News RAG system components.
"""

import os
import sys
from unittest.mock import Mock, patch
import pytest

def test_imports():
    """Test that all modules can be imported."""
    try:
        import config
        import news_fetcher
        import rag_chain
        import credibility_scorer
        import fact_checker
        import scheduler
        import evaluator
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration module."""
    try:
        import config
        assert hasattr(config, 'NEWS_API_BASE_URL')
        assert hasattr(config, 'OPENAI_MODEL')
        assert hasattr(config, 'RELIABLE_SOURCES')
        assert hasattr(config, 'UNRELIABLE_SOURCES')
        print("✅ Configuration module working")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_credibility_scorer():
    """Test credibility scoring functionality."""
    try:
        from credibility_scorer import CredibilityScorer
        
        scorer = CredibilityScorer()
        
        # Test with a sample article
        test_article = {
            'title': 'Test Article',
            'content': 'This is a test article with balanced language.',
            'url': 'https://reuters.com/test-article'
        }
        
        result = scorer.calculate_overall_credibility(test_article)
        
        assert 'overall_score' in result
        assert 'source_reputation' in result
        assert 'content_quality' in result
        
        print("✅ Credibility scorer working")
        return True
    except Exception as e:
        print(f"❌ Credibility scorer error: {e}")
        return False

def test_news_fetcher():
    """Test news fetching functionality (mocked)."""
    try:
        from news_fetcher import fetch_news
        
        # Mock the requests.get to avoid actual API calls
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                'status': 'ok',
                'articles': [
                    {
                        'title': 'Test Article',
                        'description': 'Test content',
                        'url': 'https://test.com/article',
                        'source': {'name': 'Test Source'},
                        'publishedAt': '2024-01-01T00:00:00Z',
                        'author': 'Test Author'
                    }
                ]
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            articles = fetch_news('fake_api_key')
            
            assert len(articles) == 1
            assert articles[0]['title'] == 'Test Article'
            
        print("✅ News fetcher working")
        return True
    except Exception as e:
        print(f"❌ News fetcher error: {e}")
        return False

def test_rag_pipeline():
    """Test RAG pipeline initialization."""
    try:
        from rag_chain import RAGPipeline
        
        # Test initialization (without actual API calls)
        with patch('langchain.embeddings.OpenAIEmbeddings') as mock_embeddings:
            with patch('langchain.chat_models.ChatOpenAI') as mock_llm:
                rag = RAGPipeline('fake_openai_key')
                
                assert rag.embedding is not None
                assert rag.llm is not None
                assert rag.db is None  # Not initialized yet
                
        print("✅ RAG pipeline initialization working")
        return True
    except Exception as e:
        print(f"❌ RAG pipeline error: {e}")
        return False

def test_evaluator():
    """Test evaluation metrics."""
    try:
        from evaluator import create_evaluator
        
        evaluator = create_evaluator()
        
        # Test logging a query
        evaluator.log_query(
            query="test query",
            response_time=1.5,
            confidence=0.8,
            credibility=0.7,
            misinfo_risk=0.3,
            retrieved_docs=3,
            sources=['https://test.com']
        )
        
        metrics = evaluator.get_performance_summary()
        
        assert metrics['total_queries'] == 1
        assert metrics['avg_response_time'] == 1.5
        
        print("✅ Evaluator working")
        return True
    except Exception as e:
        print(f"❌ Evaluator error: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("🧪 Running News RAG System Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_credibility_scorer,
        test_news_fetcher,
        test_rag_pipeline,
        test_evaluator
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 