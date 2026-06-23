#! /bin/bash -ex

uv run ruff check click_spinner
#uv run mypy --check-untyped-defs --explicit-package-bases --strict click_spinner
uv run mypy click_spinner
uv run pytest tests
