// Alphahuman Memory SDK for TypeScript
// Provides ingestMemory(), readMemory(), and deleteMemory() for the Alphahuman Memory API.

const DEFAULT_BASE_URL = 'https://staging-api.alphahuman.xyz';

/** Resolve ALPHAHUMAN_BASE_URL from env when available (e.g. Node). No @types/node required. */
function getEnvBaseUrl(): string | undefined {
  try {
    const g = typeof globalThis !== 'undefined' ? globalThis : (undefined as unknown as Record<string, unknown>);
    const env = (g as { process?: { env?: Record<string, string | undefined> } })?.process?.env;
    return env?.ALPHAHUMAN_BASE_URL;
  } catch {
    return undefined;
  }
}

// ---------- Types ----------

export interface AlphahumanConfig {
  /** Bearer token (JWT or API key) for authentication */
  token: string;
  /** Base URL of the Alphahuman backend. If omitted, uses ALPHAHUMAN_BASE_URL env or default staging URL */
  baseUrl?: string;
}

export interface MemoryItem {
  /** Unique key within the namespace (used for upsert / dedup) */
  key: string;
  /** Memory content text */
  content: string;
  /** Namespace to scope this item (default: "default") */
  namespace?: string;
  /** Arbitrary metadata */
  metadata?: Record<string, unknown>;
}

export interface ReadMemoryItem {
  key: string;
  content: string;
  namespace: string;
  metadata: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
}

export interface IngestMemoryRequest {
  items: MemoryItem[];
}

export interface IngestMemoryResponse {
  success: boolean;
  data: {
    ingested: number;
    updated: number;
    errors: number;
  };
}

export interface ReadMemoryRequest {
  /** Single key to read */
  key?: string;
  /** Array of keys to read */
  keys?: string[];
  /** Namespace scope (default: "default") */
  namespace?: string;
}

export interface ReadMemoryResponse {
  success: boolean;
  data: {
    items: ReadMemoryItem[];
    count: number;
  };
}

export interface DeleteMemoryRequest {
  /** Single key to delete */
  key?: string;
  /** Array of keys to delete */
  keys?: string[];
  /** Namespace scope (default: "default") */
  namespace?: string;
  /** Delete all memory for the user (optionally scoped by namespace) */
  deleteAll?: boolean;
}

export interface DeleteMemoryResponse {
  success: boolean;
  data: {
    deleted: number;
  };
}

export interface ErrorResponse {
  success: false;
  error: string;
}

// ---------- Error ----------

export class AlphahumanError extends Error {
  public readonly status: number;
  public readonly body: unknown;

  constructor(message: string, status: number, body?: unknown) {
    super(message);
    this.name = 'AlphahumanError';
    this.status = status;
    this.body = body;
  }
}

// ---------- Client ----------

export class AlphahumanMemoryClient {
  private readonly baseUrl: string;
  private readonly token: string;

  constructor(config: AlphahumanConfig) {
    if (!config.token || !config.token.trim()) throw new Error('token is required');
    const baseUrl = config.baseUrl ?? getEnvBaseUrl() ?? DEFAULT_BASE_URL;
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.token = config.token;
  }

  /** Ingest (upsert) one or more memory items. */
  async ingestMemory(request: IngestMemoryRequest): Promise<IngestMemoryResponse> {
    if (!request.items || request.items.length === 0) {
      throw new Error('items must be a non-empty array');
    }
    return this.post<IngestMemoryResponse>('/v1/memory', request);
  }

  /** Read memory items by key, keys, or namespace. Returns all user memory if no filters. */
  async readMemory(request: ReadMemoryRequest = {}): Promise<ReadMemoryResponse> {
    const params = new URLSearchParams();
    if (request.key) params.set('key', request.key);
    if (request.keys && request.keys.length > 0) {
      for (const k of request.keys) params.append('keys[]', k);
    }
    if (request.namespace) params.set('namespace', request.namespace);
    const qs = params.toString();
    const path = qs ? `/v1/memory?${qs}` : '/v1/memory';
    return this.get<ReadMemoryResponse>(path);
  }

  /** Delete memory items by key, keys array, or deleteAll flag. */
  async deleteMemory(request: DeleteMemoryRequest): Promise<DeleteMemoryResponse> {
    const hasKey = typeof request.key === 'string' && request.key.length > 0;
    const hasKeys = Array.isArray(request.keys) && request.keys.length > 0;
    if (!hasKey && !hasKeys && !request.deleteAll) {
      throw new Error('Provide "key", "keys", or set "deleteAll" to true');
    }
    return this.send<DeleteMemoryResponse>('DELETE', '/v1/memory', request);
  }

  private async get<T>(path: string): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const res = await fetch(url, {
      method: 'GET',
      headers: { Authorization: `Bearer ${this.token}` },
    });
    return this.handleResponse<T>(res);
  }

  private async post<T>(path: string, body: unknown): Promise<T> {
    return this.send<T>('POST', path, body);
  }

  private async send<T>(method: string, path: string, body: unknown): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.token}`,
      },
      body: JSON.stringify(body),
    });
    return this.handleResponse<T>(res);
  }

  private async handleResponse<T>(res: Response): Promise<T> {
    const text = await res.text();
    let json: unknown;
    try {
      json = JSON.parse(text);
    } catch {
      throw new AlphahumanError(
        `HTTP ${res.status}: non-JSON response`,
        res.status,
        text || undefined,
      );
    }
    if (!res.ok) {
      const message = (json as ErrorResponse).error ?? `HTTP ${res.status}`;
      throw new AlphahumanError(message, res.status, json);
    }
    return json as T;
  }
}

export default AlphahumanMemoryClient;
