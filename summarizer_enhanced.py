import yaml
import re
from groq import Groq

class EnhancedSummarizer:
    def __init__(self, config_path='config_runtime.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.client = Groq(api_key=self.config['groq_api']['api_key'])
        self.max_length = self.config['bot']['max_summary_length']
    
    def summarize_article(self, title, content, language='ja'):
        """Summarize article using Groq API with language support"""
        if language == 'ja':
            prompt = f"""
以下のAIニュース記事を要約してください。形式は以下の通り：
・要点1
・要点2  
・要点3
感想：1行の感想

タイトル：{title}
内容：{content[:1500]}
"""
            system_msg = "あなたはAIニュースを日本語で要約する専門家です。"
        else:
            prompt = f"""
Summarize the following AI news article in this format:
• Point 1
• Point 2
• Point 3
Thought: 1-line thought

Title: {title}
Content: {content[:1500]}
"""
            system_msg = "You are an expert at summarizing AI news in English."
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            
            summary = response.choices[0].message.content.strip()
            return self._format_summary(summary, language)
            
        except Exception as e:
            print(f"Error summarizing article: {e}")
            if language == 'ja':
                return f"【AIニュース】{title[:50]}... #AI"
            else:
                return f"【AI News】{title[:50]}... #AI"
    
    def _format_summary(self, summary, language):
        """Format summary to fit Twitter character limit"""
        # Remove extra whitespace and ensure proper formatting
        summary = re.sub(r'\s+', ' ', summary)
        
        # Add hashtags
        if language == 'ja':
            if not summary.endswith('#AI'):
                summary += " #AI"
        else:
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
                language = article.get('language', 'ja')
                summary = self.summarize_article(article['title'], content, language)
                
                summaries.append({
                    'summary': summary,
                    'url': article['link'],
                    'title': article['title'],
                    'language': language
                })
                
                # Add delay to avoid rate limiting
                import time
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing article {article['title']}: {e}")
                continue
        
        return summaries
