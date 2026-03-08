#!/usr/bin/env python3
"""
AI News Bot - Fetches AI news, summarizes it, and posts to X (Twitter)
"""

import sys
import os
from datetime import datetime
import logging

from news_engine import NewsEngine
from summarizer import Summarizer
from poster import Poster

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class AINewsBot:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.news_engine = NewsEngine(config_path)
        self.summarizer = Summarizer(config_path)
        self.poster = Poster(config_path)
        
        logging.info("AI News Bot initialized")
    
    def run(self):
        """Main bot execution"""
        try:
            logging.info("Starting AI News Bot run...")
            
            # Step 1: Fetch recent AI news
            logging.info("Fetching AI news...")
            articles = self.news_engine.get_recent_articles(hours=24)
            
            if not articles:
                logging.info("No new articles found")
                return
            
            logging.info(f"Found {len(articles)} articles")
            
            # Step 2: Summarize articles
            logging.info("Summarizing articles...")
            summaries = self.summarizer.summarize_multiple_articles(articles)
            
            if not summaries:
                logging.info("No summaries generated")
                return
            
            logging.info(f"Generated {len(summaries)} summaries")
            
            # Step 3: Post to X
            logging.info("Posting to X...")
            posted_count = self.poster.post_multiple_tweets(summaries)
            
            logging.info(f"Successfully posted {posted_count} tweets")
            
            # Step 4: Clean up old logs
            self.poster.clean_old_logs()
            
            logging.info("Bot run completed successfully")
            
        except Exception as e:
            logging.error(f"Error during bot execution: {e}")
            raise
    
    def test_mode(self):
        """Test mode - fetch and summarize without posting"""
        try:
            logging.info("Running in test mode...")
            
            articles = self.news_engine.get_recent_articles(hours=24)
            logging.info(f"Found {len(articles)} articles")
            
            for i, article in enumerate(articles[:3]):  # Test with first 3 articles
                logging.info(f"\n--- Article {i+1} ---")
                logging.info(f"Title: {article['title']}")
                logging.info(f"URL: {article['link']}")
                
                content = f"{article['title']}\n{article['summary']}"
                summary = self.summarizer.summarize_article(article['title'], content)
                logging.info(f"Summary: {summary}")
                logging.info(f"Already posted: {self.poster.is_already_posted(article['link'])}")
            
        except Exception as e:
            logging.error(f"Error in test mode: {e}")
            raise

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI News Bot')
    parser.add_argument('--test', action='store_true', help='Run in test mode (no posting)')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    args = parser.parse_args()
    
    # Check if config file exists
    if not os.path.exists(args.config):
        print(f"Config file {args.config} not found!")
        print("Please copy config.yaml.example to config.yaml and fill in your API keys")
        sys.exit(1)
    
    bot = AINewsBot(args.config)
    
    if args.test:
        bot.test_mode()
    else:
        bot.run()

if __name__ == "__main__":
    main()
