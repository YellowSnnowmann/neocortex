// Example usage of the TinyHumans Go SDK.
//
// Set environment variables: TINYHUMANS_TOKEN, OPENAI_API_KEY
package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/tinyhumansai/neocortex-sdk-go/tinyhumans"
)

func main() {
	client, err := tinyhumans.NewClient(
		os.Getenv("TINYHUMANS_TOKEN"),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Close()

	// Ingest (upsert) a single memory
	now := float64(time.Now().Unix())
	result, err := client.IngestMemory(tinyhumans.MemoryItem{
		Key:       "user-preference-theme",
		Content:   "User prefers dark mode",
		Namespace: "preferences",
		Metadata:  map[string]interface{}{"source": "onboarding"},
		CreatedAt: &now,
		UpdatedAt: &now,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Ingested: %d, Updated: %d, Errors: %d\n", result.Ingested, result.Updated, result.Errors)

	// Ingest multiple memories
	batch, err := client.IngestMemories([]tinyhumans.MemoryItem{
		{
			Key:       "go-sdk-example-1",
			Content:   "Go SDK can ingest multiple memories.",
			Namespace: "preferences",
			Metadata:  map[string]interface{}{"source": "go-example"},
		},
		{
			Key:       "go-sdk-example-2",
			Content:   "This is a second memory from the Go example.",
			Namespace: "preferences",
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Batch Ingested: %d, Updated: %d, Errors: %d\n", batch.Ingested, batch.Updated, batch.Errors)

	// Get LLM context
	ctx, err := client.RecallMemory("preferences", "What is the user's preference for theme?", nil)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(ctx.Context)

	// (Optional) Query LLM with context
	openaiKey := os.Getenv("OPENAI_API_KEY")
	if openaiKey != "" {
		resp, err := client.RecallWithLLM(
			"What is the user's preference for theme?",
			openaiKey,
			tinyhumans.RecallWithLLMOptions{
				Provider: "openai",
				Model:    "gpt-4o-mini",
				Context:  ctx.Context,
			},
		)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(resp.Text)
	}

	// Delete by namespace
	_, err = client.DeleteMemory("preferences", &tinyhumans.DeleteMemoryOptions{
		DeleteAll: true,
	})
	if err != nil {
		log.Fatal(err)
	}
}
