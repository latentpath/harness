#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash -n "$SCRIPT_DIR"/*.sh
python3 - "$SCRIPT_DIR/harnessctl.py" <<'PY'
import ast
import pathlib
import sys

ast.parse(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
PY
python3 "$SCRIPT_DIR/harnessctl.py" self-check
