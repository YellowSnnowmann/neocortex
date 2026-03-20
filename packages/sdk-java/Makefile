.PHONY: build test integration-test clean

build:
	./gradlew build

test:
	./gradlew test

integration-test:
	TINYHUMANS_TOKEN=$(TINYHUMANS_TOKEN) ./gradlew test

clean:
	./gradlew clean
