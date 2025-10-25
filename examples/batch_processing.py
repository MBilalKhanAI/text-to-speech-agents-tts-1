"""
Batch processing example for TTS Agents.

This example demonstrates how to process multiple texts efficiently
using the batch processing capabilities.
"""

import asyncio
from pathlib import Path
from tts_agents import TTSAgent, TTSConfig, Voice, AudioFormat, TTSModel, TTSRequest
from tts_agents.batch import BatchProcessor


async def basic_batch_example():
    """Basic batch processing example."""
    print("📦 TTS Agents - Batch Processing Example")
    print("=" * 50)
    
    # Sample texts for batch processing
    texts = [
        "Welcome to our AI-powered text-to-speech service.",
        "This is the second audio file in our batch processing demo.",
        "The third audio demonstrates the efficiency of batch operations.",
        "Finally, this is the fourth and last audio in our batch."
    ]
    
    # Create TTS requests
    requests = [
        TTSRequest(
            text=text,
            voice=Voice.ALLOY,
            model=TTSModel.TTS_1,
            format=AudioFormat.MP3,
            speed=1.0
        )
        for text in texts
    ]
    
    # Initialize TTS Agent and Batch Processor
    async with TTSAgent() as agent:
        batch_processor = BatchProcessor(agent, max_concurrent=3)
        
        print(f"🔄 Processing {len(requests)} texts in batch...")
        
        # Process batch
        result = await batch_processor.process_batch(
            requests=requests,
            output_directory=Path("examples/batch_output"),
            retry_attempts=2
        )
        
        # Display results
        print(f"\n📊 Batch Processing Results:")
        print(f"   Total requests: {result.total_requests}")
        print(f"   Successful: {result.successful}")
        print(f"   Failed: {result.failed}")
        print(f"   Processing time: {result.processing_time:.2f} seconds")
        print(f"   Output directory: examples/batch_output")
        
        if result.errors:
            print(f"\n❌ Errors encountered:")
            for error in result.errors:
                print(f"   • {error}")


async def advanced_batch_example():
    """Advanced batch processing with different voices."""
    print("\n🎭 Advanced Batch Processing with Multiple Voices")
    print("=" * 50)
    
    # Create diverse batch requests
    requests = [
        TTSRequest(text="This is spoken in a neutral voice.", voice=Voice.ALLOY),
        TTSRequest(text="This is spoken in a clear, articulate voice.", voice=Voice.ECHO),
        TTSRequest(text="This is spoken in a warm, storytelling voice.", voice=Voice.FABLE),
        TTSRequest(text="This is spoken in a deep, authoritative voice.", voice=Voice.ONYX),
        TTSRequest(text="This is spoken in a bright, energetic voice.", voice=Voice.NOVA),
        TTSRequest(text="This is spoken in a soft, gentle voice.", voice=Voice.SHIMMER),
    ]
    
    # Custom configuration for batch processing
    config = TTSConfig(
        default_model=TTSModel.TTS_1_HD,  # Use HD model for better quality
        rate_limit_delay=0.5  # Faster processing
    )
    
    async with TTSAgent(config) as agent:
        batch_processor = BatchProcessor(agent, max_concurrent=4)
        
        print(f"🎨 Processing {len(requests)} texts with different voices...")
        
        # Process batch
        result = await batch_processor.process_batch(
            requests=requests,
            output_directory=Path("examples/voice_demo"),
            retry_attempts=3
        )
        
        # Display detailed results
        print(f"\n📊 Voice Demo Results:")
        print(f"   Total requests: {result.total_requests}")
        print(f"   Successful: {result.successful}")
        print(f"   Failed: {result.failed}")
        print(f"   Processing time: {result.processing_time:.2f} seconds")
        
        # Show individual results
        print(f"\n📁 Generated files:")
        for i, response in enumerate(result.results):
            if response.success and response.file_path:
                print(f"   {i+1}. {response.file_path.name} - {response.metadata.get('voice', 'unknown')} voice")
            else:
                print(f"   {i+1}. Failed - {response.error}")


async def file_batch_example():
    """Batch processing from text file."""
    print("\n📄 Batch Processing from Text File")
    print("=" * 50)
    
    # Create sample text file
    sample_texts = [
        "The first paragraph of our document.",
        "The second paragraph continues the story.",
        "The third paragraph concludes our example.",
    ]
    
    text_file = Path("examples/sample_texts.txt")
    text_file.parent.mkdir(exist_ok=True)
    
    with open(text_file, 'w', encoding='utf-8') as f:
        for text in sample_texts:
            f.write(text + '\n')
    
    print(f"📝 Created sample text file: {text_file}")
    
    # Read texts from file
    with open(text_file, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f if line.strip()]
    
    # Create requests
    requests = [
        TTSRequest(
            text=text,
            voice=Voice.FABLE,  # Use storytelling voice
            model=TTSModel.TTS_1_HD,
            format=AudioFormat.MP3,
            speed=0.9  # Slightly slower for better comprehension
        )
        for text in texts
    ]
    
    # Process batch
    async with TTSAgent() as agent:
        batch_processor = BatchProcessor(agent, max_concurrent=2)
        
        print(f"🔄 Processing {len(requests)} texts from file...")
        
        result = await batch_processor.process_batch(
            requests=requests,
            output_directory=Path("examples/file_batch_output"),
            retry_attempts=2
        )
        
        print(f"\n📊 File Batch Results:")
        print(f"   Total requests: {result.total_requests}")
        print(f"   Successful: {result.successful}")
        print(f"   Failed: {result.failed}")
        print(f"   Processing time: {result.processing_time:.2f} seconds")
        
        # Clean up sample file
        text_file.unlink()
        print(f"🗑️  Cleaned up sample file: {text_file}")


async def performance_comparison():
    """Compare performance of different batch configurations."""
    print("\n⚡ Performance Comparison")
    print("=" * 50)
    
    # Create test requests
    test_texts = [f"This is test text number {i+1}." for i in range(10)]
    requests = [TTSRequest(text=text) for text in test_texts]
    
    # Test different concurrency levels
    concurrency_levels = [1, 3, 5]
    
    async with TTSAgent() as agent:
        for concurrency in concurrency_levels:
            print(f"\n🔄 Testing with {concurrency} concurrent requests...")
            
            batch_processor = BatchProcessor(agent, max_concurrent=concurrency)
            
            result = await batch_processor.process_batch(
                requests=requests,
                output_directory=Path(f"examples/performance_test_{concurrency}"),
                retry_attempts=1
            )
            
            print(f"   Results: {result.successful}/{result.total_requests} successful")
            print(f"   Time: {result.processing_time:.2f} seconds")
            print(f"   Rate: {result.total_requests/result.processing_time:.2f} requests/second")


if __name__ == "__main__":
    # Create examples directory
    Path("examples").mkdir(exist_ok=True)
    
    # Run examples
    asyncio.run(basic_batch_example())
    asyncio.run(advanced_batch_example())
    asyncio.run(file_batch_example())
    asyncio.run(performance_comparison())
    
    print("\n🎉 All batch processing examples completed!")
    print("📁 Check the 'examples' directory for generated audio files.")
