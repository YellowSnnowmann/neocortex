# Choosing an SDK

Neocortex offers SDKs and integrations across multiple languages and frameworks.

## SDKs

| SDK | Language | Install | Description |
| --- | --- | --- | --- |
| **TinyHumans SDK** | Python | `pip install tinyhumansai` | Cloud API — managed memory layer, no infra needed |
| **Neocortex GraphRAG** | Python | `pip install neocortex` | Local GraphRAG — full control over the knowledge graph |
| **TinyHumans TypeScript SDK** | TypeScript | `npm install tinyhumansai` | Cloud API for Node.js and browser environments |
| **TinyHumans Rust SDK** | Rust | `cargo add tinyhumansai` | Cloud API for Rust applications |

## Integrations

| Integration | Description |
| --- | --- |
| **LangGraph SDK** | Drop-in memory layer for LangGraph agent workflows |
| **OpenClaw Plugin** | Plugin for the OpenClaw agent framework |

## Which should I pick?

**Choose TinyHumans SDK (Python / TypeScript / Rust) if you want:**
- A managed service with no infrastructure to maintain
- Simple key-value memory storage with namespaces
- Built-in LLM recall (OpenAI, Anthropic, Gemini)
- The fastest path to production

**Choose Neocortex GraphRAG if you want:**
- Full control over the knowledge graph
- To inspect extracted entities, relations, and chunks
- To run everything locally
- Custom query tuning and retrieval pipelines

**Choose an integration (LangGraph / OpenClaw) if you want:**
- To add Neocortex memory to an existing agent framework
- Minimal code changes to your current setup

## Prerequisites

- A [TinyHumans API key](api-key.md) (for all cloud SDKs and integrations)
- **Neocortex GraphRAG** additionally requires an OpenAI API key
