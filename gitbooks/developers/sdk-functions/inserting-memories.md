# Inserting Memories

Use this operation to upsert memory into a namespace. Memories can also be backdated by sending in the time. Backdated memories tend to get forgotten more however they'll get remember if they've either been interacted with or recalled by the user.

{% tabs %}
{% tab title="cURL" %}

```bash
# Insert (upsert) one memory item.
curl -X POST "https://api.tinyhumans.ai/memory/insert" \
  -H "Authorization: Bearer $TINYHUMANS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "user-preference-theme",
    "content": "User prefers dark mode",
    "namespace": "preferences",
    "sourceType": "doc",
    "metadata": {"source": "onboarding"}
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

  // Insert one memory item.
  const result = await client.insertMemory({
    title: "user-preference-theme",
    content: "User prefers dark mode",
    namespace: "preferences",
    sourceType: "doc",
    metadata: { source: "onboarding" },
  });

  // Print insert status.
  console.log(result.data.status);
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

# Insert one memory item.
result = client.ingest_memory(
    item={
        "key": "user-preference-theme",
        "content": "User prefers dark mode",
        "namespace": "preferences",
        "metadata": {"source": "onboarding"},
    }
)

# Print insert/update counters.
print(result.ingested, result.updated, result.errors)
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

	// Insert one memory item.
	resp, err := client.IngestMemory(tinyhumans.MemoryItem{
		Key:       "user-preference-theme",
		Content:   "User prefers dark mode",
		Namespace: "preferences",
		Metadata:  map[string]interface{}{"source": "onboarding"},
	})
	if err != nil {
		log.Fatal(err)
	}

	// Print insert/update counters.
	fmt.Println(resp.Ingested, resp.Updated, resp.Errors)
}
```

{% endtab %}

{% tab title="Rust" %}

```rust
use std::env;
use tinyhumansai::{InsertMemoryParams, TinyHumanConfig, TinyHumanMemoryClient};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Read API token from env.
    let token = env::var("TINYHUMANS_TOKEN")?;

    // Create client.
    let client = TinyHumanMemoryClient::new(TinyHumanConfig::new(token))?;

    // Insert one memory item.
    let response = client
        .insert_memory(InsertMemoryParams {
            title: "user-preference-theme".into(),
            content: "User prefers dark mode".into(),
            namespace: "preferences".into(),
            ..Default::default()
        })
        .await?;

    // Print insert status.
    println!("{}", response.data.status.unwrap_or_default());
    Ok(())
}
```

{% endtab %}

{% tab title="Java" %}

```java
import xyz.tinyhuman.sdk.*;

public class InsertExample {
    public static void main(String[] args) {
        // Read API token from env.
        String token = System.getenv("TINYHUMANS_TOKEN");
        if (token == null || token.isEmpty()) throw new RuntimeException("Set token env var");

        // Create client and insert one memory item.
        try (TinyHumanMemoryClient client = new TinyHumanMemoryClient(token)) {
            InsertMemoryResponse response = client.insertMemory(
                new InsertMemoryParams("user-preference-theme", "User prefers dark mode", "preferences")
            );

            // Print insert status.
            System.out.println(response.getStatus());
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

    // Insert one memory item.
    InsertMemoryParams params;
    params
        .set_title("user-preference-theme")
        .set_content("User prefers dark mode")
        .set_namespace("preferences");

    auto response = client.insert_memory(params);

    // Print insert status.
    std::cout << response.status << std::endl;
    return 0;
}
```

{% endtab %}
{% endtabs %}
