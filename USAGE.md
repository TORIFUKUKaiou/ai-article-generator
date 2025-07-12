# AI Article Generator & Publisher 使用方法

## 概要

このツールは、OpenAI APIを使用して技術記事を自動生成し、Qiitaに投稿する統合スクリプトです。

## セットアップ

### 1. プロジェクト用仮想環境の作成

```bash
# プロジェクトルートで仮想環境を作成
python -m venv venv
source venv/bin/activate

# 統合スクリプト用の依存関係をインストール
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
# プロジェクトルートに.envファイルを作成
# QIITA_ACCESS_TOKENを設定（統合スクリプト用）
echo "QIITA_ACCESS_TOKEN=your_qiita_access_token_here" > .env

# python/.envファイルを作成
cp python/.env.sample python/.env

# python/.envファイルを編集してOpenAI API Keyを設定
OPENAI_API_KEY=your_openai_api_key_here
```

**注意**: 
- `generate_and_publish.py`は自動的にプロジェクトルートの`.env`ファイルを読み込みます
- `QIITA_ACCESS_TOKEN`はプロジェクトルートの`.env`に設定
- `OPENAI_API_KEY`は`python/.env`に設定

### 3. Python仮想環境の準備

```bash
cd python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 基本的な使用方法

```bash
# 基本的な記事生成・投稿
python generate_and_publish.py "ElixirのGenServerの使い方"

# テンプレートを指定
python generate_and_publish.py "React Hooksの活用法" --template tips --lang JavaScript

# 記事生成のみ（投稿しない）
python generate_and_publish.py "Docker入門" --generate-only

# 投稿のみ（生成済みJSONを使用）
python generate_and_publish.py --publish-only --token YOUR_TOKEN
```

## 記事テンプレート

| テンプレート | 説明 | 対象読者 | 記事長 |
|-------------|------|----------|--------|
| `tutorial` | 初心者向けチュートリアル | 初心者エンジニア | 長い |
| `tips` | 実用的なTips・小技 | 中級エンジニア | 中程度 |
| `deep-dive` | 技術の深掘り解説 | 上級エンジニア | 長い |
| `comparison` | 技術比較・選択指針 | エンジニア全般 | 中程度 |
| `troubleshooting` | 問題解決・トラブルシューティング | 実務エンジニア | 中程度 |

## オプション

### 必須パラメータ
- `topic`: 記事のトピック

### オプションパラメータ
- `--template, -t`: 記事テンプレート（デフォルト: tutorial）
- `--lang, -l`: プログラミング言語
- `--audience, -a`: 対象読者（カスタム指定）
- `--length`: 記事の長さ（短い/中程度/長い）
- `--token`: Qiita Access Token
- `--private`: プライベート記事として投稿（デフォルト）
- `--generate-only`: 記事生成のみ
- `--publish-only`: 投稿のみ

## 使用例

### 1. 初心者向けチュートリアル記事

```bash
python generate_and_publish.py "Pythonでのファイル操作入門" \
  --template tutorial \
  --lang Python \
  --audience "Python初心者"
```

### 2. 実用的なTips記事

```bash
python generate_and_publish.py "VS Codeの便利なショートカット10選" \
  --template tips \
  --length "中程度"
```

### 3. 技術比較記事

```bash
python generate_and_publish.py "Next.js vs Nuxt.js 2024年版比較" \
  --template comparison \
  --lang JavaScript
```

### 4. トラブルシューティング記事

```bash
python generate_and_publish.py "Docker Composeでよくあるエラーと解決法" \
  --template troubleshooting \
  --audience "DevOpsエンジニア"
```

### 5. 深掘り技術解説

```bash
python generate_and_publish.py "Rustの所有権システムの仕組み" \
  --template deep-dive \
  --lang Rust \
  --length "長い"
```

## ワークフロー

1. **記事生成**: OpenAI APIで指定されたトピック・テンプレートに基づいて記事を生成
2. **JSON保存**: 生成された記事を`python/generated_article.json`に保存
3. **記事投稿**: ElixirのQiita APIクライアントでQiitaに投稿

## トラブルシューティング

### よくあるエラー

1. **環境変数エラー**
   ```
   ❌ OPENAI_API_KEY環境変数が設定されていません
   ```
   → `python/.env`ファイルにAPI Keyを設定

2. **仮想環境エラー**
   ```
   ❌ Python仮想環境が見つかりません
   ```
   → `cd python && python -m venv venv`で仮想環境を作成

3. **投稿エラー**
   ```
   ❌ Qiita Access Tokenが設定されていません
   ```
   → `--token`オプションまたは環境変数`QIITA_ACCESS_TOKEN`を設定

## 注意事項

- 生成された記事はデフォルトでプライベート記事として投稿されます
- OpenAI APIの使用料金が発生します
- 生成された記事は必ず内容を確認してから公開してください
- Qiitaの利用規約を遵守してください
