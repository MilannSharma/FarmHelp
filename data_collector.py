#!/usr/bin/env python3
"""
Data Collector for Nax AI Training
Scrapes agriculture-related websites and processes content for chatbot training
"""

import requests
from bs4 import BeautifulSoup
import feedparser
import json
import time
import re
from urllib.parse import urljoin, urlparse
import pandas as pd
from datetime import datetime
import os

class AgricultureDataCollector:
    def __init__(self):
        self.sources = {
            'wikipedia': [
                'https://en.wikipedia.org/wiki/Agriculture',
                'https://en.wikibooks.org/wiki/Agriculture',
                'https://en.wikiversity.org/wiki/Portal:Agriculture'
            ],
            'indian_news': [
                'http://www.krishijagran.com',
                'https://www.downtoearth.org.in/agriculture',
                'http://www.agriculturetoday.in/',
                'https://agriculturepost.com/',
                'https://agritimes.co.in/'
            ],
            'government': [
                'http://epashuhaat.gov.in',
                'https://doordarshan.gov.in/ddkisan',
                'https://m.economictimes.com/news/economy/agriculture'
            ],
            'international': [
                'https://www.farmers.gov/blog',
                'https://horticultureandsoilscience.fandom.com/wiki/Agriculture'
            ]
        }

        self.collected_data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def clean_text(self, text):
        """Clean and preprocess text content"""
        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())

        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)

        # Remove very short texts
        if len(text.split()) < 10:
            return ""

        return text

    def extract_article_content(self, soup, url):
        """Extract main content from article pages"""
        content_selectors = [
            'article',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-content',
            'main',
            '.main-content',
            '#content',
            '.story-body'
        ]

        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                # Remove unwanted elements
                for unwanted in content.select('script, style, nav, header, footer, aside, .ads, .social-share'):
                    unwanted.decompose()

                text = content.get_text(separator=' ', strip=True)
                return self.clean_text(text)

        # Fallback: get all paragraph text
        paragraphs = soup.find_all('p')
        if paragraphs:
            text = ' '.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
            return self.clean_text(text)

        return ""

    def scrape_wikipedia_pages(self):
        """Scrape Wikipedia agriculture pages"""
        print("🔍 Scraping Wikipedia pages...")

        for url in self.sources['wikipedia']:
            try:
                print(f"  📄 Processing: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('h1', {'id': 'firstHeading'})
                title = title.get_text(strip=True) if title else "Wikipedia Agriculture"

                content = self.extract_article_content(soup, url)

                if content:
                    self.collected_data.append({
                        'title': title,
                        'content': content,
                        'url': url,
                        'source': 'Wikipedia',
                        'category': 'Educational',
                        'scraped_at': datetime.now().isoformat()
                    })

                time.sleep(1)  # Respectful scraping

            except Exception as e:
                print(f"  ❌ Error scraping {url}: {str(e)}")

    def scrape_news_sites(self):
        """Scrape agriculture news websites"""
        print("📰 Scraping agriculture news sites...")

        for base_url in self.sources['indian_news']:
            try:
                print(f"  📰 Processing: {base_url}")
                response = self.session.get(base_url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Find article links
                article_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('/'):
                        href = urljoin(base_url, href)

                    # Check if it's an article URL
                    if any(keyword in href.lower() for keyword in ['article', 'news', 'story', 'post']):
                        if href not in article_links and href.startswith(('http://', 'https://')):
                            article_links.append(href)

                # Limit to first 5 articles per site
                for article_url in article_links[:5]:
                    try:
                        article_response = self.session.get(article_url, timeout=10)
                        article_response.raise_for_status()

                        article_soup = BeautifulSoup(article_response.content, 'html.parser')

                        title_elem = article_soup.find('h1') or article_soup.find('title')
                        title = title_elem.get_text(strip=True) if title_elem else "Agriculture News"

                        content = self.extract_article_content(article_soup, article_url)

                        if content:
                            self.collected_data.append({
                                'title': title,
                                'content': content,
                                'url': article_url,
                                'source': base_url.split('//')[1].split('/')[0],
                                'category': 'News',
                                'scraped_at': datetime.now().isoformat()
                            })

                        time.sleep(2)  # Respectful scraping

                    except Exception as e:
                        print(f"    ❌ Error scraping article {article_url}: {str(e)}")

                time.sleep(3)  # Delay between sites

            except Exception as e:
                print(f"  ❌ Error scraping {base_url}: {str(e)}")

    def scrape_rss_feeds(self):
        """Scrape RSS feeds for agriculture content"""
        print("📡 Scraping RSS feeds...")

        rss_urls = [
            'https://rss.feedspot.com/indian_agriculture_rss_feeds/',
            # Add more RSS feeds as needed
        ]

        for rss_url in rss_urls:
            try:
                print(f"  📡 Processing RSS: {rss_url}")
                feed = feedparser.parse(rss_url)

                for entry in feed.entries[:10]:  # Limit to 10 entries per feed
                    title = entry.title if hasattr(entry, 'title') else 'RSS Article'
                    content = ''

                    if hasattr(entry, 'content'):
                        content = entry.content[0].value if entry.content else ''
                    elif hasattr(entry, 'summary'):
                        content = entry.summary
                    elif hasattr(entry, 'description'):
                        content = entry.description

                    # Clean HTML content
                    if content:
                        soup = BeautifulSoup(content, 'html.parser')
                        content = soup.get_text(separator=' ', strip=True)
                        content = self.clean_text(content)

                    if content:
                        self.collected_data.append({
                            'title': title,
                            'content': content,
                            'url': entry.link if hasattr(entry, 'link') else rss_url,
                            'source': 'RSS Feed',
                            'category': 'News',
                            'scraped_at': datetime.now().isoformat()
                        })

            except Exception as e:
                print(f"  ❌ Error scraping RSS {rss_url}: {str(e)}")

    def save_data(self, filename='agriculture_knowledge_base.json'):
        """Save collected data to JSON file"""
        print(f"💾 Saving {len(self.collected_data)} articles to {filename}")

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.collected_data, f, indent=2, ensure_ascii=False)

        print("✅ Data saved successfully!")

    def run_collection(self):
        """Run the complete data collection process"""
        print("🚀 Starting Agriculture Data Collection for Nax AI Training")
        print("=" * 60)

        start_time = time.time()

        # Collect data from all sources
        self.scrape_wikipedia_pages()
        self.scrape_news_sites()
        self.scrape_rss_feeds()

        # Save collected data
        self.save_data()

        end_time = time.time()
        duration = end_time - start_time

        print("=" * 60)
        print(f"✅ Collection completed in {duration:.2f} seconds")
        print(f"📊 Total articles collected: {len(self.collected_data)}")
        print("=" * 60)

        return self.collected_data

if __name__ == "__main__":
    collector = AgricultureDataCollector()
    data = collector.run_collection()
