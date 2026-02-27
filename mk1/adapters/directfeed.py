"""DirectFeed adapter — no indexing, full context window."""

import os
import sys
import time

from ._base import _REPO_ROOT, IndexResult, MethodAdapter, QueryResult


class DirectFeedAdapter(MethodAdapter):
  """Adapter for the DirectFeed RAG implementation."""

  name = "directfeed"

  def __init__(self):
    """Initialize the DirectFeed adapter."""
    self._context_str = ""
    self._chunks = []

  async def create_index(self, chunks: list[str], working_dir: str, config: dict) -> IndexResult:
    """Prepare a giant context window by concatenating all chunks."""
    self._chunks = chunks
    self._context_str = "\n\n---\n\n".join(chunks)
    return IndexResult(time_seconds=0.0, cost_usd=0.0, tokens_input=0, tokens_output=0)

  async def load_index(self, working_dir: str, config: dict) -> None:
    """DirectFeed has no persisted index to load."""
    pass

  async def query(self, question: str, config: dict) -> QueryResult:
    """Send the full concatenated context to an OpenAI model and return the answer."""
    from openai import AsyncOpenAI

    model = config.get("openai_model", "gpt-4o-mini")
    system = (
      "You are a helpful assistant. Below is a collection of reference passages. "
      "Use them to answer the user's question accurately and concisely. "
      "If the answer cannot be found in the passages, say so.\n\n"
      f"# REFERENCE PASSAGES\n{self._context_str}"
    )

    client = AsyncOpenAI()
    start = time.perf_counter()
    response = await client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": question},
      ],
    )
    elapsed = time.perf_counter() - start

    answer_text = response.choices[0].message.content or ""
    usage = response.usage
    inp = usage.prompt_tokens if usage else 0
    out = usage.completion_tokens if usage else 0

    benchmarks_dir = os.path.join(_REPO_ROOT, "benchmarks")
    if benchmarks_dir not in sys.path:
      sys.path.insert(0, benchmarks_dir)
    from _cost_tracker import _get_pricing

    pricing = _get_pricing(model)
    cost = inp * pricing["input"] / 1_000_000 + out * pricing["output"] / 1_000_000

    return QueryResult(
      answer=answer_text,
      contexts=self._chunks[: config.get("top_k", 8)],
      latency_seconds=elapsed,
      tokens_input=inp,
      tokens_output=out,
      cost_usd=cost,
    )
