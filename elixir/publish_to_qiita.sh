#!/bin/bash
# Qiita記事投稿スクリプト
# 使用方法: ./publish_to_qiita.sh <access_token> <json_path>

set -e  # エラー時に停止

# 引数チェック
if [ $# -ne 2 ]; then
    echo "使用方法: $0 <access_token> <json_path>"
    echo "例: $0 your_token_here /path/to/article.json"
    exit 1
fi

ACCESS_TOKEN="$1"
JSON_PATH="$2"

# JSONファイルの存在確認
if [ ! -f "$JSON_PATH" ]; then
    echo "❌ JSONファイルが見つかりません: $JSON_PATH"
    exit 1
fi

echo "🚀 Qiita投稿準備中..."

# Elixirプロジェクトディレクトリに移動
cd "$(dirname "$0")/qiita_publisher"

# 依存関係の取得（初回またはmix.lockが更新された場合）
echo "📦 依存関係を確認中..."
mix deps.get

# 投稿実行
echo "📝 記事を投稿中..."
mix run -e "
case QiitaPublisher.PythonBridge.publish_from_json(\"$ACCESS_TOKEN\", \"$JSON_PATH\") do
  {:ok, response} ->
    IO.puts(\"✅ 投稿成功!\")
    IO.puts(\"   タイトル: \" <> response[\"title\"])
    IO.puts(\"   URL: \" <> response[\"url\"])
    IO.puts(\"   プライベート: \" <> to_string(response[\"private\"]))
  {:error, reason} ->
    IO.puts(\"❌ 投稿エラー: \" <> inspect(reason))
    System.halt(1)
end
"

echo "🎉 投稿完了!"
