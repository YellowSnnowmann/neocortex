# Recalling Memories

Use recall to fetch the most relevant context for a namespace.

## API Endpoint

`POST /memory/recall`

Some deployments and SDKs use a `/v1` prefix (`/v1/memory/recall`). If your deployment requires it, prepend `/v1`.

## Request Body

```json
{
  "namespace": "preferences",
  "maxChunks": 10
}
```

## Examples by Language

{% tabs %}
{% tab title="cURL" %}
```bash
# Recall top chunks from a namespace.
curl -X POST "https://api.tinyhumans.ai/memory/recall" \
  -H "Authorization: Bearer $TINYHUMANS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "preferences",
    "maxChunks": 10
  }'
```
{% endtab %}

{% tab title="TypeScript" %}
```ts
// npm install @tinyhumansai/neocortex
import { TinyHumanMemoryClient } from "@tinyhumansai/neocortex";

async function main() {
  // Read API token from env.
  const token = process.env.TINYHUMANS_TOKEN;
  if (!token) throw new Error("Set TINYHUMANS_TOKEN");

  // Create client.
  const client = new TinyHumanMemoryClient({ token });

  // Recall context from a namespace.
  const result = await client.recallMemory({
    namespace: "preferences",
    maxChunks: 10,
  });

  // Print LLM-ready context string.
  console.log(result.data.llmContextMessage);
}

main().catch(console.error);
```
{% endtab %}

{% tab title="Python" %}
```python
import os
import tinyhumansai as api

# Read API token from env.
token = os.getenv("TINYHUMANS_TOKEN")
if not token:
    raise RuntimeError("Set TINYHUMANS_TOKEN")

# Create client.
client = api.TinyHumanMemoryClient(token=token)

# Recall context based on a natural-language prompt.
ctx = client.recall_memory(
    namespace="preferences",
    prompt="What does the user prefer?",
    num_chunks=10,
)

# Print formatted context for LLM injection.
print(ctx.context)
```
{% endtab %}

{% tab title="Go" %}
```go
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/tinyhumansai/neocortex-sdk-go/tinyhumans"
)

func main() {
	// Read API token from env.
	token := os.Getenv("TINYHUMANS_TOKEN")
	if token == "" {
		log.Fatal("set TINYHUMANS_TOKEN")
	}

	// Create client.
	client, err := tinyhumans.NewClient(token)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Close()

	// Recall context.
	ctx, err := client.RecallMemory(
		"preferences",
		"What does the user prefer?",
		&tinyhumans.RecallMemoryOptions{NumChunks: 10},
	)
	if err != nil {
		log.Fatal(err)
	}

	// Print LLM-ready context.
	fmt.Println(ctx.Context)
}
```
{% endtab %}

{% tab title="Rust" %}
```rust
use std::env;
use tinyhumansai::{RecallMemoryParams, TinyHumanConfig, TinyHumanMemoryClient};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Read API token from env.
    let token = env::var("TINYHUMANS_TOKEN")?;

    // Create client.
    let client = TinyHumanMemoryClient::new(TinyHumanConfig::new(token))?;

    // Recall context.
    let response = client
        .recall_memory(RecallMemoryParams {
            namespace: Some("preferences".into()),
            max_chunks: Some(10.0),
        })
        .await?;

    // Print LLM-ready context.
    println!("{:?}", response.data.llm_context_message);
    Ok(())
}
```
{% endtab %}

{% tab title="Java" %}
```java
import xyz.tinyhuman.sdk.*;

public class RecallExample {
    public static void main(String[] args) {
        // Read API token from env.
        String token = System.getenv("TINYHUMANS_TOKEN");
        if (token == null || token.isEmpty()) throw new RuntimeException("Set token env var");

        // Create client and recall context.
        try (TinyHumanMemoryClient client = new TinyHumanMemoryClient(token)) {
            RecallMemoryResponse response = client.recallMemory(
                new RecallMemoryParams()
                    .setNamespace("preferences")
                    .setMaxChunks(10)
            );

            // Print LLM-ready context.
            System.out.println(response.getLlmContextMessage());
        }
    }
}
```
{% endtab %}

{% tab title="C++" %}
```cpp
#include "tinyhuman/tinyhuman.hpp"

#include <cstdlib>
#include <iostream>
#include <stdexcept>

using namespace tinyhuman;

int main() {
    // Read API token from env.
    const char* token = std::getenv("TINYHUMANS_TOKEN");
    if (!token) throw std::runtime_error("Set TINYHUMANS_TOKEN");

    // Create client.
    TinyHumanMemoryClient client(token);

    // Recall context.
    RecallMemoryParams params;
    params
        .set_namespace("preferences")
        .set_max_chunks(10);

    auto response = client.recall_memory(params);

    // Print LLM-ready context if present.
    if (response.llm_context_message) {
        std::cout << *response.llm_context_message << std::endl;
    }
    return 0;
}
```
{% endtab %}
{% endtabs %}
