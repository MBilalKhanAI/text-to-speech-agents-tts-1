from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai = AsyncOpenAI()

# Sample text for TTS conversion
text = """In the depths of the ancient forest, where sunlight barely penetrated the canopy above, 
a mysterious light flickered between the gnarled trunks. It moved with purpose, as if guided by an unseen hand.

The villagers spoke of it in hushed tones, calling it the "Forest's Heart." Some said it was a lost soul, 
others believed it to be a guardian spirit. But no one had ever dared to follow it deep into the woods.

Until now."""

async def main() -> None:
    # Create speech using GPT-4 TTS model with streaming response
    speech_file_path = "gpt4_output.mp3"
    
    # Using the streaming response method for better performance
    async with openai.audio.speech.with_streaming_response.create(
        model="tts-1-hd",  # Using the HD model for higher quality
        voice="shimmer",   # Using a different voice
        input=text,
        response_format="mp3",
        speed=0.9  # Slightly slower for dramatic effect
    ) as response:
        # Save the audio file
        with open(speech_file_path, "wb") as file:
            async for chunk in response.iter_bytes():
                file.write(chunk)
    
    print(f"Audio has been saved to {speech_file_path}")

if __name__ == "__main__":
    asyncio.run(main()) 