/*
Comprehensive SDK route example for @tinyhumansai/neocortex.

Usage:
  cd packages/sdk-typescript
  npm install
  npm run build
  TINYHUMANS_TOKEN=... node example.mjs

Optional env vars:
  TINYHUMANS_BASE_URL / NEOCORTEX_BASE_URL
*/

import { TinyHumanMemoryClient } from './dist/index.js';

const token = process.env.TINYHUMANS_TOKEN ?? process.env.NEOCORTEX_TOKEN;
if (!token) {
  console.error('Set TINYHUMANS_TOKEN (or NEOCORTEX_TOKEN) to run this example.');
  process.exit(1);
}

const baseUrl = process.env.TINYHUMANS_BASE_URL ?? process.env.NEOCORTEX_BASE_URL;
const client = new TinyHumanMemoryClient({ token, baseUrl });

const ts = Date.now();
const namespace = `sdk-ts-example-${ts}`;
const singleDocId = `ts-doc-single-${ts}`;
const batchDocA = `ts-doc-batch-a-${ts}`;
const batchDocB = `ts-doc-batch-b-${ts}`;

function unwrapData(payload) {
  return payload?.data ?? {};
}

async function runStep(name, fn, optional = false) {
  try {
    const res = await fn();
    console.log(`[ok] ${name}`);
    return res;
  } catch (err) {
    if (optional) {
      console.log(`[skip] ${name}: ${err.message}`);
      return null;
    }
    throw err;
  }
}

let insertJobId;

const insertMemoryRes = await runStep('insertMemory', () =>
  client.insertMemory({
    title: 'TS example memory',
    content: 'TypeScript SDK inserted this core memory.',
    namespace,
    metadata: { source: 'sdk-typescript-example' },
    documentId: `${singleDocId}-memory`,
  })
);
insertJobId = unwrapData(insertMemoryRes).jobId;

await runStep('queryMemory', () =>
  client.queryMemory({
    query: 'What did the TypeScript example store?',
    namespace,
    includeReferences: true,
    maxChunks: 5,
  })
);

await runStep('recallMemory', () =>
  client.recallMemory({ namespace, maxChunks: 5 })
);

await runStep('recallMemories', () =>
  client.recallMemories({ namespace, topK: 5, minRetention: 0 })
);

await runStep('chatMemory', () =>
  client.chatMemory({
    messages: [{ role: 'user', content: 'Summarize the memory context.' }],
    temperature: 0,
    maxTokens: 128,
  })
);

await runStep('interactMemory', () =>
  client.interactMemory({
    namespace,
    entityNames: ['TS_ENTITY_A', 'TS_ENTITY_B'],
    description: 'Core interactions route',
    interactionLevel: 'engage',
    timestamp: Math.floor(Date.now() / 1000),
  })
);

await runStep('recallThoughts', () =>
  client.recallThoughts({ namespace, maxChunks: 5, persist: false })
);

const singleDocRes = await runStep('insertDocument', () =>
  client.insertDocument({
    title: 'TS single document',
    content: 'Single document inserted through /memory/documents.',
    namespace,
    documentId: singleDocId,
  })
);
const singleDocJobId = unwrapData(singleDocRes).jobId;

const batchRes = await runStep('insertDocumentsBatch', () =>
  client.insertDocumentsBatch({
    items: [
      {
        title: 'TS batch doc A',
        content: 'Batch doc A',
        namespace,
        documentId: batchDocA,
      },
      {
        title: 'TS batch doc B',
        content: 'Batch doc B',
        namespace,
        documentId: batchDocB,
      },
    ],
  })
);

const accepted = unwrapData(batchRes).accepted;
const acceptedJobId = Array.isArray(accepted) && accepted.length > 0 ? accepted[0]?.jobId : undefined;

const jobId = singleDocJobId ?? acceptedJobId ?? insertJobId;
if (jobId) {
  await runStep('getIngestionJob', () => client.getIngestionJob(jobId));
  await runStep('waitForIngestionJob', () =>
    client.waitForIngestionJob(jobId, { timeoutMs: 30_000, pollIntervalMs: 1_000 })
  );
} else {
  console.log('[skip] getIngestionJob/waitForIngestionJob: no jobId returned by backend');
}

await runStep('listDocuments', () =>
  client.listDocuments({ namespace, limit: 10, offset: 0 })
);

await runStep('getDocument', () =>
  client.getDocument({ documentId: singleDocId, namespace })
);

await runStep('queryMemoryContext', () =>
  client.queryMemoryContext({
    query: 'What content is in the TS docs namespace?',
    namespace,
    includeReferences: true,
    maxChunks: 5,
    documentIds: [singleDocId],
  })
);

await runStep('chatMemoryContext', () =>
  client.chatMemoryContext({
    messages: [{ role: 'user', content: 'Summarize stored documents.' }],
    temperature: 0,
    maxTokens: 128,
  })
);

await runStep('recordInteractions', () =>
  client.recordInteractions({
    namespace,
    entityNames: ['TS_ENTITY_A', 'TS_ENTITY_B'],
    description: 'Mirrored interactions route',
    interactionLevels: ['view', 'read'],
    timestamp: Math.floor(Date.now() / 1000),
  })
);

await runStep('getGraphSnapshot', () =>
  client.getGraphSnapshot({ namespace, mode: 'latest_chunks', limit: 10, seed_limit: 3 }),
  true
);

await runStep('deleteDocument(single)', () =>
  client.deleteDocument({ documentId: singleDocId, namespace })
);
await runStep('deleteDocument(batch A)', () =>
  client.deleteDocument({ documentId: batchDocA, namespace })
);
await runStep('deleteDocument(batch B)', () =>
  client.deleteDocument({ documentId: batchDocB, namespace })
);

await runStep('deleteMemory', () =>
  client.deleteMemory({ namespace })
);

console.log('\nTypeScript example completed.');
