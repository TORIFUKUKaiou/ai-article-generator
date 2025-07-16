# Environment Configuration Guidelines

## Environment Variable Management

### Project Structure
- **Project Root `.env`**: Qiita Access Token for publishing
- **`python/.env`**: OpenAI API Key for article generation
- **Separate concerns**: Keep API keys isolated by component

### Required Environment Variables

#### Project Root `.env`
```bash
QIITA_ACCESS_TOKEN=your_qiita_access_token_here
```

#### `python/.env`
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Environment Setup Patterns
- Always provide `.env.sample` files as templates
- Use `python-dotenv` for loading environment variables
- Validate required environment variables at startup
- Provide clear error messages for missing configuration

### Virtual Environment Management
- Use unified virtual environment at project root (`venv/`)
- Single `requirements.txt` for all Python dependencies
- Activate virtual environment before running any Python scripts
- Include virtual environment check in main scripts

## Configuration Validation
```python
def setup_environment():
    """Environment setup validation pattern"""
    if not os.getenv("REQUIRED_VAR"):
        print("❌ REQUIRED_VAR environment variable not set")
        return False
    return True
```

## Security Best Practices
- Never commit `.env` files to version control
- Use different tokens for development and production
- Rotate API keys regularly
- Validate token permissions before operations