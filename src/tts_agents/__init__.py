"""
TTS Agents - Professional Text-to-Speech with OpenAI TTS-1

A production-ready Python library for high-quality text-to-speech conversion
using OpenAI's TTS-1 model with advanced features like batch processing,
streaming, and comprehensive error handling.

Author: Muhammad Bilal Khan
License: MIT
Version: 1.0.0
"""

from .core import TTSAgent, TTSConfig
from .exceptions import TTSAgentError, TTSConfigError, TTSAPIError
from .models import Voice, AudioFormat, TTSRequest, TTSResponse
from .batch import BatchProcessor
from .streaming import StreamingTTS

__version__ = "1.0.0"
__author__ = "Muhammad Bilal Khan"
__email__ = "muhammadbilalkhan@ai.com"

__all__ = [
    "TTSAgent",
    "TTSConfig", 
    "TTSAgentError",
    "TTSConfigError",
    "TTSAPIError",
    "Voice",
    "AudioFormat",
    "TTSRequest",
    "TTSResponse",
    "BatchProcessor",
    "StreamingTTS",
]
