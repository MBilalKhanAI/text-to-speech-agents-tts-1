# Text-to-Speech Model

This repository contains implementations of text-to-speech conversion using the OpenAI TTS-1 model. It provides various approaches to convert text to speech, from simple implementations to batch processing and command-line interfaces.

## Features

- Multiple implementations of OpenAI TTS-1 model
- Batch processing for multiple text inputs
- Command-line interface for easy text-to-speech conversion
- Support for different voices and speech speeds
- Sample audio files generated from various texts

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Available Implementations

### 1. Basic OpenAI TTS (text_to_speech.py)

A simple implementation that saves the audio to a file.

```bash
python text_to_speech.py
```

### 2. GPT-4 TTS with Streaming (gpt4_tts.py)

Uses the OpenAI TTS API with the HD model and streaming response for better performance.

```bash
python gpt4_tts.py
```

### 3. Batch TTS Processing (tts1_batch.py)

Processes multiple text inputs in parallel, generating separate audio files for each input.

```bash
python tts1_batch.py
```

### 4. Command-Line Interface (tts1_cli.py)

Provides a command-line interface for the TTS-1 model, allowing you to specify text, voice, and other parameters.

```bash
# List available voices
python tts1_cli.py --list-voices

# Convert text to speech with default settings
python tts1_cli.py --text "Hello, world!"

# Convert text from a file with custom voice and speed
python tts1_cli.py --file input.txt --voice shimmer --speed 0.9 --output custom_output.mp3
```

## Sample Audio Files

The repository includes sample audio files generated using the different implementations:

- `output.mp3` - Basic TTS implementation
- `gpt4_output.mp3` - GPT-4 TTS with streaming
- `lighthouse_story.mp3`, `desert_oasis.mp3`, `antique_shop.mp3` - Batch processing examples

## Voice Options

The TTS-1 model supports the following voices:
- alloy
- echo
- fable
- onyx
- nova
- shimmer

## License

MIT

## Author

Muhammad Bilal Khan
