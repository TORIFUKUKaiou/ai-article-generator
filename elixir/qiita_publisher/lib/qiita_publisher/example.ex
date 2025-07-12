defmodule QiitaPublisher.Example do
  @moduledoc """
  Usage examples for QiitaPublisher
  """

  alias QiitaPublisher.ArticleService

  def sample_article do
    %{
      title: "ElixirでQiita APIを使ってみた",
      body: """
      # はじめに

      ElixirのReqライブラリを使ってQiita APIにアクセスしてみました。

      ## 実装

      ```elixir
      defmodule QiitaClient do
        def create_article(access_token, params) do
          Req.post("https://qiita.com/api/v2/items",
            headers: [{"Authorization", "Bearer " <> access_token}],
            json: params
          )
        end
      end
      ```

      ## まとめ

      Reqライブラリを使うことで、簡潔にHTTPクライアントを実装できました。
      """,
      tags: [
        %{name: "Elixir", versions: []},
        %{name: "Qiita", versions: []},
        %{name: "API", versions: []}
      ],
      private: true,
      tweet: false
    }
  end

  def publish_sample_article(access_token) do
    article = sample_article()
    
    case ArticleService.validate_article(article) do
      :ok ->
        ArticleService.publish_article(access_token, article)
      {:error, reason} ->
        {:error, "Validation failed: #{reason}"}
    end
  end

  def test_connection(access_token) do
    client = QiitaPublisher.Client.new(access_token)
    QiitaPublisher.Client.get_authenticated_user(client)
  end
end
