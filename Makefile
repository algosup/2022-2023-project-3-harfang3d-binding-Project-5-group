.PHONY: help tests-echo clear-build
.DEFAULT_GOAL=help

CURRENT_DIR=$(shell pwd)

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

tests-echo:
	@echo "Running tests..."

build: Dockerfile # Build docker image.
	@echo "Building docker image..."
	docker build -t fabgen-builder:1.0 . -f Dockerfile

clear-build: # Clear docker images built by this Makefile.
	docker system prune --filter "label=customname=FABGen-tests" -af

tests-python: tests-echo # Run python tests.
	docker run -it --rm --name tests-fabgen --volume $(CURRENT_DIR):/usr/src/tests --workdir /usr/src/tests fabgen-builder:1.0 python3 tests.py --linux --pybase /usr/bin/python/

tests-golang: tests-echo # Run golang tests.
	docker run -it --rm --name tests-golang fabgen-golang-tests:1.0 python3 tests.py --linux --go

tests-lua54: tests-echo # Run lua54 tests.
	docker run -it --rm --name tests-lua54 fabgen-lua54-tests:1.0 python3 tests.py --linux --luabase /usr/bin/lua5.4