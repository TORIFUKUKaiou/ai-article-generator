# API Integration Guidelines

## OpenAI API Integration

### Model Selection Strategy
- **gpt-4o-mini**: Default for development and general articles (cost-effective)
- **gpt-4o**: High-quality articles and complex topics (premium quality)
- **gpt-4-turbo**: Balanced approach for production use

### Prompt Engineering Best Practices
- Use system prompts to establish expert persona
- Include specific quality requirements (1000+ likes target)
- Provide clear structure and formatting instructions
- Include template-specific requirements
- Specify target audience and technical level

### Content Generation Standards
```python
# Prompt structure pattern
system_prompt = """You are an expert technical writer who creates 1000+ like articles.
Focus on practical, immediately usable content with detailed code examples."""

user_prompt = f"""
Topic: {topic}
Template: {template_type}
Audience: {target_audience}
Length: {article_length}
Language: {programming_language}
"""
```

## Qiita API Integration

### Publishing Workflow
1. **Validation**: Verify article structure and required fields
2. **Authentication**: Use Bearer token authentication
3. **Error Handling**: Implement retry logic for transient failures
4. **Response Processing**: Extract article URL and metadata

### API Client Patterns
```elixir
# Elixir HTTP client pattern using Req
def create_item(client, params) do
  case Req.post(client, url: "/items", json: params) do
    {:ok, %{status: 201, body: body}} -> {:ok, body}
    {:ok, %{status: status, body: body}} -> {:error, {status, body}}
    {:error, reason} -> {:error, reason}
  end
end
```

### Rate Limiting and Retry Logic
- Implement exponential backoff for failed requests
- Respect API rate limits (Qiita: 1000 requests/hour)
- Log API interactions for debugging
- Handle authentication errors gracefully

## Data Format Standards

### Article JSON Structure
```json
{
  "title": "Article Title",
  "body": "Markdown content",
  "tags": [{"name": "tag_name", "versions": []}],
  "private": true,
  "tweet": false
}
```

### Tag Processing
- Validate tag names against Qiita requirements
- Handle both string and object tag formats
- Provide fallback tags when extraction fails
- Limit tag count to Qiita's maximum (5 tags)