"""
Core TTS Agent implementation.

This module contains the main TTSAgent class that provides the primary interface
for text-to-speech conversion using OpenAI's TTS-1 model.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, Union, Dict, Any
from openai import AsyncOpenAI
from openai.types.audio import Speech

from .models import TTSRequest, TTSResponse, TTSConfig, Voice, AudioFormat, TTSModel
from .exceptions import TTSAgentError, TTSConfigError, TTSAPIError, TTSValidationError, TTSFileError


class TTSAgent:
    """
    Professional Text-to-Speech Agent using OpenAI TTS-1.
    
    This class provides a comprehensive interface for text-to-speech conversion
    with advanced features like error handling, logging, and configuration management.
    """
    
    def __init__(self, config: Optional[TTSConfig] = None) -> None:
        """
        Initialize TTS Agent.
        
        Args:
            config: TTS configuration. If None, will use environment variables.
        """
        self.config = config or TTSConfig()
        self._client: Optional[AsyncOpenAI] = None
        self._logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize OpenAI client with configuration."""
        try:
            client_kwargs = {}
            
            if self.config.api_key:
                client_kwargs["api_key"] = self.config.api_key
            
            if self.config.base_url:
                client_kwargs["base_url"] = self.config.base_url
            
            self._client = AsyncOpenAI(**client_kwargs)
            self._logger.info("OpenAI client initialized successfully")
            
        except Exception as e:
            raise TTSConfigError(f"Failed to initialize OpenAI client: {str(e)}")
    
    async def generate_speech(
        self,
        text: str,
        voice: Optional[Voice] = None,
        model: Optional[TTSModel] = None,
        format: Optional[AudioFormat] = None,
        speed: Optional[float] = None,
        output_path: Optional[Union[str, Path]] = None
    ) -> TTSResponse:
        """
        Generate speech from text.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (defaults to config default)
            model: TTS model to use (defaults to config default)
            format: Audio format (defaults to config default)
            speed: Speech speed (defaults to config default)
            output_path: Path to save audio file (optional)
            
        Returns:
            TTSResponse with audio data and metadata
            
        Raises:
            TTSValidationError: If input validation fails
            TTSAPIError: If API request fails
            TTSFileError: If file operations fail
        """
        try:
            # Create request with defaults
            request = TTSRequest(
                text=text,
                voice=voice or self.config.default_voice,
                model=model or self.config.default_model,
                format=format or self.config.default_format,
                speed=speed or self.config.default_speed
            )
            
            self._logger.info(f"Generating speech for text: {text[:50]}...")
            
            # Generate speech using OpenAI API
            audio_data = await self._call_openai_api(request)
            
            # Prepare response
            response = TTSResponse(
                success=True,
                audio_data=audio_data,
                file_size=len(audio_data) if audio_data else None,
                metadata={
                    "voice": request.voice,
                    "model": request.model,
                    "format": request.format,
                    "speed": request.speed,
                    "text_length": len(text)
                }
            )
            
            # Save to file if output path provided
            if output_path:
                saved_path = await self._save_audio_file(audio_data, output_path, request.format)
                response.file_path = saved_path
                self._logger.info(f"Audio saved to: {saved_path}")
            
            self._logger.info("Speech generation completed successfully")
            return response
            
        except TTSValidationError:
            raise
        except TTSAPIError:
            raise
        except Exception as e:
            self._logger.error(f"Unexpected error during speech generation: {str(e)}")
            return TTSResponse(
                success=False,
                error=f"Unexpected error: {str(e)}"
            )
    
    async def _call_openai_api(self, request: TTSRequest) -> bytes:
        """
        Call OpenAI API for speech generation.
        
        Args:
            request: TTS request parameters
            
        Returns:
            Audio data as bytes
            
        Raises:
            TTSAPIError: If API call fails
        """
        if not self._client:
            raise TTSConfigError("OpenAI client not initialized")
        
        try:
            # Prepare API parameters
            api_params = {
                "model": request.model,
                "voice": request.voice,
                "input": request.text,
                "response_format": request.format,
                "speed": request.speed
            }
            
            self._logger.debug(f"Calling OpenAI API with params: {api_params}")
            
            # Make API call with retries
            for attempt in range(self.config.max_retries + 1):
                try:
                    response: Speech = await self._client.audio.speech.create(**api_params)
                    
                    # Convert response to bytes
                    audio_data = b""
                    async for chunk in response.iter_bytes():
                        audio_data += chunk
                    
                    self._logger.info(f"API call successful (attempt {attempt + 1})")
                    return audio_data
                    
                except Exception as e:
                    if attempt < self.config.max_retries:
                        self._logger.warning(f"API call failed (attempt {attempt + 1}), retrying: {str(e)}")
                        await asyncio.sleep(self.config.rate_limit_delay * (attempt + 1))
                    else:
                        raise TTSAPIError(f"API call failed after {self.config.max_retries + 1} attempts: {str(e)}")
            
        except TTSAPIError:
            raise
        except Exception as e:
            raise TTSAPIError(f"Unexpected API error: {str(e)}")
    
    async def _save_audio_file(
        self, 
        audio_data: bytes, 
        output_path: Union[str, Path], 
        format: AudioFormat
    ) -> Path:
        """
        Save audio data to file.
        
        Args:
            audio_data: Audio data to save
            output_path: Path to save file
            format: Audio format for file extension
            
        Returns:
            Path to saved file
            
        Raises:
            TTSFileError: If file operations fail
        """
        try:
            output_path = Path(output_path)
            
            # Add file extension if not present
            if not output_path.suffix:
                output_path = output_path.with_suffix(f".{format}")
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write audio data
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            self._logger.info(f"Audio file saved: {output_path}")
            return output_path
            
        except Exception as e:
            raise TTSFileError(f"Failed to save audio file: {str(e)}", str(output_path))
    
    async def generate_speech_streaming(
        self,
        text: str,
        voice: Optional[Voice] = None,
        model: Optional[TTSModel] = None,
        format: Optional[AudioFormat] = None,
        speed: Optional[float] = None,
        output_path: Optional[Union[str, Path]] = None
    ) -> TTSResponse:
        """
        Generate speech with streaming response for better performance.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (defaults to config default)
            model: TTS model to use (defaults to config default)
            format: Audio format (defaults to config default)
            speed: Speech speed (defaults to config default)
            output_path: Path to save audio file (optional)
            
        Returns:
            TTSResponse with audio data and metadata
        """
        try:
            # Create request with defaults
            request = TTSRequest(
                text=text,
                voice=voice or self.config.default_voice,
                model=model or self.config.default_model,
                format=format or self.config.default_format,
                speed=speed or self.config.default_speed
            )
            
            self._logger.info(f"Generating streaming speech for text: {text[:50]}...")
            
            # Generate speech with streaming
            audio_data = await self._call_openai_api_streaming(request)
            
            # Prepare response
            response = TTSResponse(
                success=True,
                audio_data=audio_data,
                file_size=len(audio_data) if audio_data else None,
                metadata={
                    "voice": request.voice,
                    "model": request.model,
                    "format": request.format,
                    "speed": request.speed,
                    "text_length": len(text),
                    "streaming": True
                }
            )
            
            # Save to file if output path provided
            if output_path:
                saved_path = await self._save_audio_file(audio_data, output_path, request.format)
                response.file_path = saved_path
                self._logger.info(f"Streaming audio saved to: {saved_path}")
            
            self._logger.info("Streaming speech generation completed successfully")
            return response
            
        except Exception as e:
            self._logger.error(f"Unexpected error during streaming speech generation: {str(e)}")
            return TTSResponse(
                success=False,
                error=f"Unexpected error: {str(e)}"
            )
    
    async def _call_openai_api_streaming(self, request: TTSRequest) -> bytes:
        """
        Call OpenAI API with streaming response.
        
        Args:
            request: TTS request parameters
            
        Returns:
            Audio data as bytes
        """
        if not self._client:
            raise TTSConfigError("OpenAI client not initialized")
        
        try:
            # Prepare API parameters
            api_params = {
                "model": request.model,
                "voice": request.voice,
                "input": request.text,
                "response_format": request.format,
                "speed": request.speed
            }
            
            self._logger.debug(f"Calling OpenAI API with streaming: {api_params}")
            
            # Make streaming API call
            async with self._client.audio.speech.with_streaming_response.create(**api_params) as response:
                audio_data = b""
                async for chunk in response.iter_bytes():
                    audio_data += chunk
                
                self._logger.info("Streaming API call successful")
                return audio_data
                
        except Exception as e:
            raise TTSAPIError(f"Streaming API call failed: {str(e)}")
    
    def get_available_voices(self) -> list[Voice]:
        """Get list of available voices."""
        return list(Voice)
    
    def get_available_models(self) -> list[TTSModel]:
        """Get list of available models."""
        return list(TTSModel)
    
    def get_available_formats(self) -> list[AudioFormat]:
        """Get list of available audio formats."""
        return list(AudioFormat)
    
    async def close(self) -> None:
        """Close the TTS agent and cleanup resources."""
        if self._client:
            await self._client.close()
            self._logger.info("TTS Agent closed successfully")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
