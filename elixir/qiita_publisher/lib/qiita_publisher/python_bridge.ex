defmodule QiitaPublisher.PythonBridge do
  @moduledoc """
  Python側で生成された記事をQiitaに投稿するブリッジモジュール
  """

  alias QiitaPublisher.ArticleService

  def publish_from_json(access_token, json_file_path) do
    case read_article_json(json_file_path) do
      {:ok, article_data} ->
        case ArticleService.validate_article(article_data) do
          :ok ->
            ArticleService.publish_article(access_token, article_data)
          {:error, reason} ->
            {:error, "Validation failed: #{reason}"}
        end
      {:error, reason} ->
        {:error, "Failed to read JSON: #{reason}"}
    end
  end

  def read_article_json(file_path) do
    case File.read(file_path) do
      {:ok, content} ->
        case Jason.decode(content, keys: :atoms) do
          {:ok, data} ->
            # タグの形式を正しく処理
            formatted_tags = format_tags(data.tags)
            
            article_data = %{
              title: data.title,
              body: data.body,
              tags: formatted_tags,
              private: Map.get(data, :private, true),
              tweet: Map.get(data, :tweet, false)
            }
            {:ok, article_data}
          {:error, reason} ->
            {:error, "JSON decode error: #{inspect(reason)}"}
        end
      {:error, reason} ->
        {:error, "File read error: #{inspect(reason)}"}
    end
  end

  defp format_tags(tags) when is_list(tags) do
    Enum.map(tags, fn tag ->
      case tag do
        %{name: name, versions: versions} -> 
          %{name: name, versions: versions}
        %{"name" => name, "versions" => versions} -> 
          %{name: name, versions: versions}
        %{name: name} -> 
          %{name: name, versions: []}
        %{"name" => name} -> 
          %{name: name, versions: []}
        name when is_binary(name) -> 
          %{name: name, versions: []}
        _ -> 
          %{name: "misc", versions: []}
      end
    end)
  end

  defp format_tags(_), do: []

  def publish_python_generated_article(access_token, python_project_path \\ "../../../python") do
    json_path = Path.join([python_project_path, "generated_article.json"])
    absolute_path = Path.expand(json_path, __DIR__)
    
    IO.puts("📖 Reading article from: #{absolute_path}")
    
    case File.exists?(absolute_path) do
      true ->
        publish_from_json(access_token, absolute_path)
      false ->
        {:error, "Generated article file not found: #{absolute_path}"}
    end
  end
end
