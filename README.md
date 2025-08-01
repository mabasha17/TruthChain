# 📰 News RAG with Fact-Checking

**Complete real-time news analysis with AI-powered fact-checking**

## 🚀 Features

- **🆓 Completely Free**: No OpenAI costs - uses HuggingFace embeddings
- **🎨 Beautiful UI**: Modern, responsive interface with gradients and cards
- **🔍 Real-time Fact-Checking**: Comprehensive misinformation detection
- **📊 Credibility Scoring**: Source and content analysis
- **⚡ Fast Performance**: Optimized for speed and accuracy
- **📱 Mobile Friendly**: Works on all devices

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Embeddings**: HuggingFace Sentence Transformers (free)
- **Vector Database**: ChromaDB
- **News API**: NewsAPI.org (free tier)
- **Fact-Checking**: Advanced heuristics and analysis
- **Styling**: Custom gradients and modern design

## 📋 Prerequisites

- Python 3.8+
- NewsAPI key (free from https://newsapi.org)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   https://github.com/mabasha17/TruthChain.git
   cd news-rag-project
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**
   ```bash
   cp env_example.txt .env
   # Edit .env and add your NewsAPI key
   ```

## 🎯 Usage

1. **Start the application**

   ```bash
   streamlit run app.py
   ```

2. **Get your free NewsAPI key**

   - Visit https://newsapi.org
   - Sign up for free account
   - Copy your API key

3. **Configure settings**

   - Enter your NewsAPI key
   - Select country and category
   - Choose number of articles

4. **Fetch and analyze news**

   - Click "Fetch Latest News"
   - Wait for processing
   - View credibility scores

5. **Ask questions**
   - Type your question
   - Get fact-checked answers
   - View detailed analysis

## 🎨 UI Features

### Beautiful Design

- **Gradient Headers**: Eye-catching purple gradients
- **Metric Cards**: Clean, modern metric displays
- **Color-coded Analysis**: Green for good, red for risks
- **Responsive Layout**: Works on desktop and mobile

### Interactive Elements

- **Real-time Updates**: Auto-refresh functionality
- **Expandable Articles**: Click to see full content
- **Progress Bars**: Visual credibility indicators
- **Hover Effects**: Smooth button animations

## 🔍 Fact-Checking Features

### Misinformation Detection

- **Sensationalist Language**: Detects clickbait titles
- **Unverified Claims**: Identifies anonymous sources
- **Source Credibility**: Checks known unreliable sites
- **Fact-Checking Indicators**: Recognizes verified content

### Credibility Scoring

- **Source Reputation**: Known reliable/unreliable sources
- **HTTPS Security**: Checks website security
- **Content Quality**: Analyzes writing style
- **Domain Age**: Estimates site reliability

## 📊 Analysis Metrics

### Query Results

- **Confidence Score**: How reliable the answer is
- **Response Time**: How fast the system responds
- **Sources Used**: Number of articles analyzed
- **Average Credibility**: Overall source reliability

### System Performance

- **Total Queries**: Number of questions asked
- **Success Rate**: Percentage of successful responses
- **Articles Processed**: Total news items analyzed
- **Average Response Time**: System performance

## 🎯 Key Benefits

### 🆓 Completely Free

- No OpenAI API costs
- Uses free HuggingFace models
- Free NewsAPI tier
- No hidden charges

### 🎨 Beautiful Interface

- Modern gradient design
- Responsive layout
- Color-coded analysis
- Professional appearance

### 🔍 Advanced Analysis

- Comprehensive fact-checking
- Source credibility scoring
- Misinformation detection
- Detailed evidence analysis

### ⚡ High Performance

- Fast response times
- Efficient processing
- Real-time updates
- Scalable architecture

## 🚀 Deployment

### Local Development

```bash
streamlit run app.py
```

### Streamlit Cloud

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 📁 Project Structure

```
news-rag-project/
├── app.py                 # Main Streamlit application
├── news_fetcher.py        # News API integration
├── rag_chain.py          # RAG pipeline (free tools)
├── fact_checker.py       # Fact-checking heuristics
├── credibility_scorer.py # Source credibility analysis
├── scheduler.py          # Auto-refresh functionality
├── evaluator.py          # Performance metrics
├── config.py             # Configuration settings
├── requirements.txt      # Dependencies
├── README.md            # This file
└── env_example.txt      # Environment template
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
NEWS_API_KEY=your_newsapi_key_here

# Optional
NEWS_COUNTRY=us
NEWS_CATEGORY=general
NEWS_LIMIT=10
```

### RAG Settings

- **Chunk Size**: 500 characters
- **Chunk Overlap**: 100 characters
- **Top K Retrieval**: 5 documents
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2

## 🎯 Use Cases

### 📰 News Analysis

- Real-time news monitoring
- Fact-checking articles
- Source credibility assessment
- Misinformation detection

## 🙏 Acknowledgments

- **HuggingFace**: For free embedding models
- **NewsAPI**: For free news data
- **Streamlit**: For the beautiful UI framework
- **FAISS**: For vector storage
- **LangChain**: For RAG pipeline tools

## 🔧 Troubleshooting

### FAISS Import Error

If you encounter a FAISS import error like:

```
RuntimeError: This app has encountered an error...
```

**Solution:**

1. **Update dependencies:**

   ```bash
   pip uninstall faiss-cpu
   pip install faiss-cpu>=1.7.0
   ```

2. **Test FAISS installation:**

   ```bash
   python test_faiss.py
   ```

3. **Alternative: Use different Python version**
   - FAISS works with Python 3.8-3.13
   - Avoid Python 3.14+ for now

### Common Issues

**Memory Issues:**

- Reduce `NEWS_LIMIT` in config
- Use smaller embedding models
- Restart the app periodically

**API Rate Limits:**

- NewsAPI has daily limits on free tier
- Consider upgrading to paid plan for production

**Performance Issues:**

- Use GPU if available (modify `device` in config)
- Reduce chunk size for faster processing
- Enable caching in Streamlit

### Getting Help

1. Run the test script: `python test_faiss.py`
2. Check the logs in Streamlit Cloud
3. Verify your environment variables
4. Ensure all dependencies are installed correctly
