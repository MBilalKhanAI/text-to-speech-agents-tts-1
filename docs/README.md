# TTS Agents Documentation

Welcome to the comprehensive documentation for TTS Agents - a professional, production-ready Python library for text-to-speech conversion using OpenAI's TTS-1 model.

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Performance](#performance)
- [Contributing](#contributing)

## Quick Start

Get started with TTS Agents in just a few lines of code:

```python
import asyncio
from tts_agents import TTSAgent, Voice, AudioFormat

async def main():
    async with TTSAgent() as agent:
        response = await agent.generate_speech(
            text="Hello, world!",
            voice=Voice.ALLOY,
            output_path="output.mp3"
        )
        print(f"Audio saved to: {response.file_path}")

asyncio.run(main())
```

## Installation

### From PyPI (Recommended)

```bash
pip install tts-agents
```

### From Source

```bash
git clone https://github.com/muhammadbilalkhan/tts-agents.git
cd tts-agents
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/muhammadbilalkhan/tts-agents.git
cd tts-agents
pip install -e ".[dev]"
```

## Basic Usage

### Simple Text-to-Speech

```python
from tts_agents import TTSAgent, Voice, AudioFormat, TTSModel

async with TTSAgent() as agent:
    response = await agent.generate_speech(
        text="Your text here",
        voice=Voice.ALLOY,
        model=TTSModel.TTS_1,
        format=AudioFormat.MP3,
        speed=1.0,
        output_path="speech.mp3"
    )
```

### Configuration

```python
from tts_agents import TTSAgent, TTSConfig

config = TTSConfig(
    api_key="your-api-key",
    timeout=60,
    max_retries=3,
    default_voice=Voice.ECHO
)

async with TTSAgent(config) as agent:
    # Use agent with custom configuration
    pass
```

## Advanced Features

### Batch Processing

Process multiple texts efficiently:

```python
from tts_agents import TTSAgent, TTSRequest, Voice
from tts_agents.batch import BatchProcessor

async with TTSAgent() as agent:
    batch_processor = BatchProcessor(agent, max_concurrent=5)
    
    requests = [
        TTSRequest(text="First text", voice=Voice.ALLOY),
        TTSRequest(text="Second text", voice=Voice.ECHO),
        TTSRequest(text="Third text", voice=Voice.FABLE),
    ]
    
    result = await batch_processor.process_batch(
        requests=requests,
        output_directory="./output"
    )
    
    print(f"Processed {result.successful}/{result.total_requests} requests")
```

### Streaming TTS

For real-time processing:

```python
from tts_agents.streaming import StreamingTTS

async with TTSAgent() as agent:
    streaming_tts = StreamingTTS(agent)
    
    # Stream to file
    output_path = await streaming_tts.stream_speech_to_file(
        text="Long text here...",
        output_path="streaming_output.mp3"
    )
    
    # Or process chunks
    async for chunk in streaming_tts.stream_speech(text="Text here"):
        # Process each chunk as it arrives
        process_chunk(chunk)
```

## API Reference

### TTSAgent

The main class for text-to-speech conversion.

#### Methods

- `generate_speech(text, voice, model, format, speed, output_path)` - Generate speech from text
- `generate_speech_streaming(text, voice, model, format, speed, output_path)` - Generate speech with streaming
- `get_available_voices()` - Get list of available voices
- `get_available_models()` - Get list of available models
- `get_available_formats()` - Get list of available audio formats

### BatchProcessor

Efficient batch processing of multiple TTS requests.

#### Methods

- `process_batch(requests, output_directory, retry_attempts)` - Process multiple requests
- `process_batch_from_config(batch_request)` - Process from BatchTTSRequest

### StreamingTTS

Real-time streaming text-to-speech processing.

#### Methods

- `stream_speech(text, voice, model, format, speed, output_path, chunk_callback)` - Stream speech generation
- `stream_speech_to_file(text, output_path, voice, model, format, speed)` - Stream directly to file
- `stream_speech_with_progress(text, voice, model, format, speed, progress_callback)` - Stream with progress tracking

## Examples

### Command Line Interface

```bash
# Generate speech from text
tts-agents generate "Hello, world!" --voice alloy --output hello.mp3

# Generate from file
tts-agents file input.txt --voice echo --output speech.mp3

# Batch processing
tts-agents batch "Text 1" "Text 2" "Text 3" --output-dir ./output

# List available options
tts-agents voices
tts-agents models
tts-agents formats
```

### Python Examples

See the `examples/` directory for comprehensive examples:

- `basic_usage.py` - Basic usage patterns
- `batch_processing.py` - Batch processing examples
- `streaming_example.py` - Streaming TTS examples

## Configuration

### Environment Variables

Set these environment variables for automatic configuration:

```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # Optional
```

### TTSConfig Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | str | None | OpenAI API key |
| `base_url` | str | None | OpenAI API base URL |
| `timeout` | int | 30 | Request timeout in seconds |
| `max_retries` | int | 3 | Maximum retry attempts |
| `rate_limit_delay` | float | 1.0 | Delay between requests |
| `default_voice` | Voice | ALLOY | Default voice |
| `default_model` | TTSModel | TTS_1 | Default model |
| `default_format` | AudioFormat | MP3 | Default format |
| `default_speed` | float | 1.0 | Default speed |

## Error Handling

TTS Agents provides comprehensive error handling with custom exceptions:

```python
from tts_agents.exceptions import TTSAgentError, TTSAPIError, TTSConfigError

try:
    response = await agent.generate_speech(text="Hello")
except TTSAPIError as e:
    print(f"API Error: {e}")
except TTSConfigError as e:
    print(f"Configuration Error: {e}")
except TTSAgentError as e:
    print(f"General Error: {e}")
```

### Exception Types

- `TTSAgentError` - Base exception for all TTS errors
- `TTSConfigError` - Configuration-related errors
- `TTSAPIError` - OpenAI API errors
- `TTSValidationError` - Input validation errors
- `TTSFileError` - File operation errors
- `TTSRateLimitError` - Rate limiting errors

## Performance

### Optimization Tips

1. **Use streaming for long texts** - Better memory efficiency
2. **Batch processing for multiple texts** - More efficient API usage
3. **Adjust concurrency limits** - Balance speed vs rate limits
4. **Use appropriate models** - TTS-1 for speed, TTS-1-HD for quality

### Performance Metrics

Typical performance characteristics:

- **TTS-1**: ~2-3 seconds per 100 words
- **TTS-1-HD**: ~4-6 seconds per 100 words
- **Batch processing**: 3-5x faster than sequential processing
- **Streaming**: 20-30% memory reduction for long texts

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/muhammadbilalkhan/tts-agents.git
cd tts-agents
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest tests/ -v --cov=src/tts_agents
```

### Code Quality

```bash
black src/ tests/
ruff check src/ tests/
mypy src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: muhammadbilalkhan@ai.com
- 🐛 Issues: [GitHub Issues](https://github.com/muhammadbilalkhan/tts-agents/issues)
- 📖 Documentation: [GitHub Pages](https://muhammadbilalkhan.github.io/tts-agents/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
