"""
Streaming TTS example for TTS Agents.

This example demonstrates real-time streaming capabilities for
text-to-speech conversion with chunked processing.
"""

import asyncio
from pathlib import Path
from tts_agents import TTSAgent, Voice, AudioFormat, TTSModel
from tts_agents.streaming import StreamingTTS


async def basic_streaming_example():
    """Basic streaming TTS example."""
    print("🌊 TTS Agents - Streaming Example")
    print("=" * 50)
    
    async with TTSAgent() as agent:
        streaming_tts = StreamingTTS(agent)
        
        # Long text for streaming demonstration
        long_text = """
        This is a demonstration of streaming text-to-speech conversion.
        The streaming approach allows for real-time processing of audio data,
        which is particularly useful for long texts or when you need to start
        playing audio before the entire conversion is complete.
        
        Streaming provides better performance and memory efficiency,
        especially for large documents or real-time applications.
        """
        
        print("🔄 Streaming speech generation...")
        
        # Stream to file
        output_path = await streaming_tts.stream_speech_to_file(
            text=long_text,
            output_path="examples/streaming_output.mp3",
            voice=Voice.ECHO,
            model=TTSModel.TTS_1_HD,
            format=AudioFormat.MP3,
            speed=1.0
        )
        
        print(f"✅ Streaming completed!")
        print(f"📁 Output file: {output_path}")


async def chunk_processing_example():
    """Example with chunk processing callback."""
    print("\n🔧 Chunk Processing Example")
    print("=" * 50)
    
    async with TTSAgent() as agent:
        streaming_tts = StreamingTTS(agent, chunk_size=512)
        
        # Track chunks
        chunks_received = 0
        total_bytes = 0
        
        def chunk_callback(chunk: bytes):
            nonlocal chunks_received, total_bytes
            chunks_received += 1
            total_bytes += len(chunk)
            print(f"📦 Received chunk {chunks_received}: {len(chunk)} bytes")
        
        text = "This example demonstrates chunk-by-chunk processing of audio data."
        
        print("🔄 Processing with chunk callback...")
        
        # Collect all chunks
        audio_chunks = []
        async for chunk in streaming_tts.stream_speech(
            text=text,
            voice=Voice.SHIMMER,
            chunk_callback=chunk_callback
        ):
            audio_chunks.append(chunk)
        
        # Save complete audio
        complete_audio = b"".join(audio_chunks)
        output_path = Path("examples/chunk_processing_output.mp3")
        output_path.write_bytes(complete_audio)
        
        print(f"✅ Chunk processing completed!")
        print(f"📊 Total chunks: {chunks_received}")
        print(f"📊 Total bytes: {total_bytes}")
        print(f"📁 Output file: {output_path}")


async def progress_tracking_example():
    """Example with progress tracking."""
    print("\n📊 Progress Tracking Example")
    print("=" * 50)
    
    async with TTSAgent() as agent:
        streaming_tts = StreamingTTS(agent)
        
        # Long text for progress demonstration
        long_text = """
        Progress tracking in streaming TTS allows you to monitor the conversion
        process in real-time. This is particularly useful for user interfaces
        where you want to show progress bars or status updates.
        
        The progress callback receives the current number of bytes received
        and an estimated total, allowing you to calculate completion percentage.
        """
        
        def progress_callback(bytes_received: int, total_estimated: int):
            if total_estimated > 0:
                percentage = (bytes_received / total_estimated) * 100
                print(f"📈 Progress: {bytes_received}/{total_estimated} bytes ({percentage:.1f}%)")
            else:
                print(f"📈 Progress: {bytes_received} bytes received")
        
        print("🔄 Processing with progress tracking...")
        
        # Generate speech with progress tracking
        audio_data = await streaming_tts.stream_speech_with_progress(
            text=long_text,
            voice=Voice.FABLE,
            model=TTSModel.TTS_1_HD,
            progress_callback=progress_callback
        )
        
        # Save audio
        output_path = Path("examples/progress_tracking_output.mp3")
        output_path.write_bytes(audio_data)
        
        print(f"✅ Progress tracking completed!")
        print(f"📊 Final audio size: {len(audio_data)} bytes")
        print(f"📁 Output file: {output_path}")


async def real_time_processing_example():
    """Example simulating real-time processing."""
    print("\n⏱️  Real-time Processing Example")
    print("=" * 50)
    
    async with TTSAgent() as agent:
        streaming_tts = StreamingTTS(agent, chunk_size=1024)
        
        # Simulate real-time text input (like a live transcription)
        text_segments = [
            "Welcome to our real-time text-to-speech demonstration.",
            "This simulates how the system would work with live text input.",
            "Each segment is processed as it becomes available.",
            "This allows for immediate audio output without waiting for complete text."
        ]
        
        print("🔄 Processing text segments in real-time...")
        
        # Process each segment
        for i, segment in enumerate(text_segments):
            print(f"📝 Processing segment {i+1}: {segment[:50]}...")
            
            # Stream this segment
            audio_chunks = []
            async for chunk in streaming_tts.stream_speech(
                text=segment,
                voice=Voice.NOVA,
                model=TTSModel.TTS_1
            ):
                audio_chunks.append(chunk)
                # In a real application, you would play the chunk immediately
            
            # Save segment audio
            segment_audio = b"".join(audio_chunks)
            segment_path = Path(f"examples/realtime_segment_{i+1}.mp3")
            segment_path.write_bytes(segment_audio)
            
            print(f"✅ Segment {i+1} completed: {len(segment_audio)} bytes")
        
        print(f"✅ Real-time processing completed!")
        print(f"📁 Generated {len(text_segments)} segment files")


async def performance_comparison():
    """Compare streaming vs non-streaming performance."""
    print("\n⚡ Performance Comparison: Streaming vs Non-Streaming")
    print("=" * 50)
    
    long_text = """
    This is a performance comparison between streaming and non-streaming
    text-to-speech conversion. Streaming typically provides better memory
    efficiency and can start producing audio sooner, while non-streaming
    may be simpler for some use cases but requires more memory for large texts.
    
    The choice between streaming and non-streaming depends on your specific
    requirements, such as memory constraints, latency requirements, and
    the complexity of your application.
    """
    
    async with TTSAgent() as agent:
        streaming_tts = StreamingTTS(agent)
        
        # Test streaming approach
        print("🔄 Testing streaming approach...")
        start_time = asyncio.get_event_loop().time()
        
        streaming_audio = await streaming_tts.stream_speech_with_progress(
            text=long_text,
            voice=Voice.ALLOY,
            model=TTSModel.TTS_1_HD
        )
        
        streaming_time = asyncio.get_event_loop().time() - start_time
        
        # Test non-streaming approach
        print("🔄 Testing non-streaming approach...")
        start_time = asyncio.get_event_loop().time()
        
        response = await agent.generate_speech(
            text=long_text,
            voice=Voice.ALLOY,
            model=TTSModel.TTS_1_HD
        )
        
        non_streaming_time = asyncio.get_event_loop().time() - start_time
        
        # Compare results
        print(f"\n📊 Performance Comparison:")
        print(f"   Streaming time: {streaming_time:.2f} seconds")
        print(f"   Non-streaming time: {non_streaming_time:.2f} seconds")
        print(f"   Streaming audio size: {len(streaming_audio)} bytes")
        print(f"   Non-streaming audio size: {response.file_size} bytes")
        
        # Save both for comparison
        Path("examples/streaming_performance.mp3").write_bytes(streaming_audio)
        if response.success and response.audio_data:
            Path("examples/non_streaming_performance.mp3").write_bytes(response.audio_data)
        
        print(f"📁 Both audio files saved for comparison")


if __name__ == "__main__":
    # Create examples directory
    Path("examples").mkdir(exist_ok=True)
    
    # Run examples
    asyncio.run(basic_streaming_example())
    asyncio.run(chunk_processing_example())
    asyncio.run(progress_tracking_example())
    asyncio.run(real_time_processing_example())
    asyncio.run(performance_comparison())
    
    print("\n🎉 All streaming examples completed!")
    print("📁 Check the 'examples' directory for generated audio files.")
