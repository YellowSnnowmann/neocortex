.PHONY: build test integration-test clean

build:
	dotnet build

test:
	dotnet test --filter "Category!=Integration"

integration-test:
	dotnet test --filter "Category=Integration"

clean:
	dotnet clean
	rm -rf src/TinyHuman.Sdk/bin src/TinyHuman.Sdk/obj
	rm -rf test/TinyHuman.Sdk.Tests/bin test/TinyHuman.Sdk.Tests/obj
	rm -rf example/TinyHuman.Sdk.Example/bin example/TinyHuman.Sdk.Example/obj
