#!/usr/bin/env bash
# harness/scripts/validate.sh
#
# Flutter formatting, analysis, and test validation.
#
# Usage (when installed as harness/ inside a Flutter repo root):
#   bash harness/scripts/validate.sh              # run checks, exit 0/1
#   TASK_ID=<task-id> bash harness/scripts/validate.sh
#
# When TASK_ID is set, this script records *actual validation evidence* beside
# the task artifacts:
#   harness/work/<TASK_ID>/validation.log         # full captured output
#   harness/work/<TASK_ID>/validation.status      # numeric exit code (0 = pass)
#
# The exit code of this script reflects pass/fail as before. Capturing evidence
# never changes the validation outcome.
set -uo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$HARNESS_DIR/.." && pwd)"
cd "$REPO_ROOT"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

[ -f "$REPO_ROOT/pubspec.yaml" ] \
  || fail "Flutter project root not found at $REPO_ROOT. The harness directory must live inside the target Flutter repo root to run pub/analyze/test."

TASK_DIR=""
if [ -n "${TASK_ID:-}" ]; then
  TASK_DIR="$HARNESS_DIR/work/$TASK_ID"
  mkdir -p "$TASK_DIR"
  : > "$TASK_DIR/validation.log"   # reset so stale output is never reused
fi

# Run one step, tee to the log when evidence capture is active, and accumulate
# the worst exit code so ALL steps run and the failure is reported truthfully.
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

run_step "flutter pub get" flutter pub get          || overall=1
run_step "dart format --set-exit-if-changed ." \
  dart format --set-exit-if-changed .                || overall=1
run_step "flutter analyze" flutter analyze           || overall=1
run_step "flutter test" flutter test                 || overall=1

# Record the exit code of this run as validation evidence (always written, pass
# or fail, so a missing status never masquerades as a stale pass).
if [ -n "$TASK_DIR" ]; then
  echo "$overall" > "$TASK_DIR/validation.status"
fi

exit "$overall"
