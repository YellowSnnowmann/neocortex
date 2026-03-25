# tinyhumans Go SDK

Go client for TinyHumans Neocortex memory APIs.

## Requirements

- Go 1.21+

## Install

```bash
go get github.com/tinyhumansai/neocortex-sdk-go
```

## Get an API key

1. Sign in to your TinyHumans account.
2. Create a server API key in the TinyHumans dashboard.
3. Export it before running examples:

```bash
export TINYHUMANS_TOKEN="your_api_key"
# optional custom API URL
export TINYHUMANS_BASE_URL="https://api.tinyhumans.ai"
```

## Quick start

```go
package main

import (
  "fmt"
  "log"
  "os"

  "github.com/tinyhumansai/neocortex-sdk-go/tinyhumans"
)

func main() {
  client, err := tinyhumans.NewClient(os.Getenv("TINYHUMANS_TOKEN"))
  if err != nil {
    log.Fatal(err)
  }
  defer client.Close()

  _, err = client.IngestMemory(tinyhumans.MemoryItem{
    Key:       "user-preference-theme",
    Content:   "User prefers dark mode",
    Namespace: "preferences",
  })
  if err != nil {
    log.Fatal(err)
  }

  ctx, err := client.RecallMemory("preferences", "What does the user prefer?", nil)
  if err != nil {
    log.Fatal(err)
  }

  fmt.Println(ctx.Context)
}
```

## Full route example

`example/main.go` exercises all exported client methods:
- `IngestMemory`
- `IngestMemories`
- `RecallMemory`
- `DeleteMemory`
- `RecallWithLLM`
- `Close`

Run it with:

```bash
cd packages/sdk-golang
go run ./example/main.go
```

## API surface

`NewClient(token string, baseURL ...string)`
- Base URL resolution: argument -> `TINYHUMANS_BASE_URL` env -> `https://api.tinyhumans.ai`.

`RecallWithLLM` supports:
- OpenAI (`provider: "openai"`)
- Anthropic (`"anthropic"`)
- Google (`"google"`)
- Custom OpenAI-compatible URL (`URL` option)

## Current SDK scope

This Go SDK currently implements the core memory routes plus LLM helper only. It does not yet expose the newer document/mirrored routes that exist in the TypeScript/Python/Rust SDKs.
