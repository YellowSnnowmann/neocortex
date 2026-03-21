# tinyhumansai (Python SDK)

Python SDK for TinyHumans Neocortex memory APIs.

## Requirements

- Python 3.9+

## Install

```bash
pip install tinyhumansai
```

For local development from this repo:

```bash
cd packages/sdk-python
uv sync --group dev
```

## Get an API key

1. Sign in to your TinyHumans account.
2. Create a server API key in the TinyHumans dashboard.
3. Export it before running examples:

```bash
export TINYHUMANS_TOKEN="your_api_key"
# aliases used by examples/backends
export TINYHUMANS_TOKEN="your_api_key"
# optional model id and base URL overrides
export TINYHUMANS_MODEL_ID="neocortex-mk1"
export TINYHUMANS_BASE_URL="https://api.tinyhumans.ai"
```

## Quick start

```python
import tinyhumansai as api

client = api.TinyHumansMemoryClient(token="YOUR_API_KEY")

client.ingest_memory(
    item={
        "key": "user-preference-theme",
        "content": "User prefers dark mode",
        "namespace": "preferences",
    }
)

ctx = client.recall_memory(
    namespace="preferences",
    prompt="What does the user prefer?",
    num_chunks=10,
)

print(ctx.context)
```

## Full route example

`example.py` is the comprehensive SDK example and exercises all current client methods, including core, documents, mirrored routes, ingestion job polling, and cleanup.

```bash
cd packages/sdk-python
python example.py
```

## Client config

```python
client = api.TinyHumansMemoryClient(
    token="required",
    model_id="neocortex-mk1",  # optional
    base_url="https://...",    # optional
)
```

Base URL resolution: explicit arg -> `TINYHUMANS_BASE_URL` -> SDK default.

## Implemented methods

Core methods:
- `ingest_memory`
- `ingest_memories`
- `recall_memory`
- `delete_memory`
- `recall_with_llm`
- `chat_memory`
- `interact_memory`
- `recall_memory_master`
- `recall_memories`

Documents and mirrored routes:
- `insert_document`
- `insert_documents_batch`
- `list_documents`
- `get_document`
- `delete_document`
- `get_graph_snapshot`
- `query_memory_context`
- `chat_memory_context`
- `record_interactions`
- `recall_thoughts`

Ingestion jobs:
- `get_ingestion_job`
- `wait_for_ingestion_job`

## LLM helper providers

`recall_with_llm` supports:
- OpenAI
- Anthropic
- Google (Gemini)
- Custom OpenAI-compatible URL

## Error handling

API errors raise `TinyHumansError` with `message`, `status`, and `body`.
