#!/usr/bin/env python3
"""
Knowledge Processor for Nax AI Training
Processes collected agriculture data and creates vector embeddings for RAG
"""

import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import pandas as pd
from datetime import datetime
import re
from typing import List, Dict, Any

class AgricultureKnowledgeProcessor:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None

        # Initialize ChromaDB
        self.setup_chromadb()

    def setup_chromadb(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Try persistent client first
            try:
                self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
                print("💾 Using persistent ChromaDB storage")
            except Exception as disk_error:
                print(f"⚠️  Disk storage failed ({str(disk_error)}), using in-memory storage")
                self.chroma_client = chromadb.Client()
                print("🧠 Using in-memory ChromaDB storage")

            # Create or get collection
            collection_name = "agriculture_knowledge"
            try:
                self.collection = self.chroma_client.get_collection(name=collection_name)
                print("📚 Using existing knowledge collection")
            except:
                self.collection = self.chroma_client.create_collection(name=collection_name)
                print("🆕 Created new knowledge collection")

        except Exception as e:
            print(f"❌ Error setting up ChromaDB: {str(e)}")
            raise

    def load_embedding_model(self):
        """Load the sentence transformer model"""
        if self.embedding_model is None:
            print(f"🤖 Loading embedding model: {self.model_name}")
            try:
                self.embedding_model = SentenceTransformer(self.model_name)
                print("✅ Embedding model loaded successfully")
            except Exception as e:
                print(f"❌ Error loading embedding model: {str(e)}")
                raise

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for better embeddings"""
        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())

        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)

        # Normalize whitespace again
        text = re.sub(r'\s+', ' ', text.strip())

        return text

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks for better retrieval"""
        if not text or len(text) <= chunk_size:
            return [text] if text else []

        chunks = []
        words = text.split()
        start = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = ' '.join(words[start:end])
            chunks.append(chunk)

            # Move start position with overlap
            start = end - overlap
            if start >= len(words):
                break

        return chunks

    def process_article(self, article: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process a single article into chunks with metadata"""
        title = article.get('title', 'Unknown Title')
        content = article.get('content', '')
        url = article.get('url', '')
        source = article.get('source', 'Unknown')
        category = article.get('category', 'General')

        # Preprocess content
        processed_content = self.preprocess_text(content)

        if not processed_content:
            return []

        # Create chunks
        chunks = self.chunk_text(processed_content)

        # Create chunk documents
        chunk_docs = []
        for i, chunk in enumerate(chunks):
            chunk_doc = {
                'id': f"{url}_{i}",
                'content': chunk,
                'title': title,
                'url': url,
                'source': source,
                'category': category,
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
            chunk_docs.append(chunk_doc)

        return chunk_docs

    def add_to_knowledge_base(self, articles: List[Dict[str, Any]]):
        """Add articles to the knowledge base with embeddings"""
        print(f"🧠 Processing {len(articles)} articles for knowledge base...")

        self.load_embedding_model()

        all_chunks = []
        ids = []
        metadatas = []
        contents = []

        for article in articles:
            chunks = self.process_article(article)
            all_chunks.extend(chunks)

        print(f"📝 Generated {len(all_chunks)} text chunks")

        # Process in batches to avoid memory issues
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]
            batch_contents = [chunk['content'] for chunk in batch]
            batch_ids = [chunk['id'] for chunk in batch]

            # Create embeddings
            try:
                embeddings = self.embedding_model.encode(batch_contents, show_progress_bar=True)
                embeddings_list = embeddings.tolist()

                # Prepare metadata
                batch_metadatas = []
                for chunk in batch:
                    metadata = {
                        'title': chunk['title'],
                        'url': chunk['url'],
                        'source': chunk['source'],
                        'category': chunk['category'],
                        'chunk_index': str(chunk['chunk_index']),
                        'total_chunks': str(chunk['total_chunks'])
                    }
                    batch_metadatas.append(metadata)

                # Add to collection
                self.collection.add(
                    embeddings=embeddings_list,
                    documents=batch_contents,
                    metadatas=batch_metadatas,
                    ids=batch_ids
                )

                print(f"✅ Added batch {i//batch_size + 1}/{(len(all_chunks) + batch_size - 1)//batch_size}")

            except Exception as e:
                print(f"❌ Error processing batch {i//batch_size + 1}: {str(e)}")
                continue

        print(f"🎉 Successfully added {len(all_chunks)} chunks to knowledge base")

    def search_knowledge_base(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the knowledge base for relevant information"""
        if not self.embedding_model:
            self.load_embedding_model()

        try:
            # Create query embedding
            query_embedding = self.embedding_model.encode([query])[0].tolist()

            # Search collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )

            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                    distance = results['distances'][0][i] if results['distances'] and results['distances'][0] else 0

                    result = {
                        'content': doc,
                        'title': metadata.get('title', 'Unknown'),
                        'url': metadata.get('url', ''),
                        'source': metadata.get('source', 'Unknown'),
                        'category': metadata.get('category', 'General'),
                        'relevance_score': 1 - distance  # Convert distance to similarity score
                    }
                    formatted_results.append(result)

            return formatted_results

        except Exception as e:
            print(f"❌ Error searching knowledge base: {str(e)}")
            return []

    def load_and_process_data(self, data_file: str = 'agriculture_knowledge_base.json'):
        """Load collected data and process it into the knowledge base"""
        if not os.path.exists(data_file):
            print(f"❌ Data file {data_file} not found. Please run data_collector.py first.")
            return

        print(f"📖 Loading data from {data_file}")

        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)

            print(f"📊 Loaded {len(articles)} articles")

            # Process and add to knowledge base
            self.add_to_knowledge_base(articles)

        except Exception as e:
            print(f"❌ Error processing data file: {str(e)}")
            raise

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            count = self.collection.count()
            return {
                'total_chunks': count,
                'collection_name': self.collection.name,
                'model_name': self.model_name
            }
        except Exception as e:
            print(f"❌ Error getting stats: {str(e)}")
            return {}

def main():
    """Main function to run the knowledge processor"""
    print("🚀 Starting Agriculture Knowledge Processor")
    print("=" * 50)

    processor = AgricultureKnowledgeProcessor()

    # Load and process data
    processor.load_and_process_data()

    # Print stats
    stats = processor.get_stats()
    print("\n📊 Knowledge Base Statistics:")
    print(f"   Total chunks: {stats.get('total_chunks', 0)}")
    print(f"   Collection: {stats.get('collection_name', 'Unknown')}")
    print(f"   Model: {stats.get('model_name', 'Unknown')}")

    print("\n✅ Knowledge processing completed!")

if __name__ == "__main__":
    main()
