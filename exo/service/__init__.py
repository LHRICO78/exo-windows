"""
Service module for distributed inference backend.
Provides unified interface for inference processing.
"""

from exo.service.backend_service import (
    BackendService,
    ServiceManager,
    InferenceRequest,
    InferenceResponse,
)

__all__ = [
    "BackendService",
    "ServiceManager",
    "InferenceRequest",
    "InferenceResponse",
]
