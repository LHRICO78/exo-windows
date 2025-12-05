"""
Backend service module for distributed inference processing.
Handles model inference requests through a unified interface.
"""

import asyncio
import json
import hashlib
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class InferenceRequest:
    """Represents an inference request."""
    request_id: str
    model_name: str
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 1.0
    top_k: int = 50
    system_prompt: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        if self.metadata is None:
            data['metadata'] = {}
        return data


@dataclass
class InferenceResponse:
    """Represents an inference response."""
    request_id: str
    status: str  # "success", "error", "processing"
    result: Optional[str] = None
    error_message: Optional[str] = None
    processing_time_ms: float = 0.0
    tokens_generated: int = 0
    model_name: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class BackendService:
    """
    Unified backend service for distributed inference.
    Abstracts the underlying inference engine and model management.
    """
    
    def __init__(self, inference_engine=None, model_manager=None):
        """
        Initialize the backend service.
        
        Args:
            inference_engine: The inference engine to use
            model_manager: The model manager instance
        """
        self.inference_engine = inference_engine
        self.model_manager = model_manager
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.response_cache: Dict[str, InferenceResponse] = {}
        self.active_requests: Dict[str, asyncio.Task] = {}
        self.request_handlers: List[Callable] = []
        self._running = False
    
    async def initialize(self):
        """Initialize the backend service."""
        self._running = True
        logger.info("Backend service initialized")
    
    async def shutdown(self):
        """Shutdown the backend service."""
        self._running = False
        # Cancel all active requests
        for task in self.active_requests.values():
            task.cancel()
        logger.info("Backend service shutdown")
    
    async def process_request(self, request: InferenceRequest) -> InferenceResponse:
        """
        Process an inference request.
        
        Args:
            request: The inference request
            
        Returns:
            The inference response
        """
        if not self._running:
            return InferenceResponse(
                request_id=request.request_id,
                status="error",
                error_message="Service is not running"
            )
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(request)
            if cache_key in self.response_cache:
                return self.response_cache[cache_key]
            
            # Create processing task
            task = asyncio.create_task(
                self._execute_inference(request)
            )
            self.active_requests[request.request_id] = task
            
            # Wait for completion with timeout
            response = await asyncio.wait_for(task, timeout=300.0)
            
            # Cache the response
            self.response_cache[cache_key] = response
            
            return response
            
        except asyncio.TimeoutError:
            return InferenceResponse(
                request_id=request.request_id,
                status="error",
                error_message="Request timeout"
            )
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return InferenceResponse(
                request_id=request.request_id,
                status="error",
                error_message=str(e)
            )
        finally:
            # Clean up
            self.active_requests.pop(request.request_id, None)
    
    async def _execute_inference(self, request: InferenceRequest) -> InferenceResponse:
        """
        Execute the actual inference.
        
        Args:
            request: The inference request
            
        Returns:
            The inference response
        """
        import time
        start_time = time.time()
        
        try:
            # Call the inference engine
            if self.inference_engine is None:
                raise RuntimeError("Inference engine not configured")
            
            # Prepare the input
            messages = []
            if request.system_prompt:
                messages.append({
                    "role": "system",
                    "content": request.system_prompt
                })
            messages.append({
                "role": "user",
                "content": request.prompt
            })
            
            # Execute inference
            result = await self.inference_engine.generate(
                model=request.model_name,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                top_k=request.top_k,
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return InferenceResponse(
                request_id=request.request_id,
                status="success",
                result=result.get("content", ""),
                model_name=request.model_name,
                processing_time_ms=processing_time,
                tokens_generated=result.get("tokens", 0),
            )
            
        except Exception as e:
            logger.error(f"Inference execution failed: {str(e)}")
            return InferenceResponse(
                request_id=request.request_id,
                status="error",
                error_message=str(e),
                processing_time_ms=(time.time() - start_time) * 1000,
            )
    
    def _generate_cache_key(self, request: InferenceRequest) -> str:
        """
        Generate a cache key for a request.
        
        Args:
            request: The inference request
            
        Returns:
            A cache key string
        """
        key_data = f"{request.model_name}:{request.prompt}:{request.temperature}:{request.top_p}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def register_request_handler(self, handler: Callable):
        """
        Register a custom request handler.
        
        Args:
            handler: A callable that processes requests
        """
        self.request_handlers.append(handler)
    
    async def process_batch(self, requests: List[InferenceRequest]) -> List[InferenceResponse]:
        """
        Process multiple requests concurrently.
        
        Args:
            requests: List of inference requests
            
        Returns:
            List of inference responses
        """
        tasks = [
            self.process_request(req) for req in requests
        ]
        return await asyncio.gather(*tasks)
    
    def get_service_status(self) -> Dict[str, Any]:
        """
        Get the current service status.
        
        Returns:
            Service status information
        """
        return {
            "running": self._running,
            "active_requests": len(self.active_requests),
            "cached_responses": len(self.response_cache),
            "registered_handlers": len(self.request_handlers),
            "timestamp": datetime.utcnow().isoformat(),
        }


class ServiceManager:
    """Manages backend service lifecycle and configuration."""
    
    _instance: Optional[BackendService] = None
    
    @classmethod
    def get_service(cls) -> BackendService:
        """Get or create the backend service instance."""
        if cls._instance is None:
            cls._instance = BackendService()
        return cls._instance
    
    @classmethod
    async def initialize_service(cls, inference_engine=None, model_manager=None):
        """Initialize the backend service."""
        service = cls.get_service()
        service.inference_engine = inference_engine
        service.model_manager = model_manager
        await service.initialize()
        return service
    
    @classmethod
    async def shutdown_service(cls):
        """Shutdown the backend service."""
        if cls._instance is not None:
            await cls._instance.shutdown()
            cls._instance = None
