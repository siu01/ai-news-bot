# AI News Bot

AIニュースを自動収集し、要約してX（Twitter）に投稿するボットです。

## 機能

- Google News RSSからAI関連ニュースを自動収集
- Groq API（Llama3）を使用して3行の箇条書き＋感想1行で要約
- X API v2で自動投稿
- 重複投稿防止機能（posted_urls.logで管理）
- GitHub Actionsで1時間おきに自動実行

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <your-repo-url>
cd ai-news-bot
```

### 2. Python環境のセットアップ

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 設定ファイルの作成

```bash
cp config.yaml config.yaml.local
```

`config.yaml.local` を編集してAPIキーを設定：

```yaml
x_api:
  api_key: "your_x_api_key"
  api_secret: "your_x_api_secret"
  access_token: "your_x_access_token"
  access_token_secret: "your_x_access_token_secret"
  bearer_token: "your_x_bearer_token"

groq_api:
  api_key: "your_groq_api_key"
```

### 4. APIキーの取得

#### X API v2
1. [X Developer Portal](https://developer.twitter.com/) でアプリを作成
2. API Key、API Secret、Access Token、Access Token Secret、Bearer Tokenを取得
3. アプリの権限を「Read and Write」に設定

#### Groq API
1. [Groq Console](https://console.groq.com/) でアカウント作成
2. API Keyを取得

## 使い方

### ローカルでテスト実行

```bash
# テストモード（投稿なし）
python main.py --test --config config.yaml.local

# 本番実行
python main.py --config config.yaml.local
```

### GitHub Actionsで自動実行

1. リポジトリのSettings > Secrets and variables > Actions に移動
2. 以下のSecretsを追加：
   - `X_API_KEY`
   - `X_API_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_TOKEN_SECRET`
   - `X_BEARER_TOKEN`
   - `GROQ_API_KEY`

3. コードをmainブランチにプッシュすると、1時間おきに自動実行されます

## ファイル構成

```
.
├── main.py              # メイン実行ファイル
├── news_engine.py       # ニュース収集エンジン
├── summarizer.py        # 要約モジュール
├── poster.py           # X投稿モジュール
├── config.yaml         # 設定ファイル（テンプレート）
├── requirements.txt    # Python依存関係
├── .github/workflows/bot.yml  # GitHub Actions設定
├── posted_urls.log     # 投稿済みURLログ
└── bot.log            # 実行ログ
```

## 設定オプション

### config.yaml

```yaml
rss:
  google_news_ai_url: "RSSフィードURL"
  max_articles: 5        # 処理する最大記事数

bot:
  max_summary_length: 280  # 最大文字数（X制限）
  log_file: "posted_urls.log"  # 投稿済みURLログファイル
```

## トラブルシューティング

### 一般的なエラー

1. **APIキーエラー**: 設定ファイルのAPIキーが正しいか確認
2. **レート制限エラー**: 投稿間隔を調整（現在30秒）
3. **RSS取得エラー**: Google NewsのURLが有効か確認

### ログの確認

```bash
tail -f bot.log
```

## カスタマイズ

### 要約フォーマットの変更
`summarizer.py` の `summarize_article` メソッドでプロンプトを編集

### RSSフィードの変更
`config.yaml` の `google_news_ai_url` を変更

### 投稿間隔の調整
`poster.py` の `time.sleep(30)` を調整

## ライセンス

MIT License
