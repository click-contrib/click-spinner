#! /bin/bash -ex

uv run ruff check click_spinner
uv run mypy --check-untyped-defs --strict click_spinner
uv run pytest tests
