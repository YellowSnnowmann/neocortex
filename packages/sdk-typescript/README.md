# @alphahuman/memory-sdk

TypeScript / JavaScript SDK for the [Alphahuman Memory API](https://alphahuman.xyz).

## Requirements

- Node.js ≥ 18 (uses native `fetch`)

## Install

```bash
npm install @alphahuman/memory-sdk
```

## Quick start

```typescript
import { AlphahumanMemoryClient } from '@alphahuman/memory-sdk';

const client = new AlphahumanMemoryClient({ token: 'your-api-key' });

// Ingest (upsert) memory
const ingestResult = await client.ingestMemory({
  items: [
    {
      key: 'user-preference-theme',
      content: 'User prefers dark mode',
      namespace: 'preferences',
      metadata: { source: 'onboarding' },
    },
  ],
});
console.log(ingestResult.data); // { ingested: 1, updated: 0, errors: 0 }

// Read memory
const readResult = await client.readMemory({ namespace: 'preferences' });
console.log(readResult.data.items);

// Delete by key
await client.deleteMemory({ key: 'user-preference-theme', namespace: 'preferences' });

// Delete all user memory
await client.deleteMemory({ deleteAll: true });
```

## API reference

### `new AlphahumanMemoryClient(config)`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `config.token` | `string` | ✓ | JWT or API key |
| `config.baseUrl` | `string` | | Override API URL. If not set, uses `ALPHAHUMAN_BASE_URL` env (e.g. from `.env`) or default `https://staging-api.alphahuman.xyz` |

### `client.ingestMemory(request)`

Upserts memory items. Items are deduplicated by `(namespace, key)`. If a
matching item already exists, its `content` and `metadata` are updated.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `items` | `MemoryItem[]` | ✓ | One or more items to ingest |

Returns `IngestMemoryResponse` with `{ ingested, updated, errors }` counts.

### `client.readMemory(request?)`

Read memory items. All filter fields are optional; omitting all returns
every item for the authenticated user.

| Field | Type | Description |
|-------|------|-------------|
| `key` | `string` | Exact key match |
| `keys` | `string[]` | Match any of the given keys |
| `namespace` | `string` | Scope to a namespace |

Returns `ReadMemoryResponse` with `{ items, count }`.

### `client.deleteMemory(request)`

Delete memory. At least one of `key`, `keys`, or `deleteAll` must be set.

| Field | Type | Description |
|-------|------|-------------|
| `key` | `string` | Delete a single key |
| `keys` | `string[]` | Delete multiple keys |
| `namespace` | `string` | Scope deletion to a namespace |
| `deleteAll` | `boolean` | Delete all user memory |

Returns `DeleteMemoryResponse` with `{ deleted }` count.

## Error handling

All API errors throw `AlphahumanError` which extends `Error` and includes
`status` (HTTP status code) and `body` (parsed response, if available).

```typescript
import { AlphahumanError } from '@alphahuman/memory-sdk';

try {
  await client.readMemory();
} catch (err) {
  if (err instanceof AlphahumanError) {
    console.error(err.status, err.message);
  }
}
```
