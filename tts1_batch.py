from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai = AsyncOpenAI()

# Sample texts for batch TTS conversion
texts = [
    {
        "id": "story1",
        "text": """The old lighthouse stood sentinel on the rocky cliff, its beam cutting through the fog like a sword of light. 
        For generations, it had guided ships safely to harbor, its steady rhythm a comfort to sailors far from home.""",
        "voice": "alloy",
        "output_file": "lighthouse_story.mp3"
    },
    {
        "id": "story2",
        "text": """In the heart of the desert, where sand dunes stretched to the horizon, 
        a small oasis offered respite to weary travelers. Palm trees swayed gently in the breeze, 
        their leaves whispering ancient secrets to those who would listen.""",
        "voice": "echo",
        "output_file": "desert_oasis.mp3"
    },
    {
        "id": "story3",
        "text": """The antique shop was a treasure trove of forgotten memories. 
        Each item on the dusty shelves held a story, waiting to be discovered by the right person. 
        The bell above the door chimed softly as another seeker entered, perhaps to find their own piece of history.""",
        "voice": "fable",
        "output_file": "antique_shop.mp3"
    }
]

async def generate_speech(text_item):
    """Generate speech for a single text item"""
    try:
        response = await openai.audio.speech.create(
            model="tts-1",
            voice=text_item["voice"],
            input=text_item["text"],
            response_format="mp3"
        )
        
        # Save the audio file
        response.stream_to_file(text_item["output_file"])
        print(f"✅ Generated {text_item['id']}: {text_item['output_file']}")
        return True
    except Exception as e:
        print(f"❌ Error generating {text_item['id']}: {str(e)}")
        return False

async def process_batch():
    """Process all texts in the batch"""
    print("Starting batch TTS processing...")
    
    # Create tasks for all texts
    tasks = [generate_speech(text_item) for text_item in texts]
    
    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    # Count successes
    success_count = sum(1 for result in results if result)
    
    print(f"\nBatch processing complete: {success_count}/{len(texts)} files generated successfully")

async def main():
    await process_batch()

if __name__ == "__main__":
    asyncio.run(main()) 