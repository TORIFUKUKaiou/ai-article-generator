# Development Standards

## Code Quality Standards

### Python Code Standards
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Implement comprehensive error handling with specific exception types
- Use dataclasses for structured data (like ArticleData)
- Include docstrings for all public functions and classes
- Use environment variables for configuration (python/.env)

### Elixir Code Standards
- Follow Elixir community conventions
- Use pattern matching for control flow
- Implement proper error tuples {:ok, result} | {:error, reason}
- Use GenServer for stateful processes when needed
- Include @moduledoc and @doc for all public modules and functions
- Use Req library for HTTP client operations

### Shell Script Standards
- Use `set -e` for error handling
- Include usage instructions and parameter validation
- Provide clear error messages with emoji indicators
- Use absolute paths when necessary

## Error Handling Patterns

### Python Layer
```python
try:
    # Operation
    result = operation()
    return result
except SpecificException as e:
    print(f"❌ Error: {e}")
    return False
```

### Elixir Layer
```elixir
case operation() do
  {:ok, result} -> {:ok, result}
  {:error, reason} -> {:error, "Operation failed: #{reason}"}
end
```

## Testing Requirements
- Unit tests for core functionality
- Integration tests for API interactions
- Error case testing for all failure modes
- Mock external API calls in tests