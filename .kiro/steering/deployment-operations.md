# Deployment and Operations Guidelines

## Deployment Strategy

### Environment Setup Automation
- **Virtual Environment**: Unified `venv/` at project root
- **Dependency Management**: Single `requirements.txt` for all Python dependencies
- **Elixir Dependencies**: Automatic `mix deps.get` in shell scripts
- **Environment Validation**: Comprehensive setup checks before operations

### Installation Process
```bash
# Standard installation pattern
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Environment configuration
cp python/.env.sample python/.env
# Edit python/.env to add OPENAI_API_KEY
echo "QIITA_ACCESS_TOKEN=your_token" > .env
```

## Operational Monitoring

### Health Checks
- **API Connectivity**: Validate OpenAI and Qiita API access
- **Environment Variables**: Verify all required configuration
- **File Permissions**: Check read/write access for JSON files
- **Dependency Versions**: Ensure compatible package versions

### Logging and Debugging
```python
# Logging pattern for operations
print("🔧 環境設定を確認中...")
print("✅ 環境設定OK")
print(f"🤖 使用モデル: {model}")
print(f"📝 記事生成中: {topic}")
print("✅ 記事生成完了!")
```

## Error Recovery Procedures

### Common Issues and Solutions
1. **Virtual Environment Not Activated**
   - Error: `ModuleNotFoundError`
   - Solution: `source venv/bin/activate`

2. **Missing API Keys**
   - Error: Authentication failures
   - Solution: Verify `.env` file configuration

3. **Elixir Dependencies Missing**
   - Error: Module compilation failures
   - Solution: Run `mix deps.get` in Elixir project

4. **JSON File Corruption**
   - Error: Publishing failures
   - Solution: Regenerate article with `--generate-only`

### Backup and Recovery
- **Generated Articles**: Backup JSON files before publishing
- **Configuration**: Version control `.env.sample` files
- **Dependencies**: Lock file management for reproducible builds

## Performance Optimization

### API Usage Optimization
- **Model Selection**: Use appropriate OpenAI model for use case
- **Rate Limiting**: Respect API limits and implement backoff
- **Caching**: Cache generated articles for republishing
- **Batch Operations**: Group multiple operations when possible

### Resource Management
- **Memory Usage**: Monitor large article generation
- **Network Timeouts**: Configure appropriate timeout values
- **Concurrent Operations**: Limit parallel API calls
- **Cleanup**: Remove temporary files after operations