# User Experience Guidelines

## Command Line Interface Design

### User-Friendly Patterns
- **Clear Progress Indicators**: Use emoji and descriptive messages (🤖, 📝, ✅, ❌)
- **Helpful Error Messages**: Specific guidance on how to fix issues
- **Flexible Input Methods**: Support argument, file, and interactive input
- **Graceful Degradation**: Allow generation-only or publish-only workflows

### Input Method Support
1. **Argument Input**: Direct topic specification with multi-line support
2. **File Input**: Read detailed topics from external files
3. **Interactive Input**: Prompt-based input with clear instructions
4. **Fallback Behavior**: Auto-switch to interactive when no topic provided

### Feedback and Status Updates
```python
# Status message patterns
print("🔧 環境設定を確認中...")
print("✅ 環境設定OK")
print("📝 記事生成中: {topic}")
print("🤖 使用モデル: {model}")
print("✅ 記事生成完了!")
print("❌ エラー: {error_message}")
```

## Workflow Flexibility

### Generation Modes
- **Full Pipeline**: Generate and publish in one command
- **Generate Only**: Create article without publishing (`--generate-only`)
- **Publish Only**: Publish existing JSON file (`--publish-only`)
- **Interactive Mode**: Step-by-step guided process

### Configuration Options
- **Template Selection**: Easy template switching with descriptions
- **Model Selection**: Clear model options with cost/quality trade-offs
- **Audience Targeting**: Customizable target audience specification
- **Length Control**: Flexible article length configuration

## Error Handling and Recovery

### User-Friendly Error Messages
- Explain what went wrong in plain language
- Provide specific steps to resolve the issue
- Include relevant file paths and configuration details
- Offer alternative approaches when possible

### Recovery Strategies
- **Environment Issues**: Clear setup instructions
- **API Failures**: Retry suggestions and troubleshooting steps
- **File Problems**: Path validation and permission guidance
- **Configuration Errors**: Sample configuration examples

## Documentation and Help

### Built-in Help System
- Comprehensive argument descriptions
- Usage examples for common scenarios
- Template explanations with use cases
- Model selection guidance

### Progressive Disclosure
- Basic usage for quick starts
- Advanced options for power users
- Detailed examples in separate documentation
- Troubleshooting guides for common issues