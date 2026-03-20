# tinyhuman-sdk-java

Java SDK for TinyHumans/TinyHuman Neocortex memory APIs.

## Requirements

- Java 11+
- Gradle (wrapper included)

## Build

```bash
cd packages/sdk-java
./gradlew build
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

## Example (all SDK methods)

`example/ExampleUsage.java` exercises every method exposed by this SDK:
- `insertMemory`
- `recallMemory`
- `queryMemory`
- `recallMemories`
- `deleteMemory`

Build and run the example:

```bash
cd packages/sdk-java
./gradlew build
cd example
javac -cp ../build/libs/tinyhuman-sdk-java-0.1.0.jar ExampleUsage.java
java -cp .:../build/libs/tinyhuman-sdk-java-0.1.0.jar ExampleUsage
```

## API scope

This SDK currently exposes the core memory routes only (insert/query/recall/recallMemories/delete).
