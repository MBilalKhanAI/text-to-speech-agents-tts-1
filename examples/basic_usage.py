"""
Basic usage example for TTS Agents.

This example demonstrates the fundamental usage of the TTS Agents library
for text-to-speech conversion.
"""

import asyncio
from tts_agents import TTSAgent, TTSConfig, Voice, AudioFormat, TTSModel


async def main():
    """Basic TTS usage example."""
    print("🎤 TTS Agents - Basic Usage Example")
    print("=" * 50)
    
    # Initialize TTS Agent with default configuration
    async with TTSAgent() as agent:
        # Generate speech from text
        print("📝 Generating speech from text...")
        response = await agent.generate_speech(
            text="Hello, world! This is a demonstration of the TTS Agents library.",
            voice=Voice.ALLOY,
            model=TTSModel.TTS_1,
            format=AudioFormat.MP3,
            speed=1.0,
            output_path="examples/basic_output.mp3"
        )
        
        if response.success:
            print(f"✅ Speech generated successfully!")
            print(f"📁 Output file: {response.file_path}")
            print(f"📊 File size: {response.file_size} bytes")
            print(f"🎵 Voice: {response.metadata['voice']}")
            print(f"🤖 Model: {response.metadata['model']}")
        else:
            print(f"❌ Speech generation failed: {response.error}")


async def advanced_example():
    """Advanced usage example with custom configuration."""
    print("\n🚀 Advanced Usage Example")
    print("=" * 50)
    
    # Create custom configuration
    config = TTSConfig(
        api_key="your-api-key-here",  # Replace with your actual API key
        timeout=60,
        max_retries=5,
        rate_limit_delay=1.5,
        default_voice=Voice.ECHO,
        default_model=TTSModel.TTS_1_HD,
        default_format=AudioFormat.MP3,
        default_speed=1.2
    )
    
    async with TTSAgent(config) as agent:
        # Generate high-quality speech
        print("🎯 Generating high-quality speech...")
        response = await agent.generate_speech(
            text="This is a high-quality text-to-speech demonstration using the HD model.",
            output_path="examples/advanced_output.mp3"
        )
        
        if response.success:
            print(f"✅ High-quality speech generated!")
            print(f"📁 Output file: {response.file_path}")
            print(f"📊 File size: {response.file_size} bytes")
        else:
            print(f"❌ Speech generation failed: {response.error}")


async def streaming_example():
    """Streaming TTS example."""
    print("\n🌊 Streaming TTS Example")
    print("=" * 50)
    
    from tts_agents.streaming import StreamingTTS
    
    async with TTSAgent() as agent:
        streaming_tts = StreamingTTS(agent)
        
        print("🔄 Generating speech with streaming...")
        response = await streaming_tts.stream_speech_to_file(
            text="This is a streaming text-to-speech demonstration for better performance.",
            output_path="examples/streaming_output.mp3",
            voice=Voice.SHIMMER,
            model=TTSModel.TTS_1_HD
        )
        
        print(f"✅ Streaming speech completed!")
        print(f"📁 Output file: {response}")


if __name__ == "__main__":
    # Run basic example
    asyncio.run(main())
    
    # Run advanced example
    asyncio.run(advanced_example())
    
    # Run streaming example
    asyncio.run(streaming_example())
    
    print("\n🎉 All examples completed successfully!")
    print("📁 Check the 'examples' directory for generated audio files.")
