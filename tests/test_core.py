"""
Tests for TTS Agents core functionality.

This module contains tests for the main TTSAgent class and related functionality.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

from tts_agents.core import TTSAgent
from tts_agents.models import TTSConfig, TTSRequest, Voice, AudioFormat, TTSModel
from tts_agents.exceptions import TTSAgentError, TTSConfigError, TTSAPIError


class TestTTSAgent:
    """Test TTSAgent class."""
    
    def test_initialization_with_config(self):
        """Test TTSAgent initialization with config."""
        config = TTSConfig(api_key="sk-test123")
        agent = TTSAgent(config)
        
        assert agent.config == config
        assert agent._client is not None
    
    def test_initialization_without_config(self):
        """Test TTSAgent initialization without config."""
        agent = TTSAgent()
        
        assert agent.config is not None
        assert agent._client is not None
    
    @pytest.mark.asyncio
    async def test_generate_speech_success(self):
        """Test successful speech generation."""
        # Mock OpenAI client
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.iter_bytes.return_value = [b"fake_audio_data"]
        mock_client.audio.speech.create.return_value = mock_response
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            agent = TTSAgent()
            agent._client = mock_client
            
            response = await agent.generate_speech(
                text="Hello, world!",
                voice=Voice.ALLOY,
                model=TTSModel.TTS_1,
                format=AudioFormat.MP3,
                speed=1.0
            )
            
            assert response.success is True
            assert response.audio_data == b"fake_audio_data"
            assert response.file_size == len(b"fake_audio_data")
            assert response.metadata["voice"] == Voice.ALLOY
            assert response.metadata["model"] == TTSModel.TTS_1
    
    @pytest.mark.asyncio
    async def test_generate_speech_with_output_path(self):
        """Test speech generation with output file."""
        # Mock OpenAI client
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.iter_bytes.return_value = [b"fake_audio_data"]
        mock_client.audio.speech.create.return_value = mock_response
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            agent = TTSAgent()
            agent._client = mock_client
            
            # Create temporary output file
            output_path = Path("test_output.mp3")
            
            try:
                response = await agent.generate_speech(
                    text="Hello, world!",
                    output_path=output_path
                )
                
                assert response.success is True
                assert response.file_path == output_path
                assert output_path.exists()
            finally:
                # Clean up
                if output_path.exists():
                    output_path.unlink()
    
    @pytest.mark.asyncio
    async def test_generate_speech_api_error(self):
        """Test speech generation with API error."""
        # Mock OpenAI client to raise exception
        mock_client = AsyncMock()
        mock_client.audio.speech.create.side_effect = Exception("API Error")
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            agent = TTSAgent()
            agent._client = mock_client
            
            response = await agent.generate_speech(text="Hello, world!")
            
            assert response.success is False
            assert "Unexpected error" in response.error
    
    @pytest.mark.asyncio
    async def test_generate_speech_streaming_success(self):
        """Test successful streaming speech generation."""
        # Mock OpenAI client
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.iter_bytes.return_value = [b"fake_audio_data"]
        mock_client.audio.speech.with_streaming_response.create.return_value.__aenter__.return_value = mock_response
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            agent = TTSAgent()
            agent._client = mock_client
            
            response = await agent.generate_speech_streaming(
                text="Hello, world!",
                voice=Voice.ECHO,
                model=TTSModel.TTS_1_HD
            )
            
            assert response.success is True
            assert response.audio_data == b"fake_audio_data"
            assert response.metadata["streaming"] is True
    
    @pytest.mark.asyncio
    async def test_generate_speech_streaming_error(self):
        """Test streaming speech generation with error."""
        # Mock OpenAI client to raise exception
        mock_client = AsyncMock()
        mock_client.audio.speech.with_streaming_response.create.side_effect = Exception("Streaming Error")
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            agent = TTSAgent()
            agent._client = mock_client
            
            response = await agent.generate_speech_streaming(text="Hello, world!")
            
            assert response.success is False
            assert "Unexpected error" in response.error
    
    def test_get_available_voices(self):
        """Test getting available voices."""
        agent = TTSAgent()
        voices = agent.get_available_voices()
        
        assert len(voices) == 6
        assert Voice.ALLOY in voices
        assert Voice.ECHO in voices
        assert Voice.FABLE in voices
        assert Voice.ONYX in voices
        assert Voice.NOVA in voices
        assert Voice.SHIMMER in voices
    
    def test_get_available_models(self):
        """Test getting available models."""
        agent = TTSAgent()
        models = agent.get_available_models()
        
        assert len(models) == 2
        assert TTSModel.TTS_1 in models
        assert TTSModel.TTS_1_HD in models
    
    def test_get_available_formats(self):
        """Test getting available formats."""
        agent = TTSAgent()
        formats = agent.get_available_formats()
        
        assert len(formats) == 4
        assert AudioFormat.MP3 in formats
        assert AudioFormat.OPUS in formats
        assert AudioFormat.AAC in formats
        assert AudioFormat.FLAC in formats
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test TTSAgent as async context manager."""
        mock_client = AsyncMock()
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            async with TTSAgent() as agent:
                assert agent._client is not None
            
            # Should call close
            mock_client.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_close(self):
        """Test closing TTSAgent."""
        mock_client = AsyncMock()
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            agent = TTSAgent()
            agent._client = mock_client
            
            await agent.close()
            mock_client.close.assert_called_once()
    
    def test_invalid_config_initialization(self):
        """Test initialization with invalid config."""
        with patch('tts_agents.core.AsyncOpenAI', side_effect=Exception("Config Error")):
            with pytest.raises(TTSConfigError):
                TTSAgent()


class TestTTSAgentIntegration:
    """Integration tests for TTSAgent."""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test complete TTS workflow."""
        # Mock OpenAI client
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.iter_bytes.return_value = [b"fake_audio_data"]
        mock_client.audio.speech.create.return_value = mock_response
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            config = TTSConfig(
                api_key="sk-test123",
                default_voice=Voice.ECHO,
                default_model=TTSModel.TTS_1_HD
            )
            
            async with TTSAgent(config) as agent:
                # Test basic generation
                response = await agent.generate_speech(
                    text="Hello, world!",
                    output_path="test_output.mp3"
                )
                
                assert response.success is True
                assert response.audio_data == b"fake_audio_data"
                assert response.file_path == Path("test_output.mp3")
                
                # Test streaming generation
                streaming_response = await agent.generate_speech_streaming(
                    text="Streaming test"
                )
                
                assert streaming_response.success is True
                assert streaming_response.metadata["streaming"] is True
            
            # Clean up
            test_file = Path("test_output.mp3")
            if test_file.exists():
                test_file.unlink()
    
    @pytest.mark.asyncio
    async def test_error_handling_workflow(self):
        """Test error handling in complete workflow."""
        # Mock OpenAI client to raise different errors
        mock_client = AsyncMock()
        mock_client.audio.speech.create.side_effect = Exception("Network Error")
        
        with patch('tts_agents.core.AsyncOpenAI', return_value=mock_client):
            async with TTSAgent() as agent:
                response = await agent.generate_speech(text="Test")
                
                assert response.success is False
                assert "Unexpected error" in response.error
