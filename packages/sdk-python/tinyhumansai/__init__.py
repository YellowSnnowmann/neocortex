"""TinyHumans Python SDK."""

from __future__ import annotations

import logging
import os

from .client import TinyHumansMemoryClient
from .llm import SUPPORTED_LLM_PROVIDERS
from .types import (
    TinyHumansError,
    DeleteMemoryResponse,
    GetContextResponse,
    IngestMemoryResponse,
    LLMQueryResponse,
    MemoryItem,
    ReadMemoryItem,
)

logger = logging.getLogger("tinyhumansai")

_level = os.environ.get("TINYHUMANSAI_LOG_LEVEL")
if _level:
    # Optional, env-driven log level for easier debugging in apps and notebooks.
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO)
    logger.setLevel(_level.upper())

__all__ = [
    "TinyHumansMemoryClient",
    "TinyHumansError",
    "DeleteMemoryResponse",
    "IngestMemoryResponse",
    "LLMQueryResponse",
    "MemoryItem",
    "GetContextResponse",
    "ReadMemoryItem",
    "SUPPORTED_LLM_PROVIDERS",
    "logger",
]
