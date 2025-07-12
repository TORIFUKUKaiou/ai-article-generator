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
    
    # Python仮想環境の確認
    venv_path = PYTHON_DIR / "venv"
    if not venv_path.exists():
        print("❌ Python仮想環境が見つかりません")
        print(f"   以下のコマンドで作成してください:")
        print(f"   cd {PYTHON_DIR} && python -m venv venv")
        return False
    
    print("✅ 環境設定OK")
    return True

def generate_article(topic, template_type, programming_language=None, custom_params=None, model="gpt-4o-mini"):
    """記事を生成"""
    print(f"📝 記事生成中: {topic}")
    print(f"🤖 使用モデル: {model}")
    
    template = ARTICLE_TEMPLATES.get(template_type, ARTICLE_TEMPLATES["tutorial"])
    
    # 一時的なPythonスクリプトファイルを作成
    temp_script = PYTHON_DIR / "temp_generate.py"
    
    script_content = f"""
import sys
sys.path.append('{PYTHON_DIR}')
from article_generator import ArticleGenerator

generator = ArticleGenerator(model='{model}')

# カスタムパラメータの適用
custom_params = {custom_params or {}}
target_audience = custom_params.get('target_audience', '{template["target_audience"]}')
article_length = custom_params.get('article_length', '{template["article_length"]}')

article = generator.generate_article(
    topic='{topic}',
    target_audience=target_audience,
    article_length=article_length,
    programming_language={repr(programming_language)}
)

print("✅ 記事生成完了!")
print(f"   タイトル: {{article.title}}")
print(f"   タグ: {{[tag['name'] for tag in article.tags]}}")
print(f"   本文長: {{len(article.body)}}文字")

generator.save_article_json(article, '{PYTHON_DIR}/generated_article.json')
print("💾 JSONファイルに保存しました")
"""
    
    try:
        # 一時スクリプトファイルに書き込み
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Python仮想環境でスクリプト実行
        cmd = f"cd {PYTHON_DIR} && source venv/bin/activate && python temp_generate.py"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # 一時ファイルを削除
        temp_script.unlink(missing_ok=True)
        
        if result.returncode != 0:
            print(f"❌ 記事生成エラー: {result.stderr}")
            return False
            
        print(result.stdout)
        return True
        
    except Exception as e:
        # 一時ファイルを削除
        temp_script.unlink(missing_ok=True)
        print(f"❌ 記事生成中にエラー: {e}")
        return False

def publish_article(access_token, private=True):
    """記事をQiitaに投稿"""
    print("🚀 Qiitaに投稿中...")
    
    # 一時的なElixirスクリプトファイルを作成
    temp_script = ELIXIR_DIR / "temp_publish.exs"
    
    script_content = f'''
access_token = "{access_token}"
json_path = "{PYTHON_DIR}/generated_article.json"

case QiitaPublisher.PythonBridge.publish_from_json(access_token, json_path) do
  {{:ok, response}} ->
    IO.puts("✅ 投稿成功!")
    IO.puts("   タイトル: " <> response["title"])
    IO.puts("   URL: " <> response["url"])
    IO.puts("   プライベート: " <> to_string(response["private"]))
  {{:error, reason}} ->
    IO.puts("❌ 投稿エラー: " <> inspect(reason))
    System.halt(1)
end
'''
    
    try:
        # 一時スクリプトファイルに書き込み
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        cmd = f"cd {ELIXIR_DIR} && mix run {temp_script.name}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # 一時ファイルを削除
        temp_script.unlink(missing_ok=True)
        
        if result.returncode != 0:
            print(f"❌ 投稿エラー: {result.stderr}")
            return False
            
        print(result.stdout)
        return True
        
    except Exception as e:
        # 一時ファイルを削除
        temp_script.unlink(missing_ok=True)
        print(f"❌ 投稿中にエラー: {e}")
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
    
    parser.add_argument("topic", help="記事のトピック")
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
    
    # カスタムパラメータの構築
    custom_params = {}
    if args.audience:
        custom_params['target_audience'] = args.audience
    if args.length:
        custom_params['article_length'] = args.length
    
    # 記事生成
    if not args.publish_only:
        print(f"📋 設定:")
        print(f"   トピック: {args.topic}")
        print(f"   テンプレート: {args.template} ({ARTICLE_TEMPLATES[args.template]['description']})")
        print(f"   モデル: {args.model}")
        if args.lang:
            print(f"   言語: {args.lang}")
        if custom_params:
            print(f"   カスタム設定: {custom_params}")
        print()
        
        if not generate_article(args.topic, args.template, args.lang, custom_params, args.model):
            sys.exit(1)
    
    # 記事投稿
    if not args.generate_only:
        access_token = args.token or os.getenv("QIITA_ACCESS_TOKEN")
        if not access_token:
            print("❌ Qiita Access Tokenが設定されていません")
            print("   --token オプションまたは環境変数QIITA_ACCESS_TOKENを設定してください")
            sys.exit(1)
        
        if not publish_article(access_token, args.private):
            sys.exit(1)
    
    print("\n🎉 完了!")

if __name__ == "__main__":
    main()
