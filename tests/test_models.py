"""
Tests for TTS Agents models.

This module contains tests for all Pydantic models used in the TTS Agents library.
"""

import pytest
from pathlib import Path
from pydantic import ValidationError

from tts_agents.models import (
    TTSRequest, TTSResponse, TTSConfig, BatchTTSRequest, BatchTTSResponse,
    Voice, AudioFormat, TTSModel
)


class TestTTSRequest:
    """Test TTSRequest model."""
    
    def test_valid_request(self):
        """Test valid TTS request creation."""
        request = TTSRequest(
            text="Hello, world!",
            voice=Voice.ALLOY,
            model=TTSModel.TTS_1,
            format=AudioFormat.MP3,
            speed=1.0
        )
        
        assert request.text == "Hello, world!"
        assert request.voice == Voice.ALLOY
        assert request.model == TTSModel.TTS_1
        assert request.format == AudioFormat.MP3
        assert request.speed == 1.0
    
    def test_default_values(self):
        """Test default values for TTS request."""
        request = TTSRequest(text="Test text")
        
        assert request.voice == Voice.ALLOY
        assert request.model == TTSModel.TTS_1
        assert request.format == AudioFormat.MP3
        assert request.speed == 1.0
    
    def test_text_validation(self):
        """Test text validation."""
        # Empty text should fail
        with pytest.raises(ValidationError):
            TTSRequest(text="")
        
        # Whitespace only should fail
        with pytest.raises(ValidationError):
            TTSRequest(text="   ")
        
        # Text should be stripped
        request = TTSRequest(text="  Hello, world!  ")
        assert request.text == "Hello, world!"
    
    def test_speed_validation(self):
        """Test speed validation."""
        # Valid speeds
        for speed in [0.25, 1.0, 2.0, 4.0]:
            request = TTSRequest(text="Test", speed=speed)
            assert request.speed == speed
        
        # Invalid speeds should fail
        for speed in [0.1, 5.0, -1.0]:
            with pytest.raises(ValidationError):
                TTSRequest(text="Test", speed=speed)
    
    def test_text_length_validation(self):
        """Test text length validation."""
        # Valid length
        request = TTSRequest(text="A" * 1000)
        assert len(request.text) == 1000
        
        # Too long should fail
        with pytest.raises(ValidationError):
            TTSRequest(text="A" * 5000)


class TestTTSResponse:
    """Test TTSResponse model."""
    
    def test_successful_response(self):
        """Test successful TTS response."""
        response = TTSResponse(
            success=True,
            audio_data=b"fake_audio_data",
            file_size=1000,
            metadata={"voice": "alloy"}
        )
        
        assert response.success is True
        assert response.audio_data == b"fake_audio_data"
        assert response.file_size == 1000
        assert response.metadata == {"voice": "alloy"}
        assert response.error is None
    
    def test_failed_response(self):
        """Test failed TTS response."""
        response = TTSResponse(
            success=False,
            error="API error occurred"
        )
        
        assert response.success is False
        assert response.error == "API error occurred"
        assert response.audio_data is None
    
    def test_file_path_validation(self):
        """Test file path validation."""
        # Valid existing file
        test_file = Path(__file__)
        response = TTSResponse(
            success=True,
            file_path=test_file
        )
        assert response.file_path == test_file
        
        # Non-existent file should fail
        with pytest.raises(ValidationError):
            TTSResponse(
                success=True,
                file_path=Path("non_existent_file.mp3")
            )


class TestTTSConfig:
    """Test TTSConfig model."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = TTSConfig()
        
        assert config.api_key is None
        assert config.base_url is None
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.rate_limit_delay == 1.0
        assert config.default_voice == Voice.ALLOY
        assert config.default_model == TTSModel.TTS_1
        assert config.default_format == AudioFormat.MP3
        assert config.default_speed == 1.0
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = TTSConfig(
            api_key="sk-test123",
            base_url="https://api.openai.com/v1",
            timeout=60,
            max_retries=5,
            rate_limit_delay=2.0,
            default_voice=Voice.ECHO,
            default_model=TTSModel.TTS_1_HD,
            default_format=AudioFormat.OPUS,
            default_speed=1.5
        )
        
        assert config.api_key == "sk-test123"
        assert config.base_url == "https://api.openai.com/v1"
        assert config.timeout == 60
        assert config.max_retries == 5
        assert config.rate_limit_delay == 2.0
        assert config.default_voice == Voice.ECHO
        assert config.default_model == TTSModel.TTS_1_HD
        assert config.default_format == AudioFormat.OPUS
        assert config.default_speed == 1.5
    
    def test_api_key_validation(self):
        """Test API key validation."""
        # Valid API key
        config = TTSConfig(api_key="sk-1234567890abcdef")
        assert config.api_key == "sk-1234567890abcdef"
        
        # Invalid API key should fail
        with pytest.raises(ValidationError):
            TTSConfig(api_key="invalid_key")
    
    def test_base_url_validation(self):
        """Test base URL validation."""
        # Valid URLs
        for url in ["https://api.openai.com", "http://localhost:8000"]:
            config = TTSConfig(base_url=url)
            assert config.base_url == url
        
        # Invalid URLs should fail
        with pytest.raises(ValidationError):
            TTSConfig(base_url="invalid_url")
    
    def test_timeout_validation(self):
        """Test timeout validation."""
        # Valid timeouts
        for timeout in [5, 30, 300]:
            config = TTSConfig(timeout=timeout)
            assert config.timeout == timeout
        
        # Invalid timeouts should fail
        for timeout in [1, 400]:
            with pytest.raises(ValidationError):
                TTSConfig(timeout=timeout)


class TestBatchTTSRequest:
    """Test BatchTTSRequest model."""
    
    def test_valid_batch_request(self):
        """Test valid batch request."""
        requests = [
            TTSRequest(text="Text 1"),
            TTSRequest(text="Text 2")
        ]
        
        batch_request = BatchTTSRequest(
            requests=requests,
            output_directory=Path("./output"),
            concurrent_limit=5,
            retry_attempts=3
        )
        
        assert len(batch_request.requests) == 2
        assert batch_request.output_directory == Path("./output")
        assert batch_request.concurrent_limit == 5
        assert batch_request.retry_attempts == 3
    
    def test_empty_requests_validation(self):
        """Test empty requests validation."""
        with pytest.raises(ValidationError):
            BatchTTSRequest(requests=[])
    
    def test_too_many_requests_validation(self):
        """Test too many requests validation."""
        requests = [TTSRequest(text=f"Text {i}") for i in range(101)]
        
        with pytest.raises(ValidationError):
            BatchTTSRequest(requests=requests)
    
    def test_concurrent_limit_validation(self):
        """Test concurrent limit validation."""
        requests = [TTSRequest(text="Test")]
        
        # Valid limits
        for limit in [1, 5, 20]:
            batch_request = BatchTTSRequest(requests=requests, concurrent_limit=limit)
            assert batch_request.concurrent_limit == limit
        
        # Invalid limits should fail
        for limit in [0, 25]:
            with pytest.raises(ValidationError):
                BatchTTSRequest(requests=requests, concurrent_limit=limit)


class TestBatchTTSResponse:
    """Test BatchTTSResponse model."""
    
    def test_valid_batch_response(self):
        """Test valid batch response."""
        results = [
            TTSResponse(success=True),
            TTSResponse(success=False, error="Test error")
        ]
        
        response = BatchTTSResponse(
            total_requests=2,
            successful=1,
            failed=1,
            results=results,
            processing_time=5.0,
            errors=["Test error"]
        )
        
        assert response.total_requests == 2
        assert response.successful == 1
        assert response.failed == 1
        assert len(response.results) == 2
        assert response.processing_time == 5.0
        assert response.errors == ["Test error"]
    
    def test_count_validation(self):
        """Test count validation."""
        results = [TTSResponse(success=True), TTSResponse(success=False)]
        
        # Valid counts
        response = BatchTTSResponse(
            total_requests=2,
            successful=1,
            failed=1,
            results=results,
            processing_time=1.0
        )
        assert response.total_requests == 2
        
        # Invalid counts should fail
        with pytest.raises(ValidationError):
            BatchTTSResponse(
                total_requests=2,
                successful=2,
                failed=1,  # Should be 0
                results=results,
                processing_time=1.0
            )


class TestEnums:
    """Test enum models."""
    
    def test_voice_enum(self):
        """Test Voice enum."""
        assert Voice.ALLOY == "alloy"
        assert Voice.ECHO == "echo"
        assert Voice.FABLE == "fable"
        assert Voice.ONYX == "onyx"
        assert Voice.NOVA == "nova"
        assert Voice.SHIMMER == "shimmer"
    
    def test_audio_format_enum(self):
        """Test AudioFormat enum."""
        assert AudioFormat.MP3 == "mp3"
        assert AudioFormat.OPUS == "opus"
        assert AudioFormat.AAC == "aac"
        assert AudioFormat.FLAC == "flac"
    
    def test_tts_model_enum(self):
        """Test TTSModel enum."""
        assert TTSModel.TTS_1 == "tts-1"
        assert TTSModel.TTS_1_HD == "tts-1-hd"
