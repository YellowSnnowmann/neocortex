"""LangGraph-compatible tools for Alphahuman Memory API.

Aligned with the AlphaHuman backend API: insert, query, admin/delete, recall, memories/recall.

Usage:

    from alphahuman_langgraph import make_memory_tools

    tools = make_memory_tools(token="your-api-key")
    llm_with_tools = llm.bind_tools(tools)

Or from environment (ALPHAHUMAN_API_KEY, optional ALPHAHUMAN_BASE_URL):

    from alphahuman_langgraph import get_tools
    tools = get_tools()
"""

from __future__ import annotations

import os
from typing import Any, Optional

from langchain_core.tools import tool

from alphahuman_langgraph.client import AlphahumanMemoryClient, DEFAULT_BASE_URL

_TOKEN_ENV = "ALPHAHUMAN_API_KEY"
_BASE_URL_ENV = "ALPHAHUMAN_BASE_URL"


def make_memory_tools(
    token: str,
    base_url: Optional[str] = None,
) -> list[Any]:
    """Create Alphahuman Memory tools bound to a specific client.

    Credentials are captured at construction and not exposed to the LLM.

    Args:
        token: Bearer token (API key or JWT).
        base_url: Optional API base URL override.

    Returns:
        List of LangChain tools: insert_memory, query_memory, delete_memory,
        recall_memory, recall_memories.
    """
    client = AlphahumanMemoryClient(token=token, base_url=base_url or DEFAULT_BASE_URL)

    @tool
    def alphahuman_insert_memory(
        title: str,
        content: str,
        namespace: str,
        source_type: str = "doc",
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Insert a document into Alphahuman Memory.

        Args:
            title: Document title.
            content: Document content.
            namespace: Namespace (required).
            source_type: One of doc, chat, email. Default doc.
            metadata: Optional metadata dict.
        """
        return client.insert_memory(
            title=title,
            content=content,
            namespace=namespace,
            source_type=source_type,
            metadata=metadata,
        )

    @tool
    def alphahuman_query_memory(
        query: str,
        namespace: Optional[str] = None,
        max_chunks: Optional[int] = None,
    ) -> dict[str, Any]:
        """Query Alphahuman Memory via RAG.

        Args:
            query: Query string (required).
            namespace: Optional namespace.
            max_chunks: Optional limit 1-200.
        """
        return client.query_memory(
            query=query,
            namespace=namespace,
            max_chunks=max_chunks,
        )

    @tool
    def alphahuman_delete_memory(namespace: Optional[str] = None) -> dict[str, Any]:
        """Delete memory (admin). Optionally scoped by namespace."""
        return client.delete_memory(namespace=namespace)

    @tool
    def alphahuman_recall_memory(
        namespace: Optional[str] = None,
        max_chunks: Optional[int] = None,
    ) -> dict[str, Any]:
        """Recall context from Alphahuman Master node.

        Args:
            namespace: Optional namespace.
            max_chunks: Optional positive integer.
        """
        return client.recall_memory(namespace=namespace, max_chunks=max_chunks)

    @tool
    def alphahuman_recall_memories(
        namespace: Optional[str] = None,
        top_k: Optional[int] = None,
        min_retention: Optional[float] = None,
    ) -> dict[str, Any]:
        """Recall memories from Ebbinghaus bank.

        Args:
            namespace: Optional namespace.
            top_k: Optional positive number.
            min_retention: Optional non-negative number.
        """
        return client.recall_memories(
            namespace=namespace,
            top_k=top_k,
            min_retention=min_retention,
        )

    return [
        alphahuman_insert_memory,
        alphahuman_query_memory,
        alphahuman_delete_memory,
        alphahuman_recall_memory,
        alphahuman_recall_memories,
    ]


def get_tools() -> list[Any]:
    """Return memory tools from environment (ALPHAHUMAN_API_KEY, optional ALPHAHUMAN_BASE_URL)."""
    token = os.environ.get(_TOKEN_ENV, "")
    if not token:
        raise ValueError(
            f"Set {_TOKEN_ENV} or use make_memory_tools(token=...)"
        )
    base_url = os.environ.get(_BASE_URL_ENV) or None
    return make_memory_tools(token=token, base_url=base_url)
