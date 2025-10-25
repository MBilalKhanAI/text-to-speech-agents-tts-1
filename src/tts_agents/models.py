"""
Data models for TTS Agents library.

This module defines Pydantic models for type safety and validation
of TTS requests, responses, and configuration.
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pathlib import Path
from pydantic import BaseModel, Field, validator, root_validator


class Voice(str, Enum):
    """Available OpenAI TTS voices."""
    
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"


class AudioFormat(str, Enum):
    """Supported audio output formats."""
    
    MP3 = "mp3"
    OPUS = "opus"
    AAC = "aac"
    FLAC = "flac"


class TTSModel(str, Enum):
    """Available OpenAI TTS models."""
    
    TTS_1 = "tts-1"
    TTS_1_HD = "tts-1-hd"


class TTSRequest(BaseModel):
    """Request model for TTS conversion."""
    
    text: str = Field(..., min_length=1, max_length=4096, description="Text to convert to speech")
    voice: Voice = Field(default=Voice.ALLOY, description="Voice to use for synthesis")
    model: TTSModel = Field(default=TTSModel.TTS_1, description="TTS model to use")
    format: AudioFormat = Field(default=AudioFormat.MP3, description="Output audio format")
    speed: float = Field(default=1.0, ge=0.25, le=4.0, description="Speech speed multiplier")
    
    @validator('text')
    def validate_text(cls, v: str) -> str:
        """Validate and clean text input."""
        if not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        return v.strip()
    
    @validator('speed')
    def validate_speed(cls, v: float) -> float:
        """Validate speed is within OpenAI's supported range."""
        if not 0.25 <= v <= 4.0:
            raise ValueError("Speed must be between 0.25 and 4.0")
        return v
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        validate_assignment = True


class TTSResponse(BaseModel):
    """Response model for TTS conversion."""
    
    success: bool = Field(..., description="Whether the conversion was successful")
    audio_data: Optional[bytes] = Field(None, description="Generated audio data")
    file_path: Optional[Path] = Field(None, description="Path to saved audio file")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")
    file_size: Optional[int] = Field(None, description="Audio file size in bytes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    error: Optional[str] = Field(None, description="Error message if conversion failed")
    
    @validator('file_path')
    def validate_file_path(cls, v: Optional[Path]) -> Optional[Path]:
        """Validate file path exists if provided."""
        if v is not None and not v.exists():
            raise ValueError(f"Audio file does not exist: {v}")
        return v


class BatchTTSRequest(BaseModel):
    """Request model for batch TTS processing."""
    
    requests: List[TTSRequest] = Field(..., min_items=1, max_items=100, description="List of TTS requests")
    output_directory: Optional[Path] = Field(None, description="Directory to save audio files")
    concurrent_limit: int = Field(default=5, ge=1, le=20, description="Maximum concurrent requests")
    retry_attempts: int = Field(default=3, ge=0, le=10, description="Number of retry attempts")
    
    @validator('requests')
    def validate_requests(cls, v: List[TTSRequest]) -> List[TTSRequest]:
        """Validate batch requests."""
        if not v:
            raise ValueError("At least one TTS request is required")
        return v
    
    @validator('output_directory')
    def validate_output_directory(cls, v: Optional[Path]) -> Optional[Path]:
        """Validate output directory."""
        if v is not None:
            v.mkdir(parents=True, exist_ok=True)
        return v


class BatchTTSResponse(BaseModel):
    """Response model for batch TTS processing."""
    
    total_requests: int = Field(..., description="Total number of requests")
    successful: int = Field(..., description="Number of successful conversions")
    failed: int = Field(..., description="Number of failed conversions")
    results: List[TTSResponse] = Field(..., description="Individual TTS responses")
    processing_time: float = Field(..., description="Total processing time in seconds")
    errors: List[str] = Field(default_factory=list, description="List of error messages")
    
    @root_validator
    def validate_counts(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that counts match the actual results."""
        total = values.get('total_requests', 0)
        successful = values.get('successful', 0)
        failed = values.get('failed', 0)
        results = values.get('results', [])
        
        if successful + failed != total:
            raise ValueError("Successful and failed counts must equal total requests")
        
        if len(results) != total:
            raise ValueError("Number of results must equal total requests")
        
        return values


class TTSConfig(BaseModel):
    """Configuration model for TTS Agent."""
    
    api_key: Optional[str] = Field(None, description="OpenAI API key")
    base_url: Optional[str] = Field(None, description="OpenAI API base URL")
    timeout: int = Field(default=30, ge=5, le=300, description="Request timeout in seconds")
    max_retries: int = Field(default=3, ge=0, le=10, description="Maximum retry attempts")
    rate_limit_delay: float = Field(default=1.0, ge=0.1, le=10.0, description="Delay between requests")
    default_voice: Voice = Field(default=Voice.ALLOY, description="Default voice to use")
    default_model: TTSModel = Field(default=TTSModel.TTS_1, description="Default model to use")
    default_format: AudioFormat = Field(default=AudioFormat.MP3, description="Default audio format")
    default_speed: float = Field(default=1.0, ge=0.25, le=4.0, description="Default speech speed")
    
    @validator('api_key')
    def validate_api_key(cls, v: Optional[str]) -> Optional[str]:
        """Validate API key format."""
        if v is not None and not v.startswith('sk-'):
            raise ValueError("OpenAI API key must start with 'sk-'")
        return v
    
    @validator('base_url')
    def validate_base_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate base URL format."""
        if v is not None and not v.startswith(('http://', 'https://')):
            raise ValueError("Base URL must start with 'http://' or 'https://'")
        return v
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        validate_assignment = True
        extra = "forbid"
