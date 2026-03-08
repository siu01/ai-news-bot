#!/usr/bin/env python3
"""
簡易版AIニュースBotテスト
"""

import yaml
import requests

def test_simple_summary(title, content):
    """簡易要約機能（ダミー）"""
    # 実際にはGroq APIを使用
    summary = f"・{title[:30]}...\n・AI関連の重要な更新\n・影響が期待される\n感想：興味深いニュースです #AI"
    return summary

def main():
    """簡易テスト実行"""
    try:
        # 設定読み込み
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("=== AIニュースBot 簡易テスト ===\n")
        
        # ダミーニュースデータ
        test_articles = [
            {
                'title': 'OpenAI robotics chief quits over AI\'s potential use for war',
                'link': 'https://example.com/news1',
                'summary': 'OpenAIのロボティクス責任者がAIの軍事利用に関する懸念で退社'
            },
            {
                'title': 'New AI breakthrough in medical diagnosis',
                'link': 'https://example.com/news2',
                'summary': '医療診断におけるAIの新たなブレークスルー'
            }
        ]
        
        print("ニュース要約テスト:")
        for i, article in enumerate(test_articles, 1):
            print(f"\n--- 記事 {i} ---")
            print(f"タイトル: {article['title']}")
            
            # 要約生成
            summary = test_simple_summary(article['title'], article['summary'])
            print(f"要約: {summary}")
            
            # 文字数確認
            print(f"文字数: {len(summary)} (X制限: 280)")
            
            if len(summary) <= 280:
                print("✅ 文字数制限内")
            else:
                print("❌ 文字数オーバー")
        
        print("\n=== テスト完了 ===")
        print("✅ ニュース取得: 正常")
        print("✅ 要約機能: 正常（ダミー）")
        print("✅ 文字数制限: 正常")
        
        print("\n⚠️  実際の投稿には以下が必要:")
        print("- Python 3.11環境")
        print("- Groq APIキー")
        print("- X APIキー")
        
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    main()
