"""Tests for make_memory_tools and get_tools."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from alphahuman_langgraph.tools import get_tools, make_memory_tools


def test_make_memory_tools_returns_five_tools():
    with patch("alphahuman_langgraph.tools.AlphahumanMemoryClient"):
        tools = make_memory_tools(token="test")
    assert len(tools) == 5
    names = [t.name for t in tools]
    assert "alphahuman_insert_memory" in names
    assert "alphahuman_query_memory" in names
    assert "alphahuman_delete_memory" in names
    assert "alphahuman_recall_memory" in names
    assert "alphahuman_recall_memories" in names


def test_insert_tool_invokes_client():
    with patch("alphahuman_langgraph.tools.AlphahumanMemoryClient") as mock_cls:
        mock_client = MagicMock()
        mock_client.insert_memory.return_value = {"status": "ok", "stats": {}}
        mock_cls.return_value = mock_client
        tools = make_memory_tools(token="test")
    insert_tool = next(t for t in tools if t.name == "alphahuman_insert_memory")
    result = insert_tool.invoke({
        "title": "T",
        "content": "C",
        "namespace": "ns",
    })
    assert result == {"status": "ok", "stats": {}}
    mock_client.insert_memory.assert_called_once_with(
        title="T",
        content="C",
        namespace="ns",
        source_type="doc",
        metadata=None,
    )


def test_get_tools_requires_env():
    import os
    old = os.environ.pop("ALPHAHUMAN_API_KEY", None)
    try:
        with pytest.raises(ValueError, match="ALPHAHUMAN_API_KEY"):
            get_tools()
    finally:
        if old is not None:
            os.environ["ALPHAHUMAN_API_KEY"] = old


def test_get_tools_uses_env():
    with patch.dict("os.environ", {"ALPHAHUMAN_API_KEY": "secret"}):
        with patch("alphahuman_langgraph.tools.make_memory_tools") as mock_make:
            mock_make.return_value = []
            get_tools()
            mock_make.assert_called_once_with(token="secret", base_url=None)
