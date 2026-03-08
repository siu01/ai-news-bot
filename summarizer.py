import yaml
import re
from groq import Groq

class Summarizer:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.client = Groq(api_key=self.config['groq_api']['api_key'])
        self.max_length = self.config['bot']['max_summary_length']
    
    def summarize_article(self, title, content):
        """Summarize article using Groq API"""
        prompt = f"""
以下のAIニュース記事を要約してください。形式は以下の通り：
・要点1
・要点2  
・要点3
感想：1行の感想

タイトル：{title}
内容：{content[:1500]}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "あなたはAIニュースを日本語で要約する専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            return self._format_summary(summary)
            
        except Exception as e:
            print(f"Error summarizing article: {e}")
            return f"【AIニュース】{title[:50]}... #AI"
    
    def _format_summary(self, summary):
        """Format summary to fit Twitter character limit"""
        # Remove extra whitespace and ensure proper formatting
        summary = re.sub(r'\s+', ' ', summary)
        
        # Add hashtags
        if not summary.endswith('#AI'):
            summary += " #AI"
        
        # Truncate if too long
        if len(summary) > self.max_length:
            summary = summary[:self.max_length-3] + "..."
        
        return summary
    
    def summarize_multiple_articles(self, articles):
        """Summarize multiple articles"""
        summaries = []
        
        for article in articles:
            try:
                # Use title and summary for content
                content = f"{article['title']}\n{article['summary']}"
                summary = self.summarize_article(article['title'], content)
                
                summaries.append({
                    'summary': summary,
                    'url': article['link'],
                    'title': article['title']
                })
                
                # Add delay to avoid rate limiting
                import time
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing article {article['title']}: {e}")
                continue
        
        return summaries
