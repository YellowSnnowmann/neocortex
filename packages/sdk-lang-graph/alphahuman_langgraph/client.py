"""HTTP client for the AlphaHuman Memory API (aligned with backend-alphahuman)."""

from __future__ import annotations

from typing import Any, Optional

import httpx

DEFAULT_BASE_URL = "https://staging-api.alphahuman.xyz"
BASE_URL_ENV = "ALPHAHUMAN_BASE_URL"


class AlphahumanError(Exception):
    """Raised on API errors."""

    def __init__(self, message: str, status: int, body: Any = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class AlphahumanMemoryClient:
    """Client for the AlphaHuman Memory API: insert, query, delete, recall."""

    def __init__(
        self,
        token: str,
        base_url: Optional[str] = None,
    ) -> None:
        if not token or not token.strip():
            raise ValueError("token is required")
        import os
        resolved = base_url or os.environ.get(BASE_URL_ENV) or DEFAULT_BASE_URL
        self._base_url = resolved.rstrip("/")
        self._token = token
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "AlphahumanMemoryClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _request(self, method: str, path: str, json: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        resp = self._client.request(method, path, json=json or {})
        try:
            data = resp.json()
        except Exception:
            raise AlphahumanError(
                f"HTTP {resp.status_code}: non-JSON response",
                resp.status_code,
                resp.text,
            )
        if not resp.is_success:
            msg = data.get("error", f"HTTP {resp.status_code}")
            raise AlphahumanError(msg, resp.status_code, data)
        return data

    def insert_memory(
        self,
        *,
        title: str,
        content: str,
        namespace: str,
        source_type: str = "doc",
        metadata: Optional[dict[str, Any]] = None,
        priority: Optional[str] = None,
        created_at: Optional[float] = None,
        updated_at: Optional[float] = None,
        document_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """POST /v1/memory/insert"""
        if not title or not isinstance(title, str):
            raise ValueError("title is required and must be a string")
        if not content or not isinstance(content, str):
            raise ValueError("content is required and must be a string")
        if not namespace or not isinstance(namespace, str):
            raise ValueError("namespace is required and must be a string")
        body: dict[str, Any] = {
            "title": title,
            "content": content,
            "namespace": namespace,
            "sourceType": source_type,
            "metadata": metadata or {},
        }
        if priority is not None:
            body["priority"] = priority
        if created_at is not None:
            body["createdAt"] = created_at
        if updated_at is not None:
            body["updatedAt"] = updated_at
        if document_id is not None:
            body["documentId"] = document_id
        out = self._request("POST", "/v1/memory/insert", body)
        return out.get("data", {})

    def query_memory(
        self,
        *,
        query: str,
        include_references: Optional[bool] = None,
        namespace: Optional[str] = None,
        max_chunks: Optional[int] = None,
        document_ids: Optional[list[str]] = None,
        llm_query: Optional[str] = None,
    ) -> dict[str, Any]:
        """POST /v1/memory/query"""
        if not query or not isinstance(query, str):
            raise ValueError("query is required and must be a string")
        if max_chunks is not None and (not isinstance(max_chunks, int) or max_chunks < 1 or max_chunks > 200):
            raise ValueError("maxChunks must be between 1 and 200")
        body: dict[str, Any] = {"query": query}
        if include_references is not None:
            body["includeReferences"] = include_references
        if namespace is not None:
            body["namespace"] = namespace
        if max_chunks is not None:
            body["maxChunks"] = max_chunks
        if document_ids is not None:
            body["documentIds"] = document_ids
        if llm_query is not None:
            body["llmQuery"] = llm_query
        out = self._request("POST", "/v1/memory/query", body)
        return out.get("data", {})

    def delete_memory(self, *, namespace: Optional[str] = None) -> dict[str, Any]:
        """POST /v1/memory/admin/delete"""
        body: dict[str, Any] = {}
        if namespace is not None:
            body["namespace"] = namespace
        out = self._request("POST", "/v1/memory/admin/delete", body)
        return out.get("data", {})

    def recall_memory(
        self,
        *,
        namespace: Optional[str] = None,
        max_chunks: Optional[int] = None,
    ) -> dict[str, Any]:
        """POST /v1/memory/recall"""
        if max_chunks is not None and (not isinstance(max_chunks, int) or max_chunks <= 0):
            raise ValueError("maxChunks must be a positive integer")
        body: dict[str, Any] = {}
        if namespace is not None:
            body["namespace"] = namespace
        if max_chunks is not None:
            body["maxChunks"] = max_chunks
        out = self._request("POST", "/v1/memory/recall", body)
        return out.get("data", {})

    def recall_memories(
        self,
        *,
        namespace: Optional[str] = None,
        top_k: Optional[int] = None,
        min_retention: Optional[float] = None,
        as_of: Optional[float] = None,
    ) -> dict[str, Any]:
        """POST /v1/memory/memories/recall"""
        if top_k is not None and (not isinstance(top_k, (int, float)) or top_k <= 0):
            raise ValueError("topK must be a positive number")
        if min_retention is not None and (not isinstance(min_retention, (int, float)) or min_retention < 0):
            raise ValueError("minRetention must be a non-negative number")
        body: dict[str, Any] = {}
        if namespace is not None:
            body["namespace"] = namespace
        if top_k is not None:
            body["topK"] = top_k
        if min_retention is not None:
            body["minRetention"] = min_retention
        if as_of is not None:
            body["asOf"] = as_of
        out = self._request("POST", "/v1/memory/memories/recall", body)
        return out.get("data", {})
