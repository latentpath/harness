#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT_DIR"

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_DIR=""
if [ -n "${TASK_ID:-}" ]; then
  TASK_DIR="$HARNESS_DIR/work/$TASK_ID"
  mkdir -p "$TASK_DIR"
  : > "$TASK_DIR/validation.log"
fi

run_step() {
  local name="$1"; shift
  echo "==> $name"
  if [ -n "$TASK_DIR" ]; then
    "$@" 2>&1 | tee -a "$TASK_DIR/validation.log"
  else
    "$@"
  fi
  return ${PIPESTATUS[0]}
}

overall=0

if [ -f "./mvnw" ]; then
  run_step "./mvnw test" bash ./mvnw test || overall=1
else
  run_step "mvn test" mvn test || overall=1
fi

if [ -n "$TASK_DIR" ]; then
  echo "$overall" > "$TASK_DIR/validation.status"
fi

exit "$overall"
