"""
Batch processing for TTS operations.

This module provides efficient batch processing capabilities for multiple
TTS requests with concurrent execution and comprehensive error handling.
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Optional, Union, Dict, Any
from asyncio_throttle import Throttler

from .core import TTSAgent
from .models import BatchTTSRequest, BatchTTSResponse, TTSRequest, TTSResponse
from .exceptions import TTSAgentError, TTSValidationError


class BatchProcessor:
    """
    Batch processor for multiple TTS operations.
    
    Provides efficient concurrent processing of multiple TTS requests
    with rate limiting, error handling, and progress tracking.
    """
    
    def __init__(self, agent: TTSAgent, max_concurrent: int = 5) -> None:
        """
        Initialize batch processor.
        
        Args:
            agent: TTS Agent instance
            max_concurrent: Maximum concurrent requests
        """
        self.agent = agent
        self.max_concurrent = max_concurrent
        self.throttler = Throttler(rate_limit=max_concurrent, period=1.0)
        self._logger = logging.getLogger(__name__)
    
    async def process_batch(
        self,
        requests: List[TTSRequest],
        output_directory: Optional[Union[str, Path]] = None,
        retry_attempts: int = 3
    ) -> BatchTTSResponse:
        """
        Process multiple TTS requests concurrently.
        
        Args:
            requests: List of TTS requests to process
            output_directory: Directory to save audio files
            retry_attempts: Number of retry attempts for failed requests
            
        Returns:
            BatchTTSResponse with processing results
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Validate inputs
            if not requests:
                raise TTSValidationError("No requests provided for batch processing")
            
            if len(requests) > 100:
                raise TTSValidationError("Maximum 100 requests allowed per batch")
            
            self._logger.info(f"Starting batch processing for {len(requests)} requests")
            
            # Prepare output directory
            if output_directory:
                output_dir = Path(output_directory)
                output_dir.mkdir(parents=True, exist_ok=True)
            else:
                output_dir = None
            
            # Create semaphore for concurrency control
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            # Process requests concurrently
            tasks = [
                self._process_single_request(request, output_dir, retry_attempts, semaphore)
                for request in requests
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            successful = 0
            failed = 0
            errors = []
            processed_results = []
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    failed += 1
                    error_msg = f"Request {i}: {str(result)}"
                    errors.append(error_msg)
                    processed_results.append(TTSResponse(
                        success=False,
                        error=error_msg
                    ))
                elif isinstance(result, TTSResponse):
                    if result.success:
                        successful += 1
                    else:
                        failed += 1
                        if result.error:
                            errors.append(f"Request {i}: {result.error}")
                    processed_results.append(result)
                else:
                    failed += 1
                    error_msg = f"Request {i}: Unknown error"
                    errors.append(error_msg)
                    processed_results.append(TTSResponse(
                        success=False,
                        error=error_msg
                    ))
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            self._logger.info(
                f"Batch processing completed: {successful} successful, {failed} failed, "
                f"took {processing_time:.2f}s"
            )
            
            return BatchTTSResponse(
                total_requests=len(requests),
                successful=successful,
                failed=failed,
                results=processed_results,
                processing_time=processing_time,
                errors=errors
            )
            
        except Exception as e:
            self._logger.error(f"Batch processing failed: {str(e)}")
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return BatchTTSResponse(
                total_requests=len(requests),
                successful=0,
                failed=len(requests),
                results=[TTSResponse(success=False, error=str(e)) for _ in requests],
                processing_time=processing_time,
                errors=[str(e)]
            )
    
    async def _process_single_request(
        self,
        request: TTSRequest,
        output_directory: Optional[Path],
        retry_attempts: int,
        semaphore: asyncio.Semaphore
    ) -> TTSResponse:
        """
        Process a single TTS request with retry logic.
        
        Args:
            request: TTS request to process
            output_directory: Directory to save audio file
            retry_attempts: Number of retry attempts
            semaphore: Semaphore for concurrency control
            
        Returns:
            TTSResponse with result
        """
        async with semaphore:
            async with self.throttler:
                for attempt in range(retry_attempts + 1):
                    try:
                        # Prepare output path if directory provided
                        output_path = None
                        if output_directory:
                            # Generate filename based on request
                            filename = f"tts_{hash(request.text) % 1000000}.{request.format}"
                            output_path = output_directory / filename
                        
                        # Generate speech
                        response = await self.agent.generate_speech(
                            text=request.text,
                            voice=request.voice,
                            model=request.model,
                            format=request.format,
                            speed=request.speed,
                            output_path=output_path
                        )
                        
                        if response.success:
                            self._logger.debug(f"Request processed successfully (attempt {attempt + 1})")
                            return response
                        else:
                            if attempt < retry_attempts:
                                self._logger.warning(
                                    f"Request failed (attempt {attempt + 1}), retrying: {response.error}"
                                )
                                await asyncio.sleep(1.0 * (attempt + 1))
                            else:
                                self._logger.error(f"Request failed after {retry_attempts + 1} attempts")
                                return response
                    
                    except Exception as e:
                        if attempt < retry_attempts:
                            self._logger.warning(f"Request error (attempt {attempt + 1}), retrying: {str(e)}")
                            await asyncio.sleep(1.0 * (attempt + 1))
                        else:
                            self._logger.error(f"Request failed after {retry_attempts + 1} attempts: {str(e)}")
                            return TTSResponse(
                                success=False,
                                error=f"Failed after {retry_attempts + 1} attempts: {str(e)}"
                            )
                
                # This should never be reached, but just in case
                return TTSResponse(
                    success=False,
                    error="Unexpected error in retry logic"
                )
    
    async def process_batch_from_config(self, batch_request: BatchTTSRequest) -> BatchTTSResponse:
        """
        Process batch from BatchTTSRequest configuration.
        
        Args:
            batch_request: Batch TTS request configuration
            
        Returns:
            BatchTTSResponse with processing results
        """
        return await self.process_batch(
            requests=batch_request.requests,
            output_directory=batch_request.output_directory,
            retry_attempts=batch_request.retry_attempts
        )
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get current processing statistics.
        
        Returns:
            Dictionary with processing statistics
        """
        return {
            "max_concurrent": self.max_concurrent,
            "throttler_rate_limit": self.throttler.rate_limit,
            "throttler_period": self.throttler.period
        }
