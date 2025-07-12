"""
AI Article Generator for Qiita
OpenAI APIを使用して技術記事を自動生成する
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

@dataclass
class ArticleData:
    """記事データの構造"""
    title: str
    body: str
    tags: List[Dict[str, any]]
    private: bool = True
    tweet: bool = False

class ArticleGenerator:
    """OpenAI APIを使用した記事生成クラス"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        初期化
        
        Args:
            api_key: OpenAI API Key (環境変数OPENAI_API_KEYから取得可能)
            model: 使用するOpenAIモデル (デフォルト: gpt-4o-mini)
        """
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.model = model
    
    def generate_article(
        self, 
        topic: str, 
        target_audience: str = "エンジニア",
        article_length: str = "中程度",
        programming_language: Optional[str] = None
    ) -> ArticleData:
        """
        指定されたトピックで記事を生成
        
        Args:
            topic: 記事のトピック
            target_audience: 対象読者
            article_length: 記事の長さ (短い/中程度/長い)
            programming_language: プログラミング言語 (指定がある場合)
            
        Returns:
            ArticleData: 生成された記事データ
        """
        
        # プロンプトを構築
        prompt = self._build_prompt(topic, target_audience, article_length, programming_language)
        
        try:
            # OpenAI APIを呼び出し
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": """あなたは1000いいねを獲得する技術記事を書く専門家です。Qiita向けの超高品質な技術記事をMarkdown形式で作成してください。

【1000いいね獲得のポイント】:
- 実用的で即座に使える具体的なコード例
- 初心者にも分かりやすい丁寧な解説
- 「なぜそうするのか」の理由も説明
- ハマりやすいポイントと解決策を含める
- 読者の「知りたかった！」に応える内容
- 適切な見出し構成で読みやすさを重視
- コードにはコメントを充実させる
- 実際のプロジェクトで使える実践的な内容"""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=4000,  # トークン数を増やす
                temperature=0.7
            )
            
            # レスポンスから記事内容を抽出
            article_content = response.choices[0].message.content
            
            # 記事データを構造化
            return self._parse_article_content(article_content, topic, programming_language)
            
        except Exception as e:
            raise Exception(f"記事生成中にエラーが発生しました: {str(e)}")
    
    def _build_prompt(
        self, 
        topic: str, 
        target_audience: str, 
        article_length: str,
        programming_language: Optional[str]
    ) -> str:
        """記事生成用のプロンプトを構築"""
        
        length_guide = {
            "短い": "1000-1500文字程度（基本的な説明と簡単な例）",
            "中程度": "2000-3000文字程度（詳細な説明と複数の例）", 
            "長い": "3500-5000文字程度（網羅的な説明と実践的な例）"
        }
        
        prompt = f"""
以下の条件で技術記事を作成してください：

【記事の基本情報】:
- トピック: {topic}
- 対象読者: {target_audience}
- 記事の長さ: {length_guide.get(article_length, "2000-3000文字程度")}
"""
    
        if programming_language:
            prompt += f"- 主要プログラミング言語: {programming_language}\n"
        
        prompt += f"""
【記事構成の要件】:
1. **魅力的なタイトル**: 具体的で読みたくなるタイトル
2. **はじめに**: 
   - この記事で何が学べるか
   - なぜこの技術が重要か
   - 記事の対象読者
3. **本文**: 
   - 段階的に理解できる構成
   - 実際に動くコード例（コメント付き）
   - つまずきやすいポイントの解説
   - 実践的な使用例
4. **まとめ**: 
   - 学んだことの要点
   - 次のステップの提案

【コード例の要件】:
- 実際に動作するコード
- 適切なコメント
- エラーハンドリングを含む
- 実践的な使用例

【対象読者: {target_audience}】に合わせた難易度で執筆してください。

実用的で読みやすく、実際の開発で役立つ記事を作成してください。
"""
    
        return prompt
    
    def _parse_article_content(
        self, 
        content: str, 
        topic: str,
        programming_language: Optional[str]
    ) -> ArticleData:
        """生成された記事内容を解析してArticleDataに変換"""
        
        lines = content.strip().split('\n')
        title = ""
        tags = []
        body = ""
        
        # タイトルとタグを抽出
        body_start = 0
        for i, line in enumerate(lines):
            if line.startswith("TITLE:"):
                title = line.replace("TITLE:", "").strip()
            elif line.startswith("TAGS:"):
                tag_str = line.replace("TAGS:", "").strip()
                # 角括弧を除去してからタグを分割
                tag_str = tag_str.strip('[]')
                tag_names = [tag.strip().strip('[]') for tag in tag_str.split(',')]
                # 空のタグや不正なタグを除外
                tag_names = [name for name in tag_names if name and len(name) > 0]
                tags = [{"name": name, "versions": []} for name in tag_names]
            elif line.startswith("BODY:"):
                body_start = i + 1
                break
        
        # 本文を抽出
        if body_start > 0:
            body = '\n'.join(lines[body_start:]).strip()
        else:
            body = content  # フォーマットが異なる場合は全体を本文とする
        
        # タイトルが抽出できない場合はトピックから生成
        if not title:
            title = f"{topic}について"
        
        # タグが抽出できない場合はデフォルトタグを設定
        if not tags:
            default_tags = ["技術記事"]
            if programming_language:
                default_tags.append(programming_language)
            tags = [{"name": name, "versions": []} for name in default_tags]
        
        return ArticleData(
            title=title,
            body=body,
            tags=tags,
            private=True,  # デフォルトでプライベート
            tweet=False
        )
    
    def save_article_json(self, article: ArticleData, filename: str) -> None:
        """記事データをJSONファイルに保存"""
        article_dict = {
            "title": article.title,
            "body": article.body,
            "tags": article.tags,
            "private": article.private,
            "tweet": article.tweet
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(article_dict, f, ensure_ascii=False, indent=2)

def main():
    """テスト用のメイン関数"""
    
    # 環境変数チェック
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY環境変数が設定されていません")
        return
    
    try:
        # 記事生成器を初期化（デフォルトモデル）
        generator = ArticleGenerator()
        print(f"🤖 使用モデル: {generator.model}")
        
        # サンプル記事を生成
        print("📝 記事を生成中...")
        article = generator.generate_article(
            topic="ElixirのReqライブラリの使い方",
            target_audience="Elixir初心者",
            article_length="中程度",
            programming_language="Elixir"
        )
        
        print("✅ 記事生成完了!")
        print(f"タイトル: {article.title}")
        print(f"タグ: {[tag['name'] for tag in article.tags]}")
        print(f"本文長: {len(article.body)}文字")
        
        # JSONファイルに保存
        generator.save_article_json(article, "generated_article.json")
        print("💾 generated_article.jsonに保存しました")
        
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()
