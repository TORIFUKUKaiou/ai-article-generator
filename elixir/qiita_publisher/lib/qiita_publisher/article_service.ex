defmodule QiitaPublisher.ArticleService do
  @moduledoc """
  Service for managing Qiita articles
  """

  alias QiitaPublisher.Client

  def publish_article(access_token, article_data) do
    client = Client.new(access_token)
    
    params = %{
      title: article_data.title,
      body: article_data.body,
      tags: format_tags(article_data.tags),
      private: Map.get(article_data, :private, false),
      tweet: Map.get(article_data, :tweet, false)
    }

    case Client.create_item(client, params) do
      {:ok, %{status: 201, body: response}} ->
        {:ok, response}
      {:ok, %{status: status, body: error}} ->
        {:error, {status, error}}
      {:error, reason} ->
        {:error, reason}
    end
  end

  def get_user_articles(access_token, opts \\ []) do
    client = Client.new(access_token)
    
    case Client.get_items(client, opts) do
      {:ok, %{status: 200, body: articles}} ->
        {:ok, articles}
      {:ok, %{status: status, body: error}} ->
        {:error, {status, error}}
      {:error, reason} ->
        {:error, reason}
    end
  end

  def validate_article(article_data) do
    required_fields = [:title, :body, :tags]
    
    missing_fields = 
      required_fields
      |> Enum.filter(fn field -> 
        not Map.has_key?(article_data, field) or 
        is_nil(Map.get(article_data, field)) or
        Map.get(article_data, field) == ""
      end)

    case missing_fields do
      [] -> :ok
      fields -> {:error, "Missing required fields: #{Enum.join(fields, ", ")}"}
    end
  end

  defp format_tags(tags) when is_list(tags) do
    Enum.map(tags, fn
      %{name: _name} = tag -> tag
      name when is_binary(name) -> %{name: name, versions: []}
      _ -> %{name: "misc", versions: []}
    end)
  end

  defp format_tags(_), do: []
end
