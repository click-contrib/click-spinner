#! /bin/bash -ex

#uv run ruff check click_spinner
#uv run mypy --strict --check-untyped-defs --explicit-package-bases --strict click_spinner
uv run pytest .
