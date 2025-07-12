#!/usr/bin/env python3
"""
AI Article Generator & Publisher
記事を生成してQiitaに投稿する統合スクリプト
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルートを取得
PROJECT_ROOT = Path(__file__).parent
PYTHON_DIR = PROJECT_ROOT / "python"
ELIXIR_DIR = PROJECT_ROOT / "elixir" / "qiita_publisher"

# Pythonモジュールをインポートするためにパスを追加
sys.path.append(str(PROJECT_ROOT / "python"))
from article_generator import ArticleGenerator, ArticleData

# 記事テンプレート定義
ARTICLE_TEMPLATES = {
    "tutorial": {
        "description": "初心者向けチュートリアル記事",
        "target_audience": "初心者エンジニア",
        "article_length": "長い",
        "style": "丁寧で段階的な解説"
    },
    "tips": {
        "description": "実用的なTips・小技記事", 
        "target_audience": "中級エンジニア",
        "article_length": "中程度",
        "style": "すぐに使える実践的な内容"
    },
    "deep-dive": {
        "description": "技術の深掘り解説記事",
        "target_audience": "上級エンジニア", 
        "article_length": "長い",
        "style": "詳細な技術解説と背景"
    },
    "comparison": {
        "description": "技術比較・選択指針記事",
        "target_audience": "エンジニア全般",
        "article_length": "中程度", 
        "style": "客観的な比較と判断基準"
    },
    "troubleshooting": {
        "description": "問題解決・トラブルシューティング記事",
        "target_audience": "実務エンジニア",
        "article_length": "中程度",
        "style": "具体的な問題と解決手順"
    }
}

def setup_environment():
    """環境設定の確認"""
    print("🔧 環境設定を確認中...")
    
    # プロジェクトルートの.envファイルを読み込み
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print("✅ .envファイルを読み込みました")
    else:
        print("⚠️  .envファイルが見つかりません（オプション）")
    
    # 統一仮想環境の確認
    venv_path = PROJECT_ROOT / "venv"
    if not venv_path.exists():
        print("❌ Python仮想環境が見つかりません")
        print(f"   以下のコマンドで作成してください:")
        print(f"   python -m venv venv")
        print(f"   source venv/bin/activate")
        print(f"   pip install -r requirements.txt")
        return False
    
    print("✅ 環境設定OK")
    return True

def generate_article(topic, template_type, programming_language=None, custom_params=None, model="gpt-4o-mini"):
    """記事を生成 (リファクタリング版)"""
    print(f"📝 記事生成中: {topic}")
    print(f"🤖 使用モデル: {model}")

    try:
        template = ARTICLE_TEMPLATES.get(template_type, ARTICLE_TEMPLATES["tutorial"])
        
        # パラメータを決定
        target_audience = custom_params.get('target_audience', template["target_audience"])
        article_length = custom_params.get('article_length', template["article_length"])

        # ArticleGeneratorを直接呼び出し
        generator = ArticleGenerator(model=model)
        article = generator.generate_article(
            topic=topic,
            target_audience=target_audience,
            article_length=article_length,
            programming_language=programming_language,
            template_style=template_type
        )

        print("✅ 記事生成完了!")
        print(f"   タイトル: {article.title}")
        print(f"   タグ: {[tag['name'] for tag in article.tags]}")
        print(f"   本文長: {len(article.body)}文字")

        # JSONファイルに保存
        output_path = PYTHON_DIR / "generated_article.json"
        generator.save_article_json(article, str(output_path))
        print(f"💾 JSONファイルを {output_path} に保存しました")
        return True

    except Exception as e:
        print(f"❌ 記事生成中にエラー: {e}")
        return False

def get_topic(args):
    """トピックを取得（複数の入力方式に対応）"""
    if args.topic_file:
        # ファイルからトピック読み込み
        try:
            with open(args.topic_file, 'r', encoding='utf-8') as f:
                topic = f.read().strip()
                print(f"📄 ファイルからトピックを読み込みました: {args.topic_file}")
                return topic
        except FileNotFoundError:
            print(f"❌ エラー: ファイルが見つかりません: {args.topic_file}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ エラー: ファイル読み込み中にエラー: {e}")
            sys.exit(1)
    
    elif args.interactive:
        # 対話式入力
        print("📝 トピックを入力してください（複数行可、Ctrl+D（Mac/Linux）またはCtrl+Z（Windows）で終了）:")
        print("=" * 50)
        try:
            topic = sys.stdin.read().strip()
            if not topic:
                print("❌ エラー: トピックが入力されませんでした")
                sys.exit(1)
            print("=" * 50)
            print("✅ トピックを受け取りました")
            return topic
        except KeyboardInterrupt:
            print("\n❌ 入力がキャンセルされました")
            sys.exit(1)
    
    elif args.topic:
        # 通常の引数指定（複数行対応）
        return args.topic
    
    else:
        # トピック未指定時は対話式に切り替え
        print("💡 トピックが指定されていません。対話式入力に切り替えます。")
        print("📝 トピックを入力してください（複数行可、Ctrl+D（Mac/Linux）またはCtrl+Z（Windows）で終了）:")
        print("=" * 50)
        try:
            topic = sys.stdin.read().strip()
            if not topic:
                print("❌ エラー: トピックが入力されませんでした")
                sys.exit(1)
            print("=" * 50)
            print("✅ トピックを受け取りました")
            return topic
        except KeyboardInterrupt:
            print("\n❌ 入力がキャンセルされました")
            sys.exit(1)

def publish_article(access_token):
    """記事をQiitaに投稿 (シェルスクリプト使用)"""
    print("🚀 Qiitaに投稿中...")
    json_path = PYTHON_DIR / "generated_article.json"
    
    if not json_path.exists():
        print(f"❌ 投稿用のJSONファイルが見つかりません: {json_path}")
        return False

    # 専用シェルスクリプトを実行
    script_path = ELIXIR_DIR.parent / "publish_to_qiita.sh"
    
    try:
        result = subprocess.run(
            [str(script_path), access_token, str(json_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 投稿エラー:")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ 投稿中に予期せぬエラー: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="AI記事生成・投稿ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
記事テンプレート:
{chr(10).join([f"  {k}: {v['description']}" for k, v in ARTICLE_TEMPLATES.items()])}

使用例:
  python generate_and_publish.py "ElixirのGenServerの使い方" --template tutorial --lang Elixir
  python generate_and_publish.py "React vs Vue.js" --template comparison --lang JavaScript
  python generate_and_publish.py "Docker環境構築" --template troubleshooting --audience "DevOpsエンジニア"
        """
    )
    
    parser.add_argument("topic", nargs='?', help="記事のトピック（複数行可）")
    parser.add_argument("--topic-file", help="トピックファイルのパス")
    parser.add_argument("--interactive", "-i", action="store_true", help="対話式トピック入力")
    parser.add_argument("--template", "-t", 
                       choices=list(ARTICLE_TEMPLATES.keys()),
                       default="tutorial",
                       help="記事テンプレート (デフォルト: tutorial)")
    parser.add_argument("--lang", "-l", help="プログラミング言語")
    parser.add_argument("--audience", "-a", help="対象読者")
    parser.add_argument("--length", choices=["短い", "中程度", "長い"], help="記事の長さ")
    parser.add_argument("--model", "-m", default="gpt-4o-mini", 
                       help="OpenAIモデル (デフォルト: gpt-4o-mini)")
    parser.add_argument("--token", help="Qiita Access Token (環境変数QIITA_ACCESS_TOKENからも取得可能)")
    parser.add_argument("--private", action="store_true", default=True, help="プライベート記事として投稿")
    parser.add_argument("--generate-only", action="store_true", help="記事生成のみ（投稿しない）")
    parser.add_argument("--publish-only", action="store_true", help="投稿のみ（生成済みJSONを使用）")
    
    args = parser.parse_args()
    
    print("🤖 AI Article Generator & Publisher")
    print("=" * 50)
    
    # 環境設定確認
    if not setup_environment():
        sys.exit(1)
    
    # topicの取得（複数の入力方式に対応）
    if not args.publish_only:
        topic = get_topic(args)
        if not topic:
            print("❌ エラー: 記事生成にはトピックが必要です")
            sys.exit(1)
    else:
        topic = None
    
    # カスタムパラメータの構築
    custom_params = {}
    if args.audience:
        custom_params['target_audience'] = args.audience
    if args.length:
        custom_params['article_length'] = args.length
    
    # 記事生成
    if not args.publish_only:
        if not topic:
            print("❌ エラー: 記事生成にはトピックが必要です")
            sys.exit(1)
            
        print(f"📋 設定:")
        print(f"   トピック: {topic}")
        print(f"   テンプレート: {args.template} ({ARTICLE_TEMPLATES[args.template]['description']})")
        print(f"   モデル: {args.model}")
        if args.lang:
            print(f"   言語: {args.lang}")
        if custom_params:
            print(f"   カスタム設定: {custom_params}")
        print()
        
        if not generate_article(topic, args.template, args.lang, custom_params, args.model):
            sys.exit(1)
    
    # 記事投稿
    if not args.generate_only:
        access_token = args.token or os.getenv("QIITA_ACCESS_TOKEN")
        if not access_token:
            print("❌ Qiita Access Tokenが設定されていません")
            print("   --token オプションまたは環境変数QIITA_ACCESS_TOKENを設定してください")
            sys.exit(1)
        
        if not publish_article(access_token):
            sys.exit(1)
    
    print("\n🎉 完了!")

if __name__ == "__main__":
    main()
