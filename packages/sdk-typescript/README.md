# @tinyhumansai/neocortex

TypeScript / JavaScript SDK for the TinyHumans Neocortex memory API.

## Requirements

- Node.js 18+
- Native `fetch` runtime (Node 18+ already includes it)

## Install

```bash
npm install @tinyhumansai/neocortex
```

## Get an API key

1. Sign in to your TinyHumans account.
2. Create a server API key in the TinyHumans dashboard.
3. Export it before running examples:

```bash
export TINYHUMANS_TOKEN="your_api_key"
# optional custom API base URL
export TINYHUMANS_BASE_URL="https://api.tinyhumans.ai"
```

`TINYHUMANS_TOKEN` is also accepted in examples as an alias.

## Quick start

```ts
import { TinyHumanMemoryClient } from '@tinyhumansai/neocortex';

const client = new TinyHumanMemoryClient({
  token: process.env.TINYHUMANS_TOKEN!,
});

await client.insertMemory({
  title: 'User preference',
  content: 'User prefers dark mode',
  namespace: 'preferences',
});

const query = await client.queryMemory({
  query: 'What does the user prefer?',
  namespace: 'preferences',
  maxChunks: 10,
});

console.log(query.data.response);
```

## Full route example

A comprehensive example that exercises all SDK methods is available at `example.mjs`.

```bash
cd packages/sdk-typescript
npm install
npm run build
TINYHUMANS_TOKEN=your_api_key node example.mjs
```

## Client config

```ts
new TinyHumanMemoryClient({
  token: 'required',
  baseUrl: 'optional',
});
```

`baseUrl` resolution order: explicit config -> `TINYHUMANS_BASE_URL`/`TINYHUMANS_BASE_URL` env -> `https://api.tinyhumans.ai`.

## Methods

Core:
- `insertMemory`
- `queryMemory`
- `chatMemory`
- `deleteMemory`
- `interactMemory`
- `recallMemory`
- `recallMemories`
- `recallThoughts`

Ingestion jobs:
- `getIngestionJob`
- `waitForIngestionJob`

Documents and mirrored routes:
- `insertDocument`
- `insertDocumentsBatch`
- `listDocuments`
- `getDocument`
- `deleteDocument`
- `getGraphSnapshot`
- `queryMemoryContext`
- `chatMemoryContext`
- `recordInteractions`

## Error handling

Non-2xx responses throw `TinyHumanError`:

```ts
import { TinyHumanError } from '@tinyhumansai/neocortex';

try {
  await client.queryMemory({ query: 'hello' });
} catch (err) {
  if (err instanceof TinyHumanError) {
    console.error(err.status, err.message, err.body);
  }
}
```
