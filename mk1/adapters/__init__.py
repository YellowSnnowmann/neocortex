"""Method adapters package.

Each adapter wraps a RAG method, providing a uniform interface for indexing,
loading, and querying. All adapters receive the shared config dict.

Adapter imports are lazy so that only the dependencies for the requested
method need to be installed.
"""

from ._base import IndexResult, MethodAdapter, QueryResult

# Maps method name → (module_name, class_name) for lazy importing.
_ADAPTER_REGISTRY: dict[str, tuple[str, str]] = {
  "neocortex": (".neocortex", "NeocortexAdapter"),
  "neocortex_v1": (".neocortex_v1", "NeocortexV1Adapter"),
  "vdb": (".vdb", "VDBAdapter"),
  "directfeed": (".directfeed", "DirectFeedAdapter"),
  "lightrag": (".lightrag_adapter", "LightRAGAdapter"),
  "fast_graphrag": (".fast_graphrag_adapter", "FastGraphRAGAdapter"),
  "nano_graphrag": (".nano_graphrag", "NanoGraphRAGAdapter"),
  "graphrag": (".graphrag", "GraphRAGAdapter"),
  "cognee": (".cognee", "CogneeAdapter"),
  "gpt52_vdb": (".gpt52_vdb", "GPT52VDBAdapter"),
  "gemini_vdb": (".gemini_vdb", "GeminiVDBAdapter"),
}

ADAPTER_NAMES: list[str] = list(_ADAPTER_REGISTRY.keys())


def get_adapter(name: str) -> MethodAdapter:
  """Get an adapter instance by name (lazy-imports the adapter module)."""
  entry = _ADAPTER_REGISTRY.get(name)
  if entry is None:
    raise ValueError(f"Unknown method: {name}. Available: {ADAPTER_NAMES}")
  module_path, class_name = entry
  import importlib

  mod = importlib.import_module(module_path, package=__name__)
  cls = getattr(mod, class_name)
  return cls()


__all__ = [
  "ADAPTER_NAMES",
  "get_adapter",
  "IndexResult",
  "MethodAdapter",
  "QueryResult",
]
