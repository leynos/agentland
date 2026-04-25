.PHONY: help all clean test build release lint fmt check-fmt markdownlint nixie graphs check-graphs manifest-check assets-check


TARGET ?= agentland

CARGO ?= cargo
PYTHON ?= python3
BUILD_JOBS ?=
RUST_FLAGS ?=
RUST_FLAGS := -D warnings $(RUST_FLAGS)
RUSTDOC_FLAGS ?=
RUSTDOC_FLAGS := -D warnings $(RUSTDOC_FLAGS)
CARGO_FLAGS ?= --all-targets --all-features
CLIPPY_FLAGS ?= $(CARGO_FLAGS) -- $(RUST_FLAGS)
TEST_FLAGS ?= $(CARGO_FLAGS)
TEST_CMD := $(if $(shell $(CARGO) nextest --version 2>/dev/null),nextest run,test)
MDLINT ?= markdownlint-cli2
NIXIE ?= nixie
DOT ?= dot

STATE_GRAPH_DOTS := docs/ui-state-graph.dot docs/ui-state-graph-overview.dot
STATE_GRAPH_SVGS := $(STATE_GRAPH_DOTS:.dot=.svg)

build: target/debug/$(TARGET) ## Build debug binary
release: target/release/$(TARGET) ## Build release binary

all: check-fmt lint test ## Perform a comprehensive check of code

clean: ## Remove build artifacts
	$(CARGO) clean

test: ## Run tests with warnings treated as errors
	RUSTFLAGS="$(RUST_FLAGS)" $(CARGO) $(TEST_CMD) $(TEST_FLAGS) $(BUILD_JOBS)
ifneq ($(TEST_CMD),test)
	RUSTFLAGS="$(RUST_FLAGS)" $(CARGO) test --doc --workspace --all-features
endif

target/%/$(TARGET): ## Build binary in debug or release mode
	$(CARGO) build $(BUILD_JOBS) $(if $(findstring release,$(@)),--release) --bin $(TARGET)

lint: ## Run Clippy with warnings denied
	RUSTDOCFLAGS="$(RUSTDOC_FLAGS)" $(CARGO) doc --no-deps
	$(CARGO) clippy $(CLIPPY_FLAGS)
	@command -v whitaker >/dev/null 2>&1 && \
		RUSTFLAGS="$(RUST_FLAGS)" whitaker --all -- $(CARGO_FLAGS) || \
		{ echo "whitaker not found on PATH; skipping whitaker lint. Install whitaker to run this check."; }

typecheck: ## Type-check without building
	RUSTFLAGS="$(RUST_FLAGS)" $(CARGO) check $(CARGO_FLAGS)

fmt: ## Format Rust and Markdown sources
	$(CARGO) +nightly fmt --all
	mdformat-all

check-fmt: ## Verify formatting
	$(CARGO) fmt --all -- --check

markdownlint: ## Lint Markdown files
	$(MDLINT) '**/*.md'

manifest-check: ## Validate asset manifest schema
	$(PYTHON) tools/check_manifests.py

assets-check: manifest-check ## Validate asset metadata and manifests
	$(PYTHON) tools/check_assets.py

nixie: ## Validate Mermaid diagrams
	$(NIXIE) --no-sandbox

graphs: $(STATE_GRAPH_SVGS) ## Rebuild generated state graph SVGs

check-graphs: ## Verify generated state graph SVGs are current
	@tmp_dir=$$(mktemp -d); \
	trap 'rm -rf "$$tmp_dir"' EXIT; \
	for dot_file in $(STATE_GRAPH_DOTS); do \
		svg_file="$${dot_file%.dot}.svg"; \
		tmp_file="$$tmp_dir/$$(basename "$$svg_file")"; \
		$(DOT) -Tsvg "$$dot_file" -o "$$tmp_file"; \
		cmp -s "$$tmp_file" "$$svg_file" || { \
			echo "$$svg_file is out of date; run 'make graphs'."; \
			exit 1; \
		}; \
	done

docs/%.svg: docs/%.dot
	$(DOT) -Tsvg $< -o $@

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS=":"; printf "Available targets:\n"} {printf "  %-20s %s\n", $$1, $$2}'
