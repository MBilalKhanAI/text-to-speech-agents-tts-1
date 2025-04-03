from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai = AsyncOpenAI()

input = """The night was heavy with secrets… The air, thick with the scent of rain, carried whispers that did not belong to the wind.

She stepped cautiously into the alley, her breath slow, measured—listening. Footsteps, just behind. A shadow flickered, gone before she could turn.

The note in her pocket burned against her palm. Meet me at midnight. Alone. But she wasn't alone. Not anymore.

A sudden creak. A breath too close. And then—darkness.

Some mysteries are meant to be solved. Others… never should be found."""

instructions = """Voice: Deep, hushed, and enigmatic, with a slow, deliberate cadence that draws the listener in.

Phrasing: Sentences are short and rhythmic, building tension with pauses and carefully placed suspense.

Punctuation: Dramatic pauses, ellipses, and abrupt stops enhance the feeling of unease and anticipation.

Tone: Dark, ominous, and foreboding, evoking a sense of mystery and the unknown."""

async def main() -> None:
    # Create speech and save to file
    speech_file_path = "output.mp3"
    response = await openai.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=input,
        response_format="mp3"
    )
    
    # Save the audio file
    response.stream_to_file(speech_file_path)
    print(f"Audio has been saved to {speech_file_path}")

if __name__ == "__main__":
    asyncio.run(main()) 