#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found. Install uv first, then re-run."
  exit 1
fi

cd "${repo_root}/apps/api"

uv sync --extra dev
uv run ruff check .
uv run mypy app
uv run pytest
