from openai import AsyncOpenAI
import asyncio
import os
import argparse
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai = AsyncOpenAI()

# Available voices for TTS-1
AVAILABLE_VOICES = [
    "alloy", "echo", "fable", "onyx", "nova", "shimmer"
]

async def generate_speech(text, voice, output_file, speed=1.0):
    """Generate speech using OpenAI TTS-1 model"""
    try:
        print(f"Generating speech with voice '{voice}'...")
        
        response = await openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            response_format="mp3",
            speed=speed
        )
        
        # Save the audio file
        response.stream_to_file(output_file)
        print(f"✅ Speech generated successfully and saved to: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating speech: {str(e)}")
        return False

async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="OpenAI TTS-1 Text-to-Speech CLI")
    
    # Add arguments
    parser.add_argument("--text", "-t", type=str, help="Text to convert to speech")
    parser.add_argument("--file", "-f", type=str, help="File containing text to convert")
    parser.add_argument("--voice", "-v", type=str, default="alloy", 
                        help=f"Voice to use (available: {', '.join(AVAILABLE_VOICES)})")
    parser.add_argument("--output", "-o", type=str, default="output.mp3", 
                        help="Output file path (default: output.mp3)")
    parser.add_argument("--speed", "-s", type=float, default=1.0, 
                        help="Speech speed (0.25 to 4.0, default: 1.0)")
    parser.add_argument("--list-voices", action="store_true", 
                        help="List available voices and exit")
    
    # Parse arguments
    args = parser.parse_args()
    
    # List voices if requested
    if args.list_voices:
        print("Available voices:")
        for voice in AVAILABLE_VOICES:
            print(f"  - {voice}")
        return
    
    # Get text from arguments or file
    text = args.text
    if not text and args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
            return
    
    # Check if we have text to convert
    if not text:
        print("❌ No text provided. Use --text or --file to specify text to convert.")
        parser.print_help()
        return
    
    # Validate voice
    if args.voice not in AVAILABLE_VOICES:
        print(f"❌ Invalid voice: {args.voice}")
        print(f"Available voices: {', '.join(AVAILABLE_VOICES)}")
        return
    
    # Validate speed
    if args.speed < 0.25 or args.speed > 4.0:
        print("❌ Speed must be between 0.25 and 4.0")
        return
    
    # Generate speech
    await generate_speech(text, args.voice, args.output, args.speed)

if __name__ == "__main__":
    asyncio.run(main()) 