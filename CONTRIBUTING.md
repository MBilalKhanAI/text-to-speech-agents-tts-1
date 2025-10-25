# Contributing to TTS Agents

Thank you for your interest in contributing to TTS Agents! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/tts-agents.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Add tests for your changes
6. Run the test suite: `pytest tests/ -v`
7. Commit your changes: `git commit -m 'Add amazing feature'`
8. Push to your fork: `git push origin feature/amazing-feature`
9. Open a Pull Request

## 📋 Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- OpenAI API key (for testing)

### Installation

```bash
# Clone the repository
git clone https://github.com/muhammadbilalkhan/tts-agents.git
cd tts-agents

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/tts_agents --cov-report=html

# Run specific test file
pytest tests/test_core.py -v

# Run specific test
pytest tests/test_core.py::TestTTSAgent::test_initialization -v
```

### Writing Tests

- Write tests for all new functionality
- Aim for 95%+ test coverage
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies (OpenAI API)

Example:

```python
@pytest.mark.asyncio
async def test_generate_speech_success(self):
    """Test successful speech generation."""
    # Mock OpenAI client
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.iter_bytes.return_value = [b"fake_audio_data"]
    mock_client.audio.speech.create.return_value = mock_response
    
    with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
        agent = TTSAgent()
        agent._client = mock_client
        
        response = await agent.generate_speech(text="Hello, world!")
        
        assert response.success is True
        assert response.audio_data == b"fake_audio_data"
```

## 📝 Code Style

### Formatting

We use Black for code formatting and Ruff for linting:

```bash
# Format code
black src/ tests/

# Check linting
ruff check src/ tests/

# Fix auto-fixable issues
ruff check src/ tests/ --fix
```

### Type Hints

Use type hints for all function parameters and return values:

```python
from typing import Optional, Union, List
from pathlib import Path

async def generate_speech(
    self,
    text: str,
    voice: Optional[Voice] = None,
    output_path: Optional[Union[str, Path]] = None
) -> TTSResponse:
    """Generate speech from text."""
    pass
```

### Documentation

- Use docstrings for all public functions and classes
- Follow Google-style docstrings
- Include type information in docstrings
- Add examples for complex functions

Example:

```python
async def generate_speech(
    self,
    text: str,
    voice: Optional[Voice] = None,
    output_path: Optional[Union[str, Path]] = None
) -> TTSResponse:
    """
    Generate speech from text.
    
    Args:
        text: Text to convert to speech
        voice: Voice to use (defaults to config default)
        output_path: Path to save audio file (optional)
        
    Returns:
        TTSResponse with audio data and metadata
        
    Raises:
        TTSValidationError: If input validation fails
        TTSAPIError: If API request fails
        
    Example:
        >>> async with TTSAgent() as agent:
        ...     response = await agent.generate_speech("Hello, world!")
        ...     print(response.success)
        True
    """
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: Python version, OS, library versions
6. **Code Sample**: Minimal code that reproduces the issue
7. **Error Messages**: Full error messages and stack traces

### Bug Report Template

```markdown
## Bug Description
Brief description of the bug.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- Python version: 3.11.0
- OS: Windows 10
- TTS Agents version: 1.0.0

## Code Sample
```python
# Minimal code that reproduces the issue
```

## Error Messages
```
Full error message here
```
```

## ✨ Feature Requests

When requesting features, please include:

1. **Description**: Clear description of the feature
2. **Use Case**: Why this feature would be useful
3. **Proposed Solution**: How you think it should work
4. **Alternatives**: Other solutions you've considered
5. **Additional Context**: Any other relevant information

### Feature Request Template

```markdown
## Feature Description
Brief description of the feature.

## Use Case
Why this feature would be useful.

## Proposed Solution
How you think it should work.

## Alternatives
Other solutions you've considered.

## Additional Context
Any other relevant information.
```

## 📚 Documentation

### Updating Documentation

- Update docstrings when changing function signatures
- Update README.md for new features
- Add examples to the examples/ directory
- Update API documentation

### Documentation Structure

```
docs/
├── README.md          # Main documentation
├── api/              # API reference
├── examples/         # Code examples
└── guides/           # User guides
```

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes**: Run the full test suite
2. **Check code style**: Run Black and Ruff
3. **Update documentation**: Update relevant docs
4. **Add tests**: Add tests for new functionality
5. **Update CHANGELOG**: Add entry for your changes

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] All existing tests still pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: Maintainers review the code
3. **Testing**: Manual testing if needed
4. **Approval**: At least one maintainer approval required
5. **Merge**: Changes merged to main branch

## 🏷️ Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Release notes prepared
- [ ] PyPI package built and tested

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect different opinions and approaches

### Communication

- Use clear, concise language
- Be specific in bug reports and feature requests
- Provide context and examples
- Be patient with responses

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: muhammadbilalkhan@ai.com
- **LinkedIn**: [Muhammad Bilal Khan](https://linkedin.com/in/muhammadbilalkhan)

## 🙏 Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes
- Project documentation
- Social media acknowledgments

Thank you for contributing to TTS Agents! 🎉
