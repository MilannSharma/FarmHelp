# 🚀 Nax AI Training System

This document explains how to train Nax, the intelligent farming assistant, using comprehensive agriculture knowledge from trusted sources worldwide.

## 📋 Overview

Nax AI is enhanced with a knowledge base built from:
- **Wikipedia Agriculture Pages** - Foundational agricultural knowledge
- **Indian Agriculture News** - Krishi Jagran, Agriculture Today, AgriTimes
- **Government Resources** - e-Pashu Haat, DD Kisan, Economic Times Agriculture
- **International Sources** - Farmers.gov, Horticulture & Soil Science Wiki
- **RSS Feeds** - Latest agriculture news and research

## 🛠️ System Architecture

```
Data Collection → Knowledge Processing → Vector Embeddings → Chat Integration
     ↓               ↓                       ↓                  ↓
  Web Scraping → Text Processing → ChromaDB Storage → OpenAI API
```

## 📦 Dependencies

The training system requires these additional packages:
```bash
pip install beautifulsoup4 selenium chromedriver-autoinstaller
pip install feedparser langchain chromadb sentence-transformers
pip install faiss-cpu pandas lxml html5lib
```

## 🚀 Quick Start Training

### Option 1: Complete Training Pipeline
```bash
python train_nax.py
```
This runs the complete pipeline: data collection → processing → testing

### Option 2: Step-by-Step Training

1. **Collect Data from Sources:**
```bash
python data_collector.py
```
This scrapes all configured agriculture websites and saves to `agriculture_knowledge_base.json`

2. **Process and Create Knowledge Base:**
```bash
python knowledge_processor.py
```
This creates vector embeddings and stores them in ChromaDB

3. **Test the Knowledge Base:**
```bash
python -c "from knowledge_processor import AgricultureKnowledgeProcessor; p=AgricultureKnowledgeProcessor(); print(p.search_knowledge_base('rice farming techniques'))"
```

## 🎯 Training Data Sources

### Educational & Reference
- **Wikipedia**: Core agriculture concepts and practices
- **Wikibooks**: Detailed agricultural guides
- **Wikiversity**: Agricultural education portal

### Indian Agriculture News
- **Krishi Jagran**: Latest farming news and techniques
- **Down To Earth**: Environmental and agricultural journalism
- **Agriculture Today**: Farming technology and practices
- **AgriTimes**: Agricultural market intelligence
- **Agriculture Post**: Global agricultural news

### Government & Policy
- **Economic Times**: Agriculture policy and economics
- **e-Pashu Haat**: Livestock and animal husbandry
- **DD Kisan**: Government agricultural programs

### International Resources
- **Farmers.gov**: USA agricultural resources
- **Horticulture & Soil Science Wiki**: Specialized knowledge

## 🔧 Configuration

### OpenAI API Key
Set your OpenAI API key in `config.py`:
```python
OPENAI_API_KEY = 'your-api-key-here'
```

### Customize Data Sources
Edit `data_collector.py` to add or modify sources:
```python
self.sources = {
    'your_category': [
        'https://your-website.com',
        # Add more URLs
    ]
}
```

### Adjust Embedding Model
Change the embedding model in `knowledge_processor.py`:
```python
def __init__(self, model_name='all-MiniLM-L6-v2'):  # or 'all-mpnet-base-v2' for better quality
```

## 📊 Knowledge Base Statistics

After training, check the knowledge base:
```python
from knowledge_processor import AgricultureKnowledgeProcessor
processor = AgricultureKnowledgeProcessor()
stats = processor.get_stats()
print(f"Total chunks: {stats['total_chunks']}")
```

## 🧪 Testing Nax AI

1. **Start the Flask App:**
```bash
python app.py
```

2. **Test Chat Interface:**
   - Visit `http://127.0.0.1:5000/chat`
   - Ask farming-related questions
   - Nax will now use the knowledge base for enhanced responses

3. **Sample Test Questions:**
   - "What are the best crops for monsoon season?"
   - "How to control aphids in vegetable garden?"
   - "Government schemes for organic farming"
   - "Soil preparation for wheat cultivation"
   - "Latest trends in precision agriculture"

## 🔍 How It Works

### Data Collection Phase
- Scrapes content from configured websites
- Cleans and preprocesses text
- Handles rate limiting and error recovery
- Saves structured data to JSON

### Knowledge Processing Phase
- Splits content into meaningful chunks
- Creates vector embeddings using Sentence Transformers
- Stores embeddings in ChromaDB vector database
- Enables semantic search capabilities

### Chat Integration Phase
- Searches knowledge base for relevant information
- Provides context to OpenAI API
- Generates enhanced responses with agricultural expertise
- Maintains conversation history

## 🚨 Troubleshooting

### Common Issues

1. **Data Collection Fails:**
   - Check internet connection
   - Some websites may block scraping - add delays
   - Verify URLs are accessible

2. **Embedding Model Issues:**
   - Ensure sufficient RAM (4GB+ recommended)
   - Check available disk space for ChromaDB

3. **OpenAI API Errors:**
   - Verify API key is valid and has credits
   - Check rate limits and usage

4. **Memory Issues:**
   - Process data in smaller batches
   - Use lighter embedding models if needed

### Performance Optimization

- **Batch Processing:** Process data in chunks to manage memory
- **Chunk Size:** Adjust text chunk sizes (default: 500 words with 50-word overlap)
- **Embedding Model:** Use 'all-MiniLM-L6-v2' for speed, 'all-mpnet-base-v2' for quality
- **Search Results:** Limit to top 3-5 most relevant results per query

## 📈 Monitoring & Maintenance

### Regular Updates
- Re-run data collection monthly for latest information
- Update knowledge base with new agricultural research
- Refresh embeddings when adding new content

### Quality Assurance
- Test with diverse farming questions
- Verify source credibility
- Monitor response accuracy and relevance

### Backup & Recovery
- Backup `chroma_db/` directory regularly
- Keep `agriculture_knowledge_base.json` as raw data backup
- Document any custom training data additions

## 🎯 Advanced Features

### Custom Knowledge Addition
Add specific farming knowledge:
```python
processor = AgricultureKnowledgeProcessor()
articles = [
    {
        'title': 'Local Farming Practices',
        'content': 'Your specific farming knowledge...',
        'source': 'Custom',
        'category': 'Local'
    }
]
processor.add_to_knowledge_base(articles)
```

### Query Expansion
Enhance search with related terms:
```python
query = "rice cultivation"
expanded_query = f"{query} paddy farming Oryza sativa irrigation techniques"
results = processor.search_knowledge_base(expanded_query)
```

## 🤝 Contributing

To improve Nax AI's knowledge:
1. Add new reliable agriculture sources to `data_collector.py`
2. Test data collection from new sources
3. Verify content quality and relevance
4. Update this documentation

## 📞 Support

For issues or questions about the training system:
- Check the troubleshooting section above
- Verify all dependencies are installed
- Test with sample data first
- Review error logs for specific issues

---

**Happy Farming with Nax AI! 🌾🤖**
