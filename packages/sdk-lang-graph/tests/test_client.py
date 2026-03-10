"""Tests for AlphahumanMemoryClient (aligned with backend API)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from alphahuman_langgraph.client import (
    AlphahumanError,
    AlphahumanMemoryClient,
)


@pytest.fixture
def mock_httpx_client():
    """Mock httpx.Client to avoid real HTTP calls."""
    with patch("alphahuman_langgraph.client.httpx.Client") as mock_cls:
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance
        mock_instance.__enter__ = MagicMock(return_value=mock_instance)
        mock_instance.__exit__ = MagicMock(return_value=None)
        yield mock_instance


def test_client_requires_token():
    with pytest.raises(ValueError, match="token is required"):
        AlphahumanMemoryClient(token="")
    with pytest.raises(ValueError, match="token is required"):
        AlphahumanMemoryClient(token="   ")


def test_insert_memory_validates_required(mock_httpx_client):
    mock_httpx_client.request.return_value = MagicMock(
        status_code=200,
        is_success=True,
        json=lambda: {"success": True, "data": {"status": "ok", "stats": {}}},
    )
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")

    with pytest.raises(ValueError, match="title is required"):
        client.insert_memory(title="", content="c", namespace="ns")
    with pytest.raises(ValueError, match="content is required"):
        client.insert_memory(title="t", content="", namespace="ns")
    with pytest.raises(ValueError, match="namespace is required"):
        client.insert_memory(title="t", content="c", namespace="")


def test_insert_memory_posts_correctly(mock_httpx_client):
    mock_httpx_client.request.return_value = MagicMock(
        status_code=200,
        is_success=True,
        json=lambda: {"success": True, "data": {"status": "ok", "stats": {}}},
    )
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")
    result = client.insert_memory(
        title="Doc",
        content="Content",
        namespace="default",
        source_type="doc",
        metadata={"k": "v"},
    )
    assert result == {"status": "ok", "stats": {}}
    mock_httpx_client.request.assert_called_once()
    call_args = mock_httpx_client.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "/v1/memory/insert"
    body = call_args[1]["json"]
    assert body["title"] == "Doc"
    assert body["content"] == "Content"
    assert body["namespace"] == "default"
    assert body["sourceType"] == "doc"
    assert body["metadata"] == {"k": "v"}


def test_query_memory_validates_query(mock_httpx_client):
    mock_httpx_client.request.return_value = MagicMock(
        status_code=200,
        is_success=True,
        json=lambda: {"success": True, "data": {"cached": False}},
    )
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")
    with pytest.raises(ValueError, match="query is required"):
        client.query_memory(query="")


def test_query_memory_validates_max_chunks(mock_httpx_client):
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")
    with pytest.raises(ValueError, match="maxChunks"):
        client.query_memory(query="q", max_chunks=0)
    with pytest.raises(ValueError, match="maxChunks"):
        client.query_memory(query="q", max_chunks=201)


def test_query_memory_posts_correctly(mock_httpx_client):
    mock_httpx_client.request.return_value = MagicMock(
        status_code=200,
        is_success=True,
        json=lambda: {"success": True, "data": {"cached": False, "response": "ctx"}},
    )
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")
    result = client.query_memory(query="hello", namespace="ns", max_chunks=10)
    assert result["cached"] is False
    assert result["response"] == "ctx"
    call_args = mock_httpx_client.request.call_args
    assert call_args[0][1] == "/v1/memory/query"
    assert call_args[1]["json"]["query"] == "hello"
    assert call_args[1]["json"]["namespace"] == "ns"
    assert call_args[1]["json"]["maxChunks"] == 10


def test_delete_memory_posts_correctly(mock_httpx_client):
    mock_httpx_client.request.return_value = MagicMock(
        status_code=200,
        is_success=True,
        json=lambda: {
            "success": True,
            "data": {"status": "ok", "userId": "u1", "nodesDeleted": 5, "message": "Done"},
        },
    )
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")
    result = client.delete_memory(namespace="my-ns")
    assert result["nodesDeleted"] == 5
    call_args = mock_httpx_client.request.call_args
    assert call_args[0][1] == "/v1/memory/admin/delete"
    assert call_args[1]["json"]["namespace"] == "my-ns"


def test_recall_memory_posts_correctly(mock_httpx_client):
    mock_httpx_client.request.return_value = MagicMock(
        status_code=200,
        is_success=True,
        json=lambda: {"success": True, "data": {"cached": False, "response": "ctx"}},
    )
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")
    result = client.recall_memory(namespace="ns", max_chunks=10)
    assert result["response"] == "ctx"
    call_args = mock_httpx_client.request.call_args
    assert call_args[0][1] == "/v1/memory/recall"


def test_recall_memories_posts_correctly(mock_httpx_client):
    mock_httpx_client.request.return_value = MagicMock(
        status_code=200,
        is_success=True,
        json=lambda: {"success": True, "data": {"memories": []}},
    )
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")
    result = client.recall_memories(namespace="ns", top_k=5)
    assert result["memories"] == []
    call_args = mock_httpx_client.request.call_args
    assert call_args[0][1] == "/v1/memory/memories/recall"


def test_client_raises_alphahuman_error_on_failure(mock_httpx_client):
    mock_httpx_client.request.return_value = MagicMock(
        status_code=400,
        is_success=False,
        json=lambda: {"success": False, "error": "Bad request"},
    )
    client = AlphahumanMemoryClient(token="test", base_url="https://api.test")
    with pytest.raises(AlphahumanError) as exc_info:
        client.insert_memory(title="t", content="c", namespace="ns")
    assert exc_info.value.status == 400
    assert "Bad request" in str(exc_info.value)
    assert exc_info.value.body == {"success": False, "error": "Bad request"}
