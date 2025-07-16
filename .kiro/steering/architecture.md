# Architecture Guidelines

## System Architecture

### Multi-Language Integration
- **Python**: Article generation using OpenAI API, integration orchestration
- **Elixir**: Qiita API client, robust publishing system with error handling
- **Shell Scripts**: Deployment automation and dependency management

### Component Separation
- **Generation Layer** (`python/`): OpenAI integration, article templates, content structuring
- **Publishing Layer** (`elixir/`): Qiita API client, validation, publishing workflow
- **Integration Layer** (`generate_and_publish.py`): Orchestrates the entire pipeline

### Data Flow
1. Topic input → Python article generation → JSON storage
2. JSON validation → Elixir publishing → Qiita API
3. Error handling and feedback at each stage

## Design Principles

### Modularity
- Each component has a single responsibility
- Clear interfaces between Python and Elixir components
- Reusable modules for different article templates

### Reliability
- Comprehensive error handling at each layer
- Validation before publishing
- Graceful degradation (generate-only, publish-only modes)

### Flexibility
- Multiple input methods (argument, file, interactive)
- Configurable templates and models
- Environment-specific configurations