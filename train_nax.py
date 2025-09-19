#!/usr/bin/env python3
"""
Training Script for Nax AI Assistant
Runs the complete training pipeline: data collection -> knowledge processing -> testing
"""

import os
import sys
import time
from datetime import datetime

def run_data_collection():
    """Run the data collection process"""
    print("🌾 Starting Data Collection Phase")
    print("=" * 50)

    try:
        # Import and run data collector
        from data_collector import AgricultureDataCollector

        collector = AgricultureDataCollector()
        data = collector.run_collection()

        print(f"✅ Data collection completed! Collected {len(data)} articles.")
        return True

    except Exception as e:
        print(f"❌ Data collection failed: {str(e)}")
        return False

def run_knowledge_processing():
    """Run the knowledge processing and embedding creation"""
    print("\n🧠 Starting Knowledge Processing Phase")
    print("=" * 50)

    try:
        # Import and run knowledge processor
        from knowledge_processor import AgricultureKnowledgeProcessor

        processor = AgricultureKnowledgeProcessor()
        processor.load_and_process_data()

        # Get stats
        stats = processor.get_stats()
        print("✅ Knowledge processing completed!")
        print(f"📊 Knowledge base contains {stats.get('total_chunks', 0)} text chunks")

        return True

    except Exception as e:
        print(f"❌ Knowledge processing failed: {str(e)}")
        return False

def test_knowledge_base():
    """Test the knowledge base with sample queries"""
    print("\n🧪 Testing Knowledge Base")
    print("=" * 50)

    try:
        from knowledge_processor import AgricultureKnowledgeProcessor

        processor = AgricultureKnowledgeProcessor()

        # Sample test queries
        test_queries = [
            "What are the best crops for sandy soil?",
            "How to control pests in tomato plants?",
            "What is the ideal pH for rice cultivation?",
            "Government schemes for farmers in India",
            "Organic farming techniques"
        ]

        print("Testing with sample queries:")
        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            results = processor.search_knowledge_base(query, n_results=2)

            if results:
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result['content'][:100]}...")
                    print(f"     Source: {result['source']} - {result['title']}")
            else:
                print("  No relevant information found")

        print("\n✅ Knowledge base testing completed!")
        return True

    except Exception as e:
        print(f"❌ Knowledge base testing failed: {str(e)}")
        return False

def main():
    """Main training pipeline"""
    print("🚀 Starting Nax AI Training Pipeline")
    print("=" * 60)
    print(f"Training started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    start_time = time.time()

    # Phase 1: Data Collection
    if not run_data_collection():
        print("❌ Training pipeline failed at data collection phase")
        return False

    # Phase 2: Knowledge Processing
    if not run_knowledge_processing():
        print("❌ Training pipeline failed at knowledge processing phase")
        return False

    # Phase 3: Testing
    if not test_knowledge_base():
        print("⚠️  Knowledge base testing failed, but training completed")
    else:
        print("✅ All training phases completed successfully!")

    # Calculate training time
    end_time = time.time()
    training_duration = end_time - start_time

    print("\n" + "=" * 60)
    print("🎉 Nax AI Training Summary:")
    print(f"   Duration: {training_duration:.2f} seconds ({training_duration/60:.2f} minutes)")
    print("   Status: Training pipeline completed")
    print("   Next: Start the Flask app to test Nax with enhanced knowledge")
    print("=" * 60)

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
