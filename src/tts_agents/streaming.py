"""
Streaming TTS implementation.

This module provides advanced streaming capabilities for real-time
text-to-speech conversion with chunked processing and live audio output.
"""

import asyncio
import logging
from typing import AsyncIterator, Optional, Union, Callable, Any
from pathlib import Path
import aiofiles

from .core import TTSAgent
from .models import TTSRequest, Voice, AudioFormat, TTSModel
from .exceptions import TTSAgentError, TTSAPIError


class StreamingTTS:
    """
    Streaming TTS processor for real-time audio generation.
    
    Provides chunked processing and streaming capabilities for
    real-time text-to-speech conversion with live audio output.
    """
    
    def __init__(self, agent: TTSAgent, chunk_size: int = 1024) -> None:
        """
        Initialize streaming TTS processor.
        
        Args:
            agent: TTS Agent instance
            chunk_size: Size of audio chunks for streaming
        """
        self.agent = agent
        self.chunk_size = chunk_size
        self._logger = logging.getLogger(__name__)
    
    async def stream_speech(
        self,
        text: str,
        voice: Optional[Voice] = None,
        model: Optional[TTSModel] = None,
        format: Optional[AudioFormat] = None,
        speed: Optional[float] = None,
        output_path: Optional[Union[str, Path]] = None,
        chunk_callback: Optional[Callable[[bytes], None]] = None
    ) -> AsyncIterator[bytes]:
        """
        Stream speech generation in chunks.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use
            model: TTS model to use
            format: Audio format
            speed: Speech speed
            output_path: Path to save complete audio file
            chunk_callback: Callback function for each chunk
            
        Yields:
            Audio data chunks as bytes
        """
        try:
            # Create request
            request = TTSRequest(
                text=text,
                voice=voice or self.agent.config.default_voice,
                model=model or self.agent.config.default_model,
                format=format or self.agent.config.default_format,
                speed=speed or self.agent.config.default_speed
            )
            
            self._logger.info(f"Starting streaming speech for text: {text[:50]}...")
            
            # Stream audio data
            audio_chunks = []
            async for chunk in self._stream_audio_chunks(request):
                audio_chunks.append(chunk)
                
                # Call chunk callback if provided
                if chunk_callback:
                    try:
                        chunk_callback(chunk)
                    except Exception as e:
                        self._logger.warning(f"Chunk callback error: {str(e)}")
                
                yield chunk
            
            # Save complete audio file if output path provided
            if output_path and audio_chunks:
                complete_audio = b"".join(audio_chunks)
                await self._save_streaming_audio(complete_audio, output_path, request.format)
            
            self._logger.info("Streaming speech completed successfully")
            
        except Exception as e:
            self._logger.error(f"Streaming speech failed: {str(e)}")
            raise TTSAgentError(f"Streaming speech failed: {str(e)}")
    
    async def _stream_audio_chunks(self, request: TTSRequest) -> AsyncIterator[bytes]:
        """
        Stream audio chunks from OpenAI API.
        
        Args:
            request: TTS request parameters
            
        Yields:
            Audio data chunks
        """
        if not self.agent._client:
            raise TTSAgentError("OpenAI client not initialized")
        
        try:
            # Prepare API parameters
            api_params = {
                "model": request.model,
                "voice": request.voice,
                "input": request.text,
                "response_format": request.format,
                "speed": request.speed
            }
            
            self._logger.debug(f"Starting streaming API call: {api_params}")
            
            # Make streaming API call
            async with self.agent._client.audio.speech.with_streaming_response.create(**api_params) as response:
                async for chunk in response.iter_bytes(chunk_size=self.chunk_size):
                    if chunk:
                        yield chunk
                        
        except Exception as e:
            self._logger.error(f"Streaming API call failed: {str(e)}")
            raise TTSAPIError(f"Streaming API call failed: {str(e)}")
    
    async def _save_streaming_audio(
        self, 
        audio_data: bytes, 
        output_path: Union[str, Path], 
        format: AudioFormat
    ) -> Path:
        """
        Save streaming audio data to file.
        
        Args:
            audio_data: Complete audio data
            output_path: Path to save file
            format: Audio format for file extension
            
        Returns:
            Path to saved file
        """
        try:
            output_path = Path(output_path)
            
            # Add file extension if not present
            if not output_path.suffix:
                output_path = output_path.with_suffix(f".{format}")
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write audio data asynchronously
            async with aiofiles.open(output_path, 'wb') as f:
                await f.write(audio_data)
            
            self._logger.info(f"Streaming audio saved: {output_path}")
            return output_path
            
        except Exception as e:
            self._logger.error(f"Failed to save streaming audio: {str(e)}")
            raise TTSAgentError(f"Failed to save streaming audio: {str(e)}")
    
    async def stream_speech_to_file(
        self,
        text: str,
        output_path: Union[str, Path],
        voice: Optional[Voice] = None,
        model: Optional[TTSModel] = None,
        format: Optional[AudioFormat] = None,
        speed: Optional[float] = None
    ) -> Path:
        """
        Stream speech directly to file with real-time writing.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            voice: Voice to use
            model: TTS model to use
            format: Audio format
            speed: Speech speed
            
        Returns:
            Path to saved file
        """
        try:
            output_path = Path(output_path)
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get format for file extension
            if not output_path.suffix:
                format = format or self.agent.config.default_format
                output_path = output_path.with_suffix(f".{format}")
            
            self._logger.info(f"Streaming speech to file: {output_path}")
            
            # Stream and write to file
            async with aiofiles.open(output_path, 'wb') as f:
                async for chunk in self.stream_speech(
                    text=text,
                    voice=voice,
                    model=model,
                    format=format,
                    speed=speed
                ):
                    await f.write(chunk)
            
            self._logger.info(f"Streaming to file completed: {output_path}")
            return output_path
            
        except Exception as e:
            self._logger.error(f"Streaming to file failed: {str(e)}")
            raise TTSAgentError(f"Streaming to file failed: {str(e)}")
    
    async def stream_speech_with_progress(
        self,
        text: str,
        voice: Optional[Voice] = None,
        model: Optional[TTSModel] = None,
        format: Optional[AudioFormat] = None,
        speed: Optional[float] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> bytes:
        """
        Stream speech with progress tracking.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use
            model: TTS model to use
            format: Audio format
            speed: Speech speed
            progress_callback: Callback for progress updates (bytes_received, total_estimated)
            
        Returns:
            Complete audio data
        """
        try:
            audio_chunks = []
            total_bytes = 0
            
            async for chunk in self.stream_speech(
                text=text,
                voice=voice,
                model=model,
                format=format,
                speed=speed
            ):
                audio_chunks.append(chunk)
                total_bytes += len(chunk)
                
                # Call progress callback if provided
                if progress_callback:
                    try:
                        # Estimate total based on text length (rough approximation)
                        estimated_total = len(text) * 100  # Rough estimate
                        progress_callback(total_bytes, estimated_total)
                    except Exception as e:
                        self._logger.warning(f"Progress callback error: {str(e)}")
            
            complete_audio = b"".join(audio_chunks)
            self._logger.info(f"Streaming with progress completed: {total_bytes} bytes")
            return complete_audio
            
        except Exception as e:
            self._logger.error(f"Streaming with progress failed: {str(e)}")
            raise TTSAgentError(f"Streaming with progress failed: {str(e)}")
    
    def get_chunk_size(self) -> int:
        """Get current chunk size."""
        return self.chunk_size
    
    def set_chunk_size(self, chunk_size: int) -> None:
        """
        Set chunk size for streaming.
        
        Args:
            chunk_size: New chunk size
        """
        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive")
        
        self.chunk_size = chunk_size
        self._logger.info(f"Chunk size updated to: {chunk_size}")
