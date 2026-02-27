"""Base classes and shared constants for method adapters."""

import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

# Ensure repo root is on path so "neocortex" is importable
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
  sys.path.insert(0, str(_REPO_ROOT))


@dataclass
class QueryResult:
  """Result from a single query."""

  answer: str = ""
  contexts: list[str] = field(default_factory=list)
  latency_seconds: float = 0.0
  tokens_input: int = 0
  tokens_output: int = 0
  cost_usd: float = 0.0


@dataclass
class IndexResult:
  """Result from indexing."""

  time_seconds: float = 0.0
  cost_usd: float = 0.0
  tokens_input: int = 0
  tokens_output: int = 0


class MethodAdapter(ABC):
  """Abstract base class for RAG method adapters."""

  name: str = ""

  @abstractmethod
  async def create_index(self, chunks: list[str], working_dir: str, config: dict) -> IndexResult:
    """Index corpus chunks. Returns indexing metrics."""

  @abstractmethod
  async def query(self, question: str, config: dict) -> QueryResult:
    """Query the method. Returns answer, contexts, and metrics."""

  @abstractmethod
  async def load_index(self, working_dir: str, config: dict) -> None:
    """Load an existing index from working_dir."""


# --- Sherlock Holmes domain config for graph-based methods ---

SHERLOCK_DOMAIN = (
  "Analyse the following passage from the Sherlock Holmes stories and identify "
  "the people, places, objects, and events mentioned in it. Your goal is to create "
  "an RDF (Resource Description Framework) graph from the given text. "
  "Pay attention to the spelling of character names and locations."
)

SHERLOCK_QUERIES = [
  "What disguise did Holmes use in A Scandal in Bohemia?",
  "How did Holmes deduce the identity of the King of Bohemia?",
  "What was the Red-Headed League and why was it dissolved?",
  "How did Holmes solve the mystery of the Speckled Band?",
]

SHERLOCK_ENTITY_TYPES = [
  "person",
  "location",
  "object",
  "event",
  "organization",
  "animal",
]


def _get_cost_tracker():
  """Import and return ExternalCostTracker from the benchmarks directory."""
  benchmarks_dir = os.path.join(_REPO_ROOT, "benchmarks")
  if benchmarks_dir not in sys.path:
    sys.path.insert(0, benchmarks_dir)
  from _cost_tracker import ExternalCostTracker

  return ExternalCostTracker()
