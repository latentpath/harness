#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: bash scripts/check-approval.sh <task-id>" >&2
  exit 2
fi

TASK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/work/$1"
APPROVAL="$TASK_DIR/approval.json"
PLAN="$TASK_DIR/plan.md"

[ -f "$APPROVAL" ] || { echo "BLOCKED: approval.json is missing" >&2; exit 1; }
[ -f "$PLAN" ] || { echo "NEEDS_REVISION: plan.md is missing" >&2; exit 1; }

status=$(sed -n 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$APPROVAL")
plan_sha=$(sed -n 's/.*"plan_sha256"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$APPROVAL")
approved_at=$(sed -n 's/.*"approved_at"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$APPROVAL")
approved_by=$(sed -n 's/.*"approved_by"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$APPROVAL")
current_sha=$(sha256sum "$PLAN" | awk '{print $1}')

[ "$status" = "approved" ] || { echo "BLOCKED: approval status is not approved" >&2; exit 1; }
[ -n "$plan_sha" ] || { echo "BLOCKED: approval.json.plan_sha256 is missing" >&2; exit 1; }
[ -n "$approved_at" ] || { echo "BLOCKED: approval.json.approved_at is missing" >&2; exit 1; }
[ -n "$approved_by" ] || { echo "BLOCKED: approval.json.approved_by is missing" >&2; exit 1; }
[ "$current_sha" = "$plan_sha" ] || { echo "NEEDS_REVISION: plan_sha256 does not match plan.md" >&2; exit 1; }

echo "APPROVED: plan hash matches approval.json"
