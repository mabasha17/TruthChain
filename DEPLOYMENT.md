# 🚀 Streamlit Cloud Deployment Guide

## Overview

This guide helps you deploy the News RAG project to Streamlit Cloud without encountering SQLite3 compatibility issues.

## ✅ What's Fixed

- **Replaced ChromaDB with FAISS**: Avoids SQLite3 version requirements
- **Compatible with Python 3.13**: Works with Streamlit Cloud's Python version
- **Memory efficient**: FAISS is more memory-friendly for cloud deployment

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a public GitHub repository
2. **NewsAPI Key**: Get a free API key from [NewsAPI.org](https://newsapi.org/)
3. **Streamlit Account**: Sign up at [Streamlit Cloud](https://streamlit.io/cloud)

## 🚀 Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has these files:
```
news-rag-project/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies (updated for FAISS)
├── config.py             # Configuration settings
├── rag_chain.py          # RAG pipeline (now uses FAISS)
├── fact_checker.py       # Fact-checking logic
├── credibility_scorer.py # Source credibility analysis
├── news_fetcher.py       # News API integration
├── evaluator.py          # Performance metrics
├── scheduler.py          # Auto-refresh functionality
└── README.md            # Project documentation
```

### 2. Set Environment Variables

In Streamlit Cloud, add these environment variables:

```bash
NEWS_API_KEY=your_newsapi_key_here
NEWS_COUNTRY=us
NEWS_CATEGORY=general
NEWS_LIMIT=10
```

### 3. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set the main file path to: `app.py`
5. Click "Deploy"

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NEWS_API_KEY` | Your NewsAPI key | - | ✅ Yes |
| `NEWS_COUNTRY` | Country for news | `us` | ❌ No |
| `NEWS_CATEGORY` | News category | `general` | ❌ No |
| `NEWS_LIMIT` | Number of articles | `10` | ❌ No |

### RAG Settings

The app uses these optimized settings for cloud deployment:

- **Chunk Size**: 500 characters
- **Chunk Overlap**: 100 characters
- **Top K Retrieval**: 5 documents
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`

## 🐛 Troubleshooting

### Common Issues

**1. FAISS Import Error**
```bash
# Solution: Update requirements.txt
faiss-cpu>=1.7.0
```

**2. Memory Issues**
- Reduce `NEWS_LIMIT` to 5-8 articles
- Use smaller embedding models
- Restart the app periodically

**3. API Rate Limits**
- NewsAPI free tier: 1,000 requests/day
- Consider upgrading for production use

**4. Slow Loading**
- First load may take 1-2 minutes
- Subsequent loads will be faster
- Embedding model downloads on first use

### Performance Tips

1. **Reduce Article Count**: Set `NEWS_LIMIT=5` for faster processing
2. **Use Caching**: The app automatically caches results
3. **Monitor Memory**: Check Streamlit Cloud logs for memory usage
4. **Optimize Chunks**: Smaller chunks = faster processing

## 📊 Monitoring

### Streamlit Cloud Logs

Check logs for:
- Memory usage
- API rate limits
- Import errors
- Performance metrics

### Performance Metrics

The app tracks:
- Response times
- Query success rates
- Source credibility scores
- Misinformation detection accuracy

## 🔄 Updates

To update your deployment:

1. Push changes to GitHub
2. Streamlit Cloud automatically redeploys
3. Check logs for any issues
4. Test the new functionality

## 📞 Support

If you encounter issues:

1. Check the logs in Streamlit Cloud
2. Run `python test_faiss.py` locally
3. Verify environment variables
4. Check NewsAPI rate limits

## 🎯 Best Practices

1. **Start Small**: Begin with 5-8 articles
2. **Monitor Usage**: Check Streamlit Cloud metrics
3. **Cache Results**: Let the app cache embeddings
4. **Regular Updates**: Keep dependencies updated
5. **Error Handling**: The app includes robust error handling

## 🚀 Advanced Configuration

### Custom Embedding Models

To use different embedding models, modify `config.py`:

```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Fast, small
# Alternative: "sentence-transformers/all-mpnet-base-v2"   # Better quality, slower
```

### Memory Optimization

For memory-constrained environments:

```python
# In config.py
RAG_CONFIG = {
    'chunk_size': 300,      # Smaller chunks
    'chunk_overlap': 50,    # Less overlap
    'top_k': 3             # Fewer results
}
```

---

**Happy Deploying! 🎉**

Your News RAG app should now work perfectly on Streamlit Cloud without any SQLite3 compatibility issues. 