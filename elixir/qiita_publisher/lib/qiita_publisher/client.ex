defmodule QiitaPublisher.Client do
  @moduledoc """
  Qiita API client using Req
  """

  @base_url "https://qiita.com/api/v2"

  def new(access_token) do
    Req.new(
      base_url: @base_url,
      headers: [
        {"Authorization", "Bearer #{access_token}"},
        {"Content-Type", "application/json"}
      ]
    )
  end

  def create_item(client, params) do
    Req.post(client, url: "/items", json: params)
  end

  def get_items(client, opts \\ []) do
    Req.get(client, url: "/items", params: opts)
  end

  def get_item(client, item_id) do
    Req.get(client, url: "/items/#{item_id}")
  end

  def update_item(client, item_id, params) do
    Req.patch(client, url: "/items/#{item_id}", json: params)
  end

  def delete_item(client, item_id) do
    Req.delete(client, url: "/items/#{item_id}")
  end

  def get_authenticated_user(client) do
    Req.get(client, url: "/authenticated_user")
  end
end
