#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT_DIR"

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_DIR=""
if [ -n "${TASK_ID:-}" ]; then
  python3 "$HARNESS_DIR/scripts/harnessctl.py" check-approval "$TASK_ID" >/dev/null
  TASK_DIR="$HARNESS_DIR/work/$TASK_ID"
  mkdir -p "$TASK_DIR"
  : > "$TASK_DIR/validation.log"
  {
    echo "repository_revision=$(git rev-parse HEAD 2>/dev/null || echo unavailable)"
    echo "started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "java=$(java -version 2>&1 | head -n 1 || echo unavailable)"
  } >> "$TASK_DIR/validation.log"
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
build_status=0
MAVEN_GOAL="${HARNESS_MAVEN_GOAL:-verify}"

if [ -f "./mvnw" ]; then
  run_step "./mvnw $MAVEN_GOAL" bash ./mvnw "$MAVEN_GOAL" || { build_status=$?; overall=1; }
else
  run_step "mvn $MAVEN_GOAL" mvn "$MAVEN_GOAL" || { build_status=$?; overall=1; }
fi

if [ -n "$TASK_DIR" ]; then
  echo "$overall" > "$TASK_DIR/validation.status"
  python3 - "$TASK_DIR/validation.json" "$overall" "$build_status" "$MAVEN_GOAL" <<'PY'
import datetime as dt
import json
import sys

path, overall, build, goal = sys.argv[1:]
payload = {
    "schema_version": 1,
    "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "exit_code": int(overall),
    "steps": [{"name": f"maven {goal}", "exit_code": int(build)}],
}
with open(path, "w", encoding="utf-8") as stream:
    json.dump(payload, stream, indent=2, sort_keys=True)
    stream.write("\n")
PY
fi

exit "$overall"
