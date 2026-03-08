import yaml
import tweepy
import os
from datetime import datetime

class Poster:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.log_file = self.config['bot']['log_file']
        self.posted_urls = self._load_posted_urls()
        
        # Initialize Twitter API v2 client
        self.client = tweepy.Client(
            bearer_token=self.config['x_api']['bearer_token'],
            consumer_key=self.config['x_api']['api_key'],
            consumer_secret=self.config['x_api']['api_secret'],
            access_token=self.config['x_api']['access_token'],
            access_token_secret=self.config['x_api']['access_token_secret']
        )
        
        # Also initialize v1.1 for media upload if needed
        auth = tweepy.OAuth1UserHandler(
            self.config['x_api']['api_key'],
            self.config['x_api']['api_secret'],
            self.config['x_api']['access_token'],
            self.config['x_api']['access_token_secret']
        )
        self.v1_api = tweepy.API(auth)
    
    def _load_posted_urls(self):
        """Load previously posted URLs from log file"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        return set()
    
    def _save_posted_url(self, url):
        """Save posted URL to log file"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{url}\n")
        self.posted_urls.add(url)
    
    def is_already_posted(self, url):
        """Check if URL has already been posted"""
        return url in self.posted_urls
    
    def post_tweet(self, summary, url):
        """Post tweet with summary and URL"""
        try:
            # Check if already posted
            if self.is_already_posted(url):
                print(f"Already posted: {url}")
                return False
            
            # Create tweet content
            tweet_content = f"{summary}\n\n{url}"
            
            # Post tweet
            response = self.client.create_tweet(text=tweet_content)
            
            # Log successful post
            self._save_posted_url(url)
            print(f"Successfully posted: {tweet_content[:50]}...")
            return True
            
        except Exception as e:
            print(f"Error posting tweet: {e}")
            return False
    
    def post_multiple_tweets(self, summaries):
        """Post multiple tweets"""
        posted_count = 0
        
        for item in summaries:
            if self.post_tweet(item['summary'], item['url']):
                posted_count += 1
                # Add delay between posts to avoid rate limiting
                import time
                time.sleep(30)  # 30 seconds between posts
        
        print(f"Posted {posted_count} tweets out of {len(summaries)} summaries")
        return posted_count
    
    def clean_old_logs(self, days=30):
        """Clean old entries from log file (keep last N days)"""
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Keep only recent entries (simplified - just keep last 1000 lines)
                recent_lines = lines[-1000:]
                
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.writelines(recent_lines)
                
                print(f"Cleaned log file, kept {len(recent_lines)} entries")
                
        except Exception as e:
            print(f"Error cleaning log file: {e}")
