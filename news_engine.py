import feedparser
import yaml
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse
import time

class NewsEngine:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.rss_url = self.config['rss']['google_news_ai_url']
        self.max_articles = self.config['rss']['max_articles']
    
    def get_ai_news(self):
        """Fetch AI news from Google News RSS feed"""
        try:
            feed = feedparser.parse(self.rss_url)
            articles = []
            
            for entry in feed.entries[:self.max_articles]:
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                    'summary': entry.summary if hasattr(entry, 'summary') else '',
                    'source': entry.source.title if hasattr(entry, 'source') else 'Unknown'
                }
                articles.append(article)
            
            return articles
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def get_recent_articles(self, hours=24):
        """Get articles from the last N hours"""
        articles = self.get_ai_news()
        recent_articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for article in articles:
            try:
                # Parse published date
                pub_date = datetime.strptime(article['published'], '%a, %d %b %Y %H:%M:%S %Z')
                if pub_date > cutoff_time:
                    recent_articles.append(article)
            except:
                # If date parsing fails, include the article anyway
                recent_articles.append(article)
        
        return recent_articles
    
    def extract_content(self, url):
        """Extract article content from URL (basic implementation)"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            return response.text[:2000]  # Return first 2000 characters
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return ""
