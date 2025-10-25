"""
Custom exceptions for TTS Agents library.

This module defines all custom exceptions used throughout the TTS Agents library,
providing clear error handling and debugging information.
"""

from typing import Optional


class TTSAgentError(Exception):
    """Base exception for all TTS Agent errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None) -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class TTSConfigError(TTSAgentError):
    """Raised when there's an error in TTS configuration."""
    
    def __init__(self, message: str, config_key: Optional[str] = None) -> None:
        self.config_key = config_key
        super().__init__(message, "CONFIG_ERROR")
    
    def __str__(self) -> str:
        if self.config_key:
            return f"[CONFIG_ERROR] Configuration error for '{self.config_key}': {self.message}"
        return f"[CONFIG_ERROR] {self.message}"


class TTSAPIError(TTSAgentError):
    """Raised when there's an error with the OpenAI API."""
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        api_error_type: Optional[str] = None
    ) -> None:
        self.status_code = status_code
        self.api_error_type = api_error_type
        super().__init__(message, "API_ERROR")
    
    def __str__(self) -> str:
        error_info = []
        if self.status_code:
            error_info.append(f"Status: {self.status_code}")
        if self.api_error_type:
            error_info.append(f"Type: {self.api_error_type}")
        
        error_details = f" ({', '.join(error_info)})" if error_info else ""
        return f"[API_ERROR] {self.message}{error_details}"


class TTSValidationError(TTSAgentError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None) -> None:
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")
    
    def __str__(self) -> str:
        if self.field:
            return f"[VALIDATION_ERROR] Validation error for field '{self.field}': {self.message}"
        return f"[VALIDATION_ERROR] {self.message}"


class TTSFileError(TTSAgentError):
    """Raised when there's an error with file operations."""
    
    def __init__(self, message: str, file_path: Optional[str] = None) -> None:
        self.file_path = file_path
        super().__init__(message, "FILE_ERROR")
    
    def __str__(self) -> str:
        if self.file_path:
            return f"[FILE_ERROR] File operation error for '{self.file_path}': {self.message}"
        return f"[FILE_ERROR] {self.message}"


class TTSRateLimitError(TTSAPIError):
    """Raised when API rate limits are exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None) -> None:
        self.retry_after = retry_after
        super().__init__(message, api_error_type="rate_limit")
    
    def __str__(self) -> str:
        retry_info = f" (retry after {self.retry_after}s)" if self.retry_after else ""
        return f"[RATE_LIMIT] {self.message}{retry_info}"
