#!/usr/bin/env python3
"""
簡易ニュース取得テスト
"""

import xml.etree.ElementTree as ET
import requests
import yaml
from datetime import datetime, timedelta
import re

def test_news_fetch():
    """ニュース取得機能のテスト"""
    try:
        # 設定読み込み
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        rss_url = config['rss']['google_news_ai_url']
        max_articles = config['rss']['max_articles']
        
        print(f"RSS URL: {rss_url}")
        print(f"最大記事数: {max_articles}")
        
        # RSSフィード取得
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"RSS取得成功: {len(response.content)} bytes")
        
        # XML解析
        root = ET.fromstring(response.content)
        articles = []
        
        for item in root.findall('.//item')[:max_articles]:
            article = {
                'title': item.find('title').text if item.find('title') is not None else "",
                'link': item.find('link').text if item.find('link') is not None else "",
                'published': item.find('pubDate').text if item.find('pubDate') is not None else "",
                'summary': item.find('description').text if item.find('description') is not None else ""
            }
            
            if article['title'] and article['link']:
                articles.append(article)
        
        print(f"\n=== 記事一覧 ===")
        for i, article in enumerate(articles, 1):
            print(f"\n--- 記事 {i} ---")
            print(f"タイトル: {article['title']}")
            print(f"URL: {article['link']}")
            print(f"日時: {article['published']}")
            print(f"概要: {article['summary'][:100]}...")
        
        print(f"\n成功！ {len(articles)}件の記事を取得しました。")
        return True
        
    except Exception as e:
        print(f"エラー: {e}")
        return False

if __name__ == "__main__":
    test_news_fetch()
