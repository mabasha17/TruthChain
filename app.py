"""
Complete News RAG with Fact-Checking - Beautiful UI
"""

import streamlit as st
import os
from datetime import datetime
from news_fetcher import fetch_news, process_articles, get_news_categories, get_news_config
from rag_chain import RAGPipeline
from scheduler import create_auto_refresh_scheduler
from evaluator import create_evaluator
from credibility_scorer import CredibilityScorer
import config

# Page config
st.set_page_config(
    page_title="📰 News RAG with Fact-Checking",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .warning-box {
        background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .article-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application with beautiful UI."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📰 News RAG with Fact-Checking</h1>
        <p><strong>Real-time news with AI-powered fact-checking using free tools</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
    if 'articles' not in st.session_state:
        st.session_state.articles = []
    if 'scheduler' not in st.session_state:
        st.session_state.scheduler = create_auto_refresh_scheduler()
    if 'evaluator' not in st.session_state:
        st.session_state.evaluator = create_evaluator()
    if 'credibility_scorer' not in st.session_state:
        st.session_state.credibility_scorer = CredibilityScorer()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # API Keys
        news_api_key = st.text_input(
            "🔑 NewsAPI Key (Required)",
            type="password",
            help="Get free key from https://newsapi.org"
        )
        
        st.markdown("---")
        
        # News Settings
        st.markdown("### 📰 News Settings")
        news_config = get_news_config()
        
        country = st.selectbox(
            "🌍 Country",
            ["us", "gb", "ca", "au", "in"],
            index=0
        )
        
        category = st.selectbox(
            "📂 Category",
            get_news_categories(),
            index=0
        )
        
        limit = st.slider(
            "📊 Number of Articles",
            min_value=5,
            max_value=20,
            value=10
        )
        
        st.markdown("---")
        
        # System Status
        st.markdown("### 📊 System Status")
        
        if st.session_state.rag_pipeline:
            metrics = st.session_state.rag_pipeline.get_system_metrics()
            
            st.metric("📈 Total Queries", metrics.get('total_queries', 0))
            st.metric("⚡ Avg Response Time", f"{metrics.get('avg_response_time', 0):.2f}s")
            st.metric("✅ Success Rate", f"{metrics.get('success_rate', 100):.1f}%")
            st.metric("📰 Articles Processed", metrics.get('articles_processed', 0))
            
            # Last update
            last_update = st.session_state.scheduler.get_time_since_update()
            st.info(f"🕒 Last update: {last_update}")
            
            # Auto-refresh
            if st.session_state.scheduler.should_update():
                st.warning("⏰ Time to refresh news!")
        else:
            st.info("🔧 System not initialized")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Fetch News Section (Moved to top)
        st.markdown("### 📥 Fetch News")
        
        # Fetch News Button
        if st.button("🔄 Fetch Latest News", type="primary", use_container_width=True):
            if not news_api_key:
                st.error("Please enter your NewsAPI key")
            else:
                with st.spinner("Fetching news..."):
                    articles = fetch_news(news_api_key, country, category, limit)
                    if articles:
                        processed_articles = process_articles(articles)
                        st.session_state.articles = processed_articles
                        
                        # Initialize RAG pipeline
                        st.session_state.rag_pipeline = RAGPipeline()
                        st.session_state.rag_pipeline.ingest(processed_articles)
                        
                        st.session_state.scheduler.mark_updated()
                        st.success(f"✅ Fetched {len(processed_articles)} articles!")
                    else:
                        st.error("Failed to fetch news")
        
        st.markdown("---")
        
        # Fact-Checking Section (Moved below fetch)
        st.markdown("### 🤖 Ask Questions")
        
        # Query input
        query = st.text_input(
            "Ask a question about the news",
            placeholder="What are the latest developments in technology?",
            help="Ask any question about the fetched news articles"
        )
        
        if query and st.button("🔍 Get Fact-Checked Answer", type="primary", use_container_width=True):
            if not st.session_state.rag_pipeline:
                st.error("Please fetch news first")
            else:
                with st.spinner("Analyzing..."):
                    result = st.session_state.rag_pipeline.query(query)
                    
                    # Display results in beautiful cards
                    st.markdown("### ✅ Fact-Check Results")
                    
                    # Metrics row
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        st.markdown("""
                        <div class="metric-card">
                            <h4>Confidence</h4>
                            <h2>{}</h2>
                        </div>
                        """.format(f"{result.get('confidence', 0)}%"), unsafe_allow_html=True)
                    
                    with col_b:
                        st.markdown("""
                        <div class="metric-card">
                            <h4>Response Time</h4>
                            <h2>{}</h2>
                        </div>
                        """.format(f"{result.get('response_time', 0):.2f}s"), unsafe_allow_html=True)
                    
                    with col_c:
                        st.markdown("""
                        <div class="metric-card">
                            <h4>Sources Used</h4>
                            <h2>{}</h2>
                        </div>
                        """.format(result.get('retrieved_docs', 0)), unsafe_allow_html=True)
                    
                    with col_d:
                        st.markdown("""
                        <div class="metric-card">
                            <h4>Avg Credibility</h4>
                            <h2>{}</h2>
                        </div>
                        """.format(f"{result.get('avg_credibility', 0.5)*100:.1f}%"), unsafe_allow_html=True)
                    
                    # Answer
                    st.markdown("### 📝 Answer")
                    st.markdown("""
                    <div class="article-card">
                        <p>{}</p>
                    </div>
                    """.format(result.get('answer', 'No answer available')), unsafe_allow_html=True)
                    
                    # Evidence and Analysis
                    st.markdown("### 📋 Evidence & Analysis")
                    
                    col_ev, col_lim, col_rec = st.columns(3)
                    
                    with col_ev:
                        st.markdown("""
                        <div class="info-box">
                            <h4>🔍 Evidence</h4>
                            <p>{}</p>
                        </div>
                        """.format(result.get('evidence', 'No evidence provided')), unsafe_allow_html=True)
                    
                    with col_lim:
                        st.markdown("""
                        <div class="warning-box">
                            <h4>⚠️ Limitations</h4>
                            <p>{}</p>
                        </div>
                        """.format(result.get('limitations', 'No limitations noted')), unsafe_allow_html=True)
                    
                    with col_rec:
                        st.markdown("""
                        <div class="success-box">
                            <h4>💡 Recommendations</h4>
                            <p>{}</p>
                        </div>
                        """.format(result.get('recommendations', 'No recommendations')), unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Quick Stats")
        
        if st.session_state.articles:
            # Calculate stats
            total_articles = len(st.session_state.articles)
            credibility_scores = [a.get('credibility', {}).get('overall_score', 0.5) for a in st.session_state.articles]
            misinfo_risks = [a.get('misinfo_analysis', {}).get('misinfo_risk', 0.5) for a in st.session_state.articles]
            
            avg_credibility = sum(credibility_scores) / len(credibility_scores)
            avg_misinfo_risk = sum(misinfo_risks) / len(misinfo_risks)
            
            high_cred = sum(1 for score in credibility_scores if score >= 0.8)
            low_cred = sum(1 for score in credibility_scores if score < 0.6)
            
            st.metric("📰 Total Articles", total_articles)
            st.metric("✅ High Credibility", high_cred)
            st.metric("⚠️ Low Credibility", low_cred)
            st.metric("📊 Avg Credibility", f"{avg_credibility:.1%}")
            st.metric("🚨 Avg Misinfo Risk", f"{avg_misinfo_risk:.1%}")
        else:
            st.info("📰 No articles loaded yet")
    
    # News Display
    if st.session_state.articles:
        st.markdown("### 📰 Latest News")
        
        for i, article in enumerate(st.session_state.articles[:5]):
            with st.expander(f"📄 {i+1}. {article.get('title', 'No title')}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(article.get('content', 'No content')[:300] + "...")
                    st.caption(f"📰 Source: {article.get('source', 'Unknown')}")
                    st.caption(f"📅 Published: {article.get('published_at', 'Unknown')}")
                
                with col2:
                    credibility = article.get('credibility', {})
                    if credibility:
                        score = credibility.get('overall_score', 0.5)
                        label = st.session_state.credibility_scorer.get_credibility_label(score)
                        color = st.session_state.credibility_scorer.get_credibility_color(score)
                        
                        st.markdown(f"**Credibility:** :{color}[{label}]")
                        st.progress(score)
                    
                    misinfo = article.get('misinfo_analysis', {})
                    if misinfo:
                        risk = misinfo.get('misinfo_risk', 0.5)
                        label = st.session_state.rag_pipeline.fact_checker.get_misinfo_label(risk)
                        color = st.session_state.rag_pipeline.fact_checker.get_misinfo_color(risk)
                        
                        st.markdown(f"**Misinfo Risk:** :{color}[{label}]")
                        st.progress(risk)

if __name__ == "__main__":
    main()

