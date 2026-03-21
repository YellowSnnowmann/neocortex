# Deleting Memories

Use delete to remove memory by namespace.

## API Endpoint

`POST /memory/admin/delete`

Some deployments and SDKs use a `/v1` prefix (`/v1/memory/admin/delete`). If your deployment requires it, prepend `/v1`.

## Request Body

```json
{
  "namespace": "preferences"
}
```

## Examples by Language

{% tabs %}
{% tab title="cURL" %}
```bash
# Delete all memory in a namespace.
curl -X POST "https://api.tinyhumans.ai/memory/admin/delete" \
  -H "Authorization: Bearer $TINYHUMANS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"namespace": "preferences"}'
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

  // Delete by namespace.
  const result = await client.deleteMemory({ namespace: "preferences" });

  // Print nodes deleted from API response.
  console.log(result.data.nodesDeleted);
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

# Delete namespace memory.
response = client.delete_memory(namespace="preferences", delete_all=True)

# Print number of deleted records.
print(response.deleted)
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

	// Delete by namespace.
	resp, err := client.DeleteMemory("preferences", nil)
	if err != nil {
		log.Fatal(err)
	}

	// Print number deleted.
	fmt.Println(resp.Deleted)
}
```
{% endtab %}

{% tab title="Rust" %}
```rust
use std::env;
use tinyhumansai::{DeleteMemoryParams, TinyHumanConfig, TinyHumanMemoryClient};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Read API token from env.
    let token = env::var("TINYHUMANS_TOKEN")?;

    // Create client.
    let client = TinyHumanMemoryClient::new(TinyHumanConfig::new(token))?;

    // Delete by namespace.
    let response = client
        .delete_memory(DeleteMemoryParams {
            namespace: Some("preferences".into()),
        })
        .await?;

    // Print number deleted.
    println!("{}", response.data.nodes_deleted);
    Ok(())
}
```
{% endtab %}

{% tab title="Java" %}
```java
import xyz.tinyhuman.sdk.*;

public class DeleteExample {
    public static void main(String[] args) {
        // Read API token from env.
        String token = System.getenv("TINYHUMANS_TOKEN");
        if (token == null || token.isEmpty()) throw new RuntimeException("Set token env var");

        // Create client and delete by namespace.
        try (TinyHumanMemoryClient client = new TinyHumanMemoryClient(token)) {
            DeleteMemoryResponse response = client.deleteMemory(
                new DeleteMemoryParams().setNamespace("preferences")
            );

            // Print number deleted.
            System.out.println(response.getNodesDeleted());
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

    // Delete by namespace.
    DeleteMemoryParams params;
    params.set_namespace("preferences");
    auto response = client.delete_memory(params);

    // Print number deleted.
    std::cout << response.nodes_deleted << std::endl;
    return 0;
}
```
{% endtab %}
{% endtabs %}
