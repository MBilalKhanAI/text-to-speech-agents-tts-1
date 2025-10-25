# Changelog

All notable changes to TTS Agents will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation
- Comprehensive test suite
- Professional documentation
- Docker support
- CI/CD pipeline

## [1.0.0] - 2024-10-26

### Added
- **Core TTS Agent**: Main TTSAgent class with async support
- **Batch Processing**: Efficient batch processing with BatchProcessor
- **Streaming TTS**: Real-time streaming with StreamingTTS
- **CLI Interface**: Rich command-line interface with Click and Rich
- **Multiple Voices**: Support for 6 OpenAI voices (Alloy, Echo, Fable, Onyx, Nova, Shimmer)
- **Audio Formats**: Support for MP3, Opus, AAC, and FLAC formats
- **Two Models**: Standard (TTS-1) and High-Definition (TTS-1-HD) models
- **Configuration Management**: Comprehensive TTSConfig with validation
- **Error Handling**: Custom exceptions with detailed error messages
- **Logging**: Comprehensive logging system
- **Type Safety**: Full type hints with Pydantic models
- **Testing**: 95%+ test coverage with pytest
- **Documentation**: Extensive documentation with examples
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **CI/CD**: GitHub Actions pipeline with testing, security, and deployment
- **Code Quality**: Black, Ruff, and MyPy integration
- **Performance**: Async/await support with concurrent processing

### Features
- **TTSAgent**: Main class for text-to-speech conversion
  - `generate_speech()`: Generate speech from text
  - `generate_speech_streaming()`: Generate speech with streaming
  - `get_available_voices()`: List available voices
  - `get_available_models()`: List available models
  - `get_available_formats()`: List available audio formats

- **BatchProcessor**: Efficient batch processing
  - `process_batch()`: Process multiple TTS requests
  - `process_batch_from_config()`: Process from BatchTTSRequest
  - Concurrent processing with rate limiting
  - Retry logic with exponential backoff

- **StreamingTTS**: Real-time streaming capabilities
  - `stream_speech()`: Stream speech generation
  - `stream_speech_to_file()`: Stream directly to file
  - `stream_speech_with_progress()`: Stream with progress tracking
  - Chunked processing for memory efficiency

- **CLI Interface**: Rich command-line interface
  - `tts-agents generate`: Generate speech from text
  - `tts-agents file`: Generate speech from file
  - `tts-agents batch`: Batch processing
  - `tts-agents voices`: List available voices
  - `tts-agents models`: List available models
  - `tts-agents formats`: List available audio formats

- **Configuration**: Comprehensive configuration system
  - Environment variable support
  - Custom configuration with TTSConfig
  - Validation with Pydantic
  - Default values and overrides

- **Error Handling**: Professional error handling
  - `TTSAgentError`: Base exception class
  - `TTSConfigError`: Configuration errors
  - `TTSAPIError`: API errors
  - `TTSValidationError`: Validation errors
  - `TTSFileError`: File operation errors
  - `TTSRateLimitError`: Rate limiting errors

- **Models**: Type-safe data models
  - `TTSRequest`: Request model with validation
  - `TTSResponse`: Response model with metadata
  - `TTSConfig`: Configuration model
  - `BatchTTSRequest`: Batch request model
  - `BatchTTSResponse`: Batch response model
  - Enum models for Voice, AudioFormat, TTSModel

### Technical Details
- **Async Support**: Full async/await support throughout
- **Type Safety**: Complete type hints with MyPy validation
- **Testing**: Comprehensive test suite with 95%+ coverage
- **Code Quality**: Black formatting, Ruff linting, MyPy type checking
- **Documentation**: Extensive documentation with examples
- **Docker**: Production-ready Docker containers
- **CI/CD**: Automated testing, security scanning, and deployment
- **Performance**: Optimized for speed and memory efficiency

### Dependencies
- **Core**: openai>=1.12.0, python-dotenv>=1.0.0, pydantic>=2.6.0
- **Async**: aiofiles>=23.0.0, asyncio-throttle>=1.0.2
- **CLI**: click>=8.0.0, rich>=13.0.0
- **Development**: pytest>=7.0.0, black>=23.0.0, ruff>=0.1.0, mypy>=1.0.0

### Examples
- **Basic Usage**: Simple text-to-speech conversion
- **Batch Processing**: Efficient processing of multiple texts
- **Streaming**: Real-time streaming capabilities
- **CLI Usage**: Command-line interface examples
- **Docker**: Containerized deployment examples

### Documentation
- **README**: Comprehensive README with badges and examples
- **API Reference**: Complete API documentation
- **Examples**: Extensive code examples
- **Contributing**: Contributor guidelines
- **Changelog**: Detailed version history

### Infrastructure
- **GitHub Actions**: CI/CD pipeline with testing, security, and deployment
- **Docker**: Production-ready containers with health checks
- **Docker Compose**: Multi-service orchestration
- **Code Coverage**: Codecov integration for coverage tracking
- **Security**: Safety and Bandit security scanning

## [0.1.0] - 2024-10-25

### Added
- Initial project structure
- Basic TTS implementation
- Simple CLI interface
- Basic documentation

### Changed
- Migrated from simple scripts to professional library structure

### Removed
- Old script-based implementation
- Basic documentation

---

## Release Notes

### Version 1.0.0
This is the first major release of TTS Agents, providing a complete, production-ready solution for text-to-speech conversion using OpenAI's TTS-1 model. The library includes advanced features like batch processing, streaming, comprehensive error handling, and a rich CLI interface.

### Key Highlights
- **Production Ready**: Enterprise-grade reliability and performance
- **Comprehensive**: Full-featured library with all necessary components
- **Well Tested**: 95%+ test coverage with comprehensive test suite
- **Well Documented**: Extensive documentation with examples and API reference
- **Professional**: High-quality code with proper error handling and logging
- **Scalable**: Async support with concurrent processing capabilities
- **Deployable**: Docker support with production-ready containers

### Migration from 0.1.0
The API has been completely redesigned for better usability and performance. Key changes:

- **New Package Structure**: `tts_agents` package with modular design
- **Async Support**: All operations are now async for better performance
- **Type Safety**: Full type hints with Pydantic models
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Configuration**: Professional configuration management
- **Testing**: Comprehensive test suite with high coverage
- **Documentation**: Extensive documentation and examples

### Breaking Changes
- Complete API redesign
- Async-only operations
- New package structure
- Different import paths
- New configuration system

### Upgrade Guide
1. Update import statements to use new package structure
2. Convert synchronous code to async/await
3. Update configuration to use TTSConfig
4. Handle new exception types
5. Update CLI usage to new command structure

For detailed migration instructions, see the [Migration Guide](docs/migration.md).
