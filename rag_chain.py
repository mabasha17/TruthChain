"""
Complete RAG pipeline using only free tools.
"""

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from typing import Dict, List, Any
import config
from fact_checker import FactChecker
from evaluator import QueryTimer, create_evaluator

class RAGPipeline:
    """Complete RAG pipeline using only free tools."""
    
    def __init__(self):
        # Use HuggingFace embeddings (free)
        self.embedding = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        # No OpenAI dependency - completely free
        self.db = None
        self.fact_checker = FactChecker()
        self.evaluator = create_evaluator()
        self.articles = []
        
        # Configure RAG settings
        rag_config = config.get_rag_config()
        self.chunk_size = rag_config['chunk_size']
        self.chunk_overlap = rag_config['chunk_overlap']
        self.top_k = rag_config['top_k']

    def ingest(self, articles: List[Dict]) -> None:
        """Ingest articles into the knowledge base."""
        if not articles:
            return
        
        self.articles = articles
        
        # Create documents
        docs = []
        for article in articles:
            content = f"Title: {article.get('title', '')}\n\nContent: {article.get('content', '')}"
            metadata = {
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'source': article.get('source', ''),
                'credibility_score': article.get('credibility', {}).get('overall_score', 0.5),
                'misinfo_risk': article.get('misinfo_analysis', {}).get('misinfo_risk', 0.5)
            }
            docs.append(Document(page_content=content, metadata=metadata))
        
        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        chunks = splitter.split_documents(docs)
        
        # Create vector store
        self.db = Chroma.from_documents(chunks, self.embedding)
        
        self.evaluator.log_articles_processed(len(articles))

    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system with comprehensive analysis."""
        if self.db is None:
            return {
                'answer': 'Please fetch news first.',
                'confidence': 0,
                'evidence': 'No data available',
                'limitations': 'System not ready',
                'recommendations': 'Initialize the system',
                'sources': [],
                'response_time': 0,
                'retrieved_docs': 0
            }
        
        try:
            with QueryTimer(self.evaluator) as timer:
                # Get relevant documents
                retriever = self.db.as_retriever(search_kwargs={'k': self.top_k})
                source_docs = retriever.get_relevant_documents(question)
                
                # Extract context
                context = "\n\n".join([doc.page_content for doc in source_docs])
                
                # Get fact-checked response
                fact_check_result = self.fact_checker.fact_check_query(
                    question, context, self.articles
                )
                
                # Calculate comprehensive metrics
                credibility_scores = [doc.metadata.get('credibility_score', 0.5) for doc in source_docs]
                misinfo_risks = [doc.metadata.get('misinfo_risk', 0.5) for doc in source_docs]
                
                avg_credibility = sum(credibility_scores) / len(credibility_scores) if credibility_scores else 0.5
                avg_misinfo_risk = sum(misinfo_risks) / len(misinfo_risks) if misinfo_risks else 0.5
                
                # Calculate source diversity
                sources = [doc.metadata.get('url', '') for doc in source_docs]
                source_diversity = min(len(set(sources)) / max(len(sources), 1), 1.0)
                
                # Log comprehensive metrics
                self.evaluator.log_query(
                    query=question,
                    response_time=timer.response_time,
                    confidence=fact_check_result.get('confidence', 50) / 100.0,
                    credibility=avg_credibility,
                    misinfo_risk=avg_misinfo_risk,
                    retrieved_docs=len(source_docs),
                    sources=sources
                )
                
                return {
                    'answer': fact_check_result.get('answer', 'No answer available'),
                    'confidence': fact_check_result.get('confidence', 50),
                    'evidence': fact_check_result.get('evidence', 'No specific evidence'),
                    'limitations': fact_check_result.get('limitations', 'Limited information'),
                    'recommendations': fact_check_result.get('recommendations', 'Verify with additional sources'),
                    'sources': sources,
                    'response_time': timer.response_time,
                    'retrieved_docs': len(source_docs),
                    'avg_credibility': avg_credibility,
                    'avg_misinfo_risk': avg_misinfo_risk,
                    'source_diversity': source_diversity,
                    'source_count': fact_check_result.get('source_count', len(sources)),
                    'full_response': fact_check_result.get('full_response', 'No response available')
                }
                
        except Exception as e:
            return {
                'answer': f'Error: {str(e)}',
                'confidence': 0,
                'evidence': 'Error occurred',
                'limitations': f'Technical error: {str(e)}',
                'recommendations': 'Try again later',
                'sources': [],
                'response_time': 0,
                'retrieved_docs': 0
            }

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics."""
        return self.evaluator.get_performance_summary()

    def export_metrics(self, filename: str = None) -> str:
        """Export system metrics."""
        return self.evaluator.export_metrics(filename)
