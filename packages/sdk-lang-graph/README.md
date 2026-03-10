# alphahuman-langgraph

LangGraph integration for the [Alphahuman Memory API](https://alphahuman.xyz), aligned with the backend API: insert, query, admin/delete, recall, and memories/recall.

## Requirements

- Python ≥ 3.9
- `httpx >= 0.25`
- `langgraph >= 0.2`
- `langchain-core >= 0.3`

## Install

```bash
pip install alphahuman-langgraph
# or, if pip is not in PATH:
python3 -m pip install alphahuman-langgraph
```

## Usage — factory pattern (recommended)

Use `make_memory_tools` to create tools with credentials baked in. Credentials are **not** exposed to the LLM as tool parameters.

```python
from langchain_openai import ChatOpenAI
from alphahuman_langgraph import make_memory_tools

tools = make_memory_tools(token="your-api-key")
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)
```

## Usage — environment variables

Set `ALPHAHUMAN_API_KEY` (required) and optionally `ALPHAHUMAN_BASE_URL`, then call `get_tools()`:

```bash
export ALPHAHUMAN_API_KEY="your-api-key"
```

```python
from alphahuman_langgraph import get_tools
tools = get_tools()
```

## Available tools

| Tool | Description |
|------|-------------|
| `alphahuman_insert_memory` | Insert a document (title, content, namespace) |
| `alphahuman_query_memory` | Query memory via RAG (query, namespace?, max_chunks?) |
| `alphahuman_delete_memory` | Delete memory – optional namespace scope |
| `alphahuman_recall_memory` | Recall context from Master node |
| `alphahuman_recall_memories` | Recall memories from Ebbinghaus bank |

## Error handling

The client raises `AlphahumanError` (from `alphahuman_langgraph.client`) on API failures and `ValueError` on invalid input. These propagate through LangChain/LangGraph.

## Tests

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest tests/ -v
```
