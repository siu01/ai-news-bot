import feedparser
import yaml
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse
import time

class EnhancedNewsEngine:
    def __init__(self, config_path='config_runtime.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.rss_urls = {
            'en': self.config['rss']['google_news_ai_url'],
            'ja': self.config['rss']['google_news_ai_jp_url']
        }
        self.max_articles = self.config['rss']['max_articles']
    
    def get_ai_news_by_language(self, language='en'):
        """Fetch AI news from Google News RSS feed by language"""
        try:
            rss_url = self.rss_urls.get(language, self.rss_urls['en'])
            feed = feedparser.parse(rss_url)
            articles = []
            
            for entry in feed.entries[:self.max_articles]:
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                    'summary': entry.summary if hasattr(entry, 'summary') else '',
                    'source': entry.source.title if hasattr(entry, 'source') else 'Unknown',
                    'language': language
                }
                articles.append(article)
            
            return articles
        except Exception as e:
            print(f"Error fetching {language} news: {e}")
            return []
    
    def get_all_news(self):
        """Get news from all languages"""
        all_articles = []
        for language in ['en', 'ja']:
            articles = self.get_ai_news_by_language(language)
            all_articles.extend(articles)
        return all_articles
    
    def get_today_articles(self):
        """Get articles from today only"""
        articles = self.get_all_news()
        today_articles = []
        today = datetime.now().date()
        
        for article in articles:
            try:
                # Parse published date
                if article['published']:
                    pub_date = datetime.strptime(article['published'], '%a, %d %b %Y %H:%M:%S %Z').date()
                    if pub_date == today:
                        today_articles.append(article)
                else:
                    # If no date, include anyway
                    today_articles.append(article)
            except:
                # If date parsing fails, include the article anyway
                today_articles.append(article)
        
        return today_articles
    
    def extract_content(self, url):
        """Extract article content from URL (basic implementation)"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            return response.text[:2000]  # Return first 2000 characters
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return ""
