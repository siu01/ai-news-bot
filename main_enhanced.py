#!/usr/bin/env python3
"""
Enhanced AI News Bot - Fetches AI news in multiple languages, summarizes, and posts to X (Twitter)
"""

import sys
import os
from datetime import datetime
import logging

from news_engine_enhanced import EnhancedNewsEngine
from summarizer_enhanced import EnhancedSummarizer
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

class EnhancedAINewsBot:
    def __init__(self, config_path='config_runtime.yaml'):
        self.config_path = config_path
        self.news_engine = EnhancedNewsEngine(config_path)
        self.summarizer = EnhancedSummarizer(config_path)
        self.poster = Poster(config_path)
        
        logging.info("Enhanced AI News Bot initialized")
    
    def run(self):
        """Main bot execution"""
        try:
            logging.info("Starting Enhanced AI News Bot run...")
            
            # Step 1: Fetch today's AI news from all languages
            logging.info("Fetching today's AI news from multiple languages...")
            articles = self.news_engine.get_today_articles()
            
            if not articles:
                logging.info("No new articles found for today")
                return
            
            logging.info(f"Found {len(articles)} articles for today")
            
            # Step 2: Summarize articles
            logging.info("Summarizing articles...")
            summaries = self.summarizer.summarize_multiple_articles(articles)
            
            if not summaries:
                logging.info("No summaries generated")
                return
            
            logging.info(f"Generated {len(summaries)} summaries")
            
            # Group by language
            ja_summaries = [s for s in summaries if s['language'] == 'ja']
            en_summaries = [s for s in summaries if s['language'] == 'en']
            
            logging.info(f"Japanese summaries: {len(ja_summaries)}")
            logging.info(f"English summaries: {len(en_summaries)}")
            
            # Step 3: Post to X (interleave languages)
            logging.info("Posting to X...")
            posted_count = 0
            
            # Interleave posting: Japanese first, then English, repeat
            max_posts = max(len(ja_summaries), len(en_summaries))
            for i in range(max_posts):
                # Post Japanese
                if i < len(ja_summaries):
                    if self.poster.post_tweet(ja_summaries[i]['summary'], ja_summaries[i]['url']):
                        posted_count += 1
                        import time
                        time.sleep(30)  # Delay between posts
                
                # Post English
                if i < len(en_summaries):
                    if self.poster.post_tweet(en_summaries[i]['summary'], en_summaries[i]['url']):
                        posted_count += 1
                        import time
                        time.sleep(30)  # Delay between posts
            
            logging.info(f"Successfully posted {posted_count} tweets out of {len(summaries)} summaries")
            
            # Step 4: Clean up old logs
            self.poster.clean_old_logs()
            
            logging.info("Enhanced Bot run completed successfully")
            
        except Exception as e:
            logging.error(f"Error during bot execution: {e}")
            raise
    
    def test_mode(self):
        """Test mode - fetch and summarize without posting"""
        try:
            logging.info("Running in test mode...")
            
            articles = self.news_engine.get_today_articles()
            logging.info(f"Found {len(articles)} articles for today")
            
            ja_count = 0
            en_count = 0
            
            for i, article in enumerate(articles[:6]):  # Test with first 6 articles
                logging.info(f"\n--- Article {i+1} ({article.get('language', 'unknown')}) ---")
                logging.info(f"Title: {article['title']}")
                logging.info(f"URL: {article['link']}")
                
                content = f"{article['title']}\n{article['summary']}"
                language = article.get('language', 'ja')
                summary = self.summarizer.summarize_article(article['title'], content, language)
                logging.info(f"Summary: {summary}")
                logging.info(f"Already posted: {self.poster.is_already_posted(article['link'])}")
                
                if language == 'ja':
                    ja_count += 1
                else:
                    en_count += 1
            
            logging.info(f"\nSummary: {ja_count} Japanese articles, {en_count} English articles")
            
        except Exception as e:
            logging.error(f"Error in test mode: {e}")
            raise

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced AI News Bot')
    parser.add_argument('--test', action='store_true', help='Run in test mode (no posting)')
    parser.add_argument('--config', default='config_runtime.yaml', help='Config file path')
    
    args = parser.parse_args()
    
    # Check if config file exists
    if not os.path.exists(args.config):
        print(f"Config file {args.config} not found!")
        print("Please set up your API keys in the config file")
        sys.exit(1)
    
    bot = EnhancedAINewsBot(args.config)
    
    if args.test:
        bot.test_mode()
    else:
        bot.run()

if __name__ == "__main__":
    main()
