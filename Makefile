.PHONY: help tests
.DEFAULT_GOAL=help

CURRENT_DIR=$(shell pwd)

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

tests-python: build-python tests # Run python tests
	docker run -it --rm --name tests -v $(CURRENT_DIR):/usr/src/tests -w /usr/src/tests fabgen-python-tests:1.0 python tests.py --linux --pybase /usr/bin/python

tests-golang: build-golang tests # Run golang tests
	docker run -it --rm --name tests -v $(CURRENT_DIR):/usr/src/tests -w /usr/src/tests fabgen-golang-tests:1.0 python tests.py --linux --go

tests:
	@echo "Running tests..."

build: Dockerfiles/
	@echo "Building docker image..."

build-python: build Dockerfiles/Dockerfile.python
	docker build -t fabgen-python-tests:1.0 . -f Dockerfiles/Dockerfile.python

build-golang: build Dockerfiles/Dockerfile.golang
	docker build -t fabgen-golang-tests:1.0 . -f Dockerfiles/Dockerfile.golang