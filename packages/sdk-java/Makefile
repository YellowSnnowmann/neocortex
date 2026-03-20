.PHONY: build test integration-test clean

build:
	gradle build

test:
	gradle test

integration-test:
	TINYHUMANS_TOKEN=$(TINYHUMANS_TOKEN) gradle test

clean:
	gradle clean
