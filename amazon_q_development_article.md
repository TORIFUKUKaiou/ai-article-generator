# Amazon Q CLIと一緒に作る！AI記事生成・投稿システム開発記

## はじめに

「AIで記事を自動生成してQiitaに投稿できたら便利だな...」

そんな思いつきから始まった開発が、Amazon Q CLIとのペアプログラミングによって、わずか数時間で本格的なシステムに進化しました。この記事では、実際の開発過程を振り返りながら、AI支援開発の魅力と技術的な詳細を紹介します。

## 完成したシステム概要

最終的に完成したのは、以下の機能を持つ統合システムです：

```bash
# 一行で記事生成・投稿が完了
python generate_and_publish.py "Elixirの並行処理入門" --template tutorial --lang Elixir --model gpt-4o
```

### 主な機能
- **5つの記事テンプレート**（tutorial, tips, deep-dive, comparison, troubleshooting）
- **OpenAIモデル選択**（gpt-4o-mini〜gpt-4o）
- **Python-Elixir連携**による堅牢な投稿システム
- **柔軟なワークフロー**（生成のみ、投稿のみも可能）

## 開発の始まり：「記事生成だけでも...」

### 最初のリクエスト
```
私: 「OpenAI APIを使って技術記事を生成するPythonスクリプトを作りたい」
```

Amazon Q CLIは即座に基本的な構造を提案してくれました：

```python
class ArticleGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    
    def generate_article(self, topic: str, target_audience: str = "エンジニア"):
        # 記事生成ロジック
```

**ここでの学び**: AIは基本構造を素早く提供してくれるので、アイデアを形にするスピードが格段に上がります。

## 進化の過程：「もっと高品質な記事を」

### プロンプトエンジニアリング
単純な記事生成では物足りなくなり、「1000いいねを獲得する記事」を目指すことに。

```
私: 「1000いいねを獲得するような高品質な記事にしたい」
```

Amazon Q CLIが提案したプロンプト改善：

```python
system_prompt = """あなたは1000いいねを獲得する技術記事を書く専門家です。

【1000いいね獲得のポイント】:
- 実用的で即座に使える具体的なコード例
- 初心者にも分かりやすい丁寧な解説
- 「なぜそうするのか」の理由も説明
- ハマりやすいポイントと解決策を含める
- 読者の「知りたかった！」に応える内容
"""
```

**ここでの学び**: AIとの対話を通じて、プロンプトを段階的に改善できます。一人では思いつかない視点も得られました。

## 技術的な挑戦：Python-Elixir連携

### 「Qiitaに自動投稿もしたい」
記事生成だけでは満足できず、投稿の自動化も要求しました。

```
私: 「ElixirでQiita APIクライアントを作って、Pythonと連携させたい」
```

Amazon Q CLIは即座にElixirのHTTPクライアント実装を提案：

```elixir
defmodule QiitaPublisher.ArticleService do
  def publish_article(access_token, article_data) do
    client = Req.new(
      base_url: "https://qiita.com/api/v2",
      headers: [
        {"Authorization", "Bearer #{access_token}"},
        {"Content-Type", "application/json"}
      ]
    )
    
    Req.post(client, url: "/items", json: article_data)
  end
end
```

### 連携の仕組み
1. **Python**: OpenAI APIで記事生成 → JSON保存
2. **Elixir**: JSONファイル読み込み → Qiita API投稿

```python
# Python側
generator.save_article_json(article, "generated_article.json")

# Elixir側（統合スクリプトから呼び出し）
QiitaPublisher.PythonBridge.publish_from_json(access_token, json_path)
```

**ここでの学び**: 異なる言語間の連携も、AIの提案により自然に実現できました。

## 実際の問題解決：タグ解析のバグ

開発中に遭遇した実際の問題と解決過程を紹介します。

### 問題発生
```
🏷️  Tags: [nil, nil, nil, nil, nil]
```

タグ名が`nil`になってしまう問題が発生。

### 問題分析
```
私: 「タグがおかしいので変更してみて。」
```

Amazon Q CLIは即座に原因を特定：

```python
# 問題のあるコード
tag_names = [tag.strip() for tag in tag_str.split(',')]

# 修正後
tag_str = tag_str.strip('[]')  # 角括弧を除去
tag_names = [tag.strip().strip('[]') for tag in tag_str.split(',')]
tag_names = [name for name in tag_names if name and len(name) > 0]
```

**ここでの学び**: バグの説明をすると、AIが原因を特定して修正案を提示してくれます。デバッグ効率が大幅に向上しました。

## システムの進化：統合スクリプトの誕生

### 「パラメータで記事の方向性を指定したい」
個別のスクリプトでは使いにくくなり、統合的なソリューションを要求：

```
私: 「スクリプトにしてほしい。いろいろな記事を作成できるようにパラメータで記事の方向性とかを指定できるようにしてほしい。」
```

Amazon Q CLIが提案した統合スクリプト：

```python
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
    # ... 他のテンプレート
}
```

### 柔軟な実行オプション
```bash
# 基本的な使用
python generate_and_publish.py "ElixirのGenServerの使い方"

# 詳細指定
python generate_and_publish.py "React Hooksの活用法" \
  --template tips \
  --lang JavaScript \
  --model gpt-4o

# 段階的実行
python generate_and_publish.py "Docker入門" --generate-only
python generate_and_publish.py --publish-only
```

## 技術的な詳細解説

### アーキテクチャ概要

```mermaid
graph LR
    A[統合スクリプト] --> B[Python記事生成]
    B --> C[OpenAI API]
    B --> D[JSON保存]
    D --> E[Elixir投稿システム]
    E --> F[Qiita API]
```

### 環境変数の設計
セキュリティと使いやすさを両立する設計：

```bash
# プロジェクトルート/.env（統合スクリプト用）
QIITA_ACCESS_TOKEN=your_token

# python/.env（記事生成用）
OPENAI_API_KEY=your_key
```

### エラーハンドリング
実用的なシステムには堅牢なエラー処理が必要：

```python
def setup_environment():
    """環境設定の確認"""
    if not env_file.exists():
        print("⚠️  .envファイルが見つかりません（オプション）")
    
    if not venv_path.exists():
        print("❌ Python仮想環境が見つかりません")
        print(f"   以下のコマンドで作成してください:")
        return False
```

## AI支援開発の魅力

### 1. **高速プロトタイピング**
アイデアから動作するプロトタイプまでの時間が劇的に短縮されます。

### 2. **技術的な壁の突破**
知らない技術（今回はElixir）でも、AIの支援により実装できました。

### 3. **コード品質の向上**
AIが提案するコードは、ベストプラクティスに従っていることが多く、学習効果も高いです。

### 4. **問題解決の効率化**
バグや課題に遭遇した際の解決スピードが格段に向上します。

## 実際の使用感

### 生成される記事の品質
```bash
python generate_and_publish.py "Elixirの並行処理入門" --template tutorial --lang Elixir
```

**結果**:
- タイトル: Elixirの並行処理入門 - 簡単に使えるActorモデルとTaskを理解しよう
- 本文長: 2,448文字
- 適切なタグ付け
- 実用的なコード例を含む高品質な記事

### パフォーマンス
- **記事生成時間**: 約30-60秒（モデルにより変動）
- **投稿処理**: 数秒
- **総実行時間**: 1分程度

## 今後の展望

### 機能拡張のアイデア
- **画像生成**: DALL-E APIとの連携
- **多言語対応**: 英語記事の生成
- **SEO最適化**: メタデータの自動生成
- **スケジュール投稿**: 定期的な記事投稿

### 他プラットフォーム対応
- **Zenn**: Zenn APIとの連携
- **note**: note APIとの連携
- **Medium**: Medium APIとの連携

## まとめ

Amazon Q CLIとのペアプログラミングにより、単純なアイデアが本格的なシステムに進化しました。AI支援開発の魅力は以下の点にあります：

1. **アイデアの高速実現**: 思いついたらすぐに形にできる
2. **技術的制約の突破**: 知らない技術でも実装可能
3. **継続的な改善**: 対話を通じた段階的な品質向上
4. **学習効果**: AIとの協働で新しい知識を獲得

### 開発のコツ
- **具体的な要求**: 「〜したい」を明確に伝える
- **段階的な改善**: 一度に完璧を求めず、徐々に改良
- **積極的な質問**: 分からないことは遠慮なく聞く
- **実験精神**: 新しいアイデアを恐れずに試す

AI支援開発は、プログラマーの創造性を制限するものではなく、むしろ拡張するツールです。Amazon Q CLIのような優秀なAIパートナーと一緒に、あなたも次の革新的なプロジェクトを始めてみませんか？

## 参考リンク

- [完成したプロジェクト（GitHub）](#) ※公開予定
- [Amazon Q CLI公式ドキュメント](https://docs.aws.amazon.com/amazonq/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Qiita API v2](https://qiita.com/api/v2/docs)

---

**この記事が、AI支援開発に興味を持つエンジニアの参考になれば幸いです。質問やコメントをお待ちしています！** 🚀
