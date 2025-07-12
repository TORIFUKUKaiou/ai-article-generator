# AI Article Generator & Publisher 使用方法

## 概要

このツールは、OpenAI APIを使用して技術記事を自動生成し、Qiitaに投稿する統合スクリプトです。

## セットアップ

### 1. 仮想環境の作成とパッケージインストール

```bash
# プロジェクトルートで仮想環境を作成
python -m venv venv
source venv/bin/activate

# 全依存関係をインストール
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

## 基本的な使用方法

```bash
# 仮想環境をアクティベート
source venv/bin/activate

# 基本的な記事生成・投稿
python generate_and_publish.py "ElixirのGenServerの使い方"

# テンプレートを指定
python generate_and_publish.py "React Hooksの活用法" --template tips --lang JavaScript

# 記事生成のみ（投稿しない）
python generate_and_publish.py "Docker入門" --generate-only

# 投稿のみ（生成済みJSONを使用）
python generate_and_publish.py --publish-only
```

## トピック入力方式

### 1. 通常の引数指定（複数行対応）

```bash
# 単一行トピック
python generate_and_publish.py "Elixirの並行処理入門"

# 複数行トピック（引用符内で改行）
python generate_and_publish.py "Elixirの並行処理入門

ActorモデルとTaskの基本概念から
実際のプロダクションでの使用例まで
段階的に解説していきます"
```

### 2. ファイル指定

```bash
# トピックファイルから読み込み
python generate_and_publish.py --topic-file sample_topic.txt --template deep-dive

# sample_topic.txt の内容例:
# Elixirの並行処理とGenServerの実践的活用法
# 
# 本記事では、Elixirの並行処理の核となるGenServerについて、
# 基本概念から実際のプロダクションでの使用例まで段階的に解説します。
# 
# 具体的には以下の内容を扱います：
# - GenServerの基本的な仕組みとActorモデル
# - 状態管理とメッセージパッシング
# - エラーハンドリングとスーパーバイザーツリー
```

### 3. 対話式入力

```bash
# 対話式入力を明示的に指定
python generate_and_publish.py --interactive --template tutorial

# トピック未指定時は自動的に対話式入力
python generate_and_publish.py --template tips
# > トピックを入力してください（複数行可、Ctrl+D（Mac/Linux）またはCtrl+Z（Windows）で終了）:
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
- `topic`: 記事のトピック（複数行可、`--publish-only`時は不要）

### トピック入力オプション
- `--topic-file`: トピックファイルのパス
- `--interactive, -i`: 対話式トピック入力

### オプションパラメータ
- `--template, -t`: 記事テンプレート（デフォルト: tutorial）
- `--lang, -l`: プログラミング言語
- `--audience, -a`: 対象読者（カスタム指定）
- `--length`: 記事の長さ（短い/中程度/長い）
- `--model, -m`: OpenAIモデル（デフォルト: gpt-4o-mini）
- `--token`: Qiita Access Token
- `--private`: プライベート記事として投稿（デフォルト）
- `--generate-only`: 記事生成のみ
- `--publish-only`: 投稿のみ

## 利用可能なOpenAIモデル

| モデル | 説明 | 品質 | コスト | 用途 |
|--------|------|------|--------|------|
| `gpt-4o-mini` | 軽量版GPT-4o（デフォルト） | 良い | 安い | 一般的な記事生成 |
| `gpt-4o` | 最新のGPT-4 Optimized | 最高 | 高い | 高品質記事・複雑なトピック |
| `gpt-4-turbo` | GPT-4 Turbo | 高い | 中程度 | バランス重視 |

**推奨**:
- **開発・テスト**: `gpt-4o-mini`（デフォルト）
- **高品質記事**: `gpt-4o`
- **コストバランス**: `gpt-4-turbo`

## 使用例

### 1. 初心者向けチュートリアル記事

```bash
source venv/bin/activate
python generate_and_publish.py "Pythonでのファイル操作入門" \
  --template tutorial \
  --lang Python \
  --audience "Python初心者"
```

### 2. 実用的なTips記事

```bash
source venv/bin/activate
python generate_and_publish.py "VS Codeの便利なショートカット10選" \
  --template tips \
  --length "中程度"
```

### 3. 技術比較記事

```bash
source venv/bin/activate
python generate_and_publish.py "Next.js vs Nuxt.js 2024年版比較" \
  --template comparison \
  --lang JavaScript
```

### 4. トラブルシューティング記事

```bash
source venv/bin/activate
python generate_and_publish.py "Docker Composeでよくあるエラーと解決法" \
  --template troubleshooting \
  --audience "DevOpsエンジニア"
```

### 5. 高性能モデルでの記事生成

```bash
source venv/bin/activate

# GPT-4oで高品質な記事を生成
python generate_and_publish.py "Rustの所有権システムの仕組み" \
  --template deep-dive \
  --lang Rust \
  --model gpt-4o \
  --length "長い"

# GPT-4 Turboで技術比較記事
python generate_and_publish.py "TypeScript vs JavaScript 2024年版" \
  --template comparison \
  --model gpt-4-turbo
```

### 6. 段階的ワークフロー

```bash
source venv/bin/activate

# 1. 記事生成のみ
python generate_and_publish.py "Elixirの並行処理入門" --template tutorial --generate-only

# 2. 生成された記事を確認・編集

# 3. 投稿のみ
python generate_and_publish.py --publish-only
```

### 7. 複数行トピックでの詳細指定

```bash
source venv/bin/activate

# 複数行トピックで詳細な要求を指定
python generate_and_publish.py "Elixirの並行処理とGenServer

本記事では以下の内容を段階的に解説します：
- ActorモデルとTaskの基本概念
- GenServerの実装パターン
- エラーハンドリングとスーパーバイザー
- 実際のプロダクションでの使用例" \
  --template deep-dive \
  --lang Elixir
```

### 8. ファイル指定での構造化トピック

```bash
source venv/bin/activate

# 事前に作成したトピックファイルを使用
python generate_and_publish.py --topic-file sample_topic.txt \
  --template tutorial \
  --lang Elixir \
  --model gpt-4o
```

### 9. 対話式入力での柔軟な記事作成

```bash
source venv/bin/activate

# 対話式でトピックを入力
python generate_and_publish.py --interactive \
  --template tips \
  --lang Python
# トピック入力画面が表示され、複数行での詳細な指定が可能
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
   ModuleNotFoundError: No module named 'openai'
   ```
   → `source venv/bin/activate`で仮想環境をアクティベート

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

## プロジェクト構造

```
ai-article-generator/
├── venv/                    # 統一仮想環境
├── requirements.txt         # 全依存関係
├── generate_and_publish.py  # メインスクリプト
├── .env                    # Qiita Access Token
├── python/
│   ├── article_generator.py # 記事生成モジュール
│   └── .env                # OpenAI API Key
└── elixir/                 # Qiita投稿モジュール
```
