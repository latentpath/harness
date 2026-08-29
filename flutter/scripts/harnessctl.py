#!/usr/bin/env python3
"""Small, dependency-free enforcement helpers for the repository harness."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
STAGES = ("spec", "plan", "implement", "review")
TERMINAL = {
    "spec": {"COMPLETED", "BLOCKED", "NEEDS_REVISION", "ABORTED"},
    "plan": {"COMPLETED", "BLOCKED", "NEEDS_REVISION", "ABORTED"},
    "implement": {"COMPLETED", "FAILED", "BLOCKED", "NEEDS_REVISION", "ABORTED"},
    "review": {"APPROVED", "CHANGES_REQUESTED", "BLOCKED", "FAILED", "ABORTED"},
}


class HarnessError(Exception):
    pass


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def harness_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def repo_root() -> Path:
    return harness_dir().parent


def task_dir(task_id: str, create: bool = False) -> Path:
    if not TASK_ID_RE.fullmatch(task_id):
        raise HarnessError(
            "invalid task id; use 1-80 ASCII letters, digits, dot, underscore, or hyphen"
        )
    work = (harness_dir() / "work").resolve()
    target = (work / task_id).resolve()
    if target.parent != work:
        raise HarnessError("task path escapes harness/work")
    if create:
        target.mkdir(parents=True, exist_ok=True)
    return target


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HarnessError(f"missing {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise HarnessError(f"invalid JSON in {path.name}: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise HarnessError(f"{path.name} must contain one JSON object")
    return value


def parse_timestamp(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HarnessError("approval.json.approved_at must be a non-empty ISO-8601 timestamp")
    candidate = value.replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise HarnessError("approval.json.approved_at is not valid ISO-8601") from exc
    if parsed.tzinfo is None:
        raise HarnessError("approval.json.approved_at must include a timezone")
    return value


def approval_facts(task_id: str) -> dict:
    directory = task_dir(task_id)
    spec = directory / "spec.md"
    plan = directory / "plan.md"
    if not spec.is_file():
        raise HarnessError("NEEDS_REVISION: spec.md is missing")
    if not plan.is_file():
        raise HarnessError("NEEDS_REVISION: plan.md is missing")
    approval = read_object(directory / "approval.json")
    required = {"status", "spec_sha256", "plan_sha256", "approved_at", "approved_by"}
    missing = sorted(required - approval.keys())
    if missing:
        raise HarnessError("approval.json missing fields: " + ", ".join(missing))
    if approval["status"] != "approved":
        raise HarnessError("BLOCKED: approval status is not approved")
    for field in ("spec_sha256", "plan_sha256"):
        if not isinstance(approval[field], str) or not SHA_RE.fullmatch(approval[field]):
            raise HarnessError(f"approval.json.{field} must be a lowercase SHA-256")
    parse_timestamp(approval["approved_at"])
    if not isinstance(approval["approved_by"], str) or not approval["approved_by"].strip():
        raise HarnessError("approval.json.approved_by must be a non-empty string")
    actual_spec = sha256(spec)
    actual_plan = sha256(plan)
    if approval["spec_sha256"] != actual_spec:
        raise HarnessError("NEEDS_REVISION: spec_sha256 does not match spec.md")
    if approval["plan_sha256"] != actual_plan:
        raise HarnessError("NEEDS_REVISION: plan_sha256 does not match plan.md")
    return {
        "approved": True,
        "spec_sha256": actual_spec,
        "plan_sha256": actual_plan,
        "approved_at": approval["approved_at"],
        "approved_by": approval["approved_by"],
    }


def file_manifest() -> dict[str, str]:
    root = repo_root()
    result: dict[str, str] = {}
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in {".git", ".dart_tool", "build", "target"})
        for name in sorted(files):
            path = Path(current) / name
            if path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            result[relative] = sha256(path)
    return result


def baseline_path(task_id: str, stage: str) -> Path:
    return task_dir(task_id, create=True) / f".{stage}-baseline.json"


def stage_start(task_id: str, stage: str) -> None:
    if stage == "implement":
        approval_facts(task_id)
    payload = {
        "schema_version": 1,
        "task_id": task_id,
        "stage": stage,
        "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "files": file_manifest(),
    }
    baseline_path(task_id, stage).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"STARTED: {stage} baseline recorded for {task_id}")


def changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))


def stage_check(task_id: str, stage: str) -> None:
    baseline = read_object(baseline_path(task_id, stage))
    before = baseline.get("files")
    if not isinstance(before, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in before.items()):
        raise HarnessError("invalid stage baseline")
    changes = changed_paths(before, file_manifest())
    task_prefix = f"harness/work/{task_id}/"
    baseline_file = task_prefix + f".{stage}-baseline.json"
    evidence = {
        task_prefix + "validation.log",
        task_prefix + "validation.status",
        task_prefix + "validation.json",
        task_prefix + "metrics.json",
        task_prefix + "state.json",
        baseline_file,
    }
    if stage == "spec":
        allowed = evidence | {task_prefix + "spec.md"}
    elif stage == "plan":
        allowed = evidence | {task_prefix + "plan.md"}
    elif stage == "review":
        allowed = evidence | {task_prefix + "review.md"}
    else:
        protected_artifacts = {
            task_prefix + "spec.md",
            task_prefix + "plan.md",
            task_prefix + "approval.json",
            task_prefix + "review.md",
        }
        protected = sorted(set(changes) & protected_artifacts)
        if protected:
            raise HarnessError("IMPLEMENT changed protected artifacts: " + ", ".join(protected))
        print("SCOPE PASS: IMPLEMENT protected artifacts are unchanged")
        return
    violations = sorted(set(changes) - allowed)
    if violations:
        raise HarnessError(f"{stage.upper()} changed files outside its ownership: " + ", ".join(violations))
    print(f"SCOPE PASS: {stage.upper()} changed only permitted files")


def write_state(task_id: str, stage: str, status: str) -> None:
    if status not in TERMINAL[stage]:
        raise HarnessError(f"invalid status {status!r} for {stage}")
    directory = task_dir(task_id, create=True)
    if stage in {"plan", "implement", "review"} and not (directory / "spec.md").is_file():
        raise HarnessError(f"{stage.upper()} requires spec.md")
    if stage in {"implement", "review"} and not (directory / "plan.md").is_file():
        raise HarnessError(f"{stage.upper()} requires plan.md")
    if stage == "review" and not (directory / "development.md").is_file():
        raise HarnessError("REVIEW requires development.md")
    state_path = directory / "state.json"
    previous = read_object(state_path) if state_path.exists() else None
    stage_index = STAGES.index(stage)
    if previous:
        previous_stage = previous.get("stage")
        if previous_stage not in STAGES:
            raise HarnessError("state.json contains an unknown stage")
        previous_index = STAGES.index(previous_stage)
        if stage_index > previous_index + 1:
            raise HarnessError("cannot skip lifecycle stages")
    if stage in {"implement", "review"}:
        facts = approval_facts(task_id)
    else:
        facts = {}
    if stage == "review":
        validation = directory / "validation.status"
        if not validation.is_file() or validation.read_text(encoding="utf-8").strip() != "0":
            raise HarnessError("REVIEW requires validation.status == 0")
    payload = {
        "schema_version": 1,
        "task_id": task_id,
        "stage": stage,
        "status": status,
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        **facts,
    }
    temp = state_path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(state_path)
    print(f"STATE: {task_id} {stage} {status}")


def repo_revision() -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_root(), text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def metrics(task_id: str) -> None:
    directory = task_dir(task_id)
    status_path = directory / "validation.status"
    validation_status = None
    if status_path.exists():
        try:
            validation_status = int(status_path.read_text(encoding="utf-8").strip())
        except ValueError as exc:
            raise HarnessError("validation.status is not an integer") from exc
    try:
        approval = approval_facts(task_id)
    except HarnessError as exc:
        approval = {"approved": False, "reason": str(exc)}
    payload = {
        "schema_version": 1,
        "task_id": task_id,
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository_revision": repo_revision(),
        "approval": approval,
        "validation": {
            "status": validation_status,
            "result": "NOT_RUN" if validation_status is None else ("PASS" if validation_status == 0 else "FAIL"),
        },
        "artifacts": {name: (directory / name).is_file() for name in (
            "spec.md", "plan.md", "approval.json", "development.md", "review.md"
        )},
    }
    output = directory / "metrics.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)


def self_check() -> None:
    required = [
        harness_dir() / "AGENTS.md",
        *(harness_dir() / "prompts" / name for name in ("01-spec.md", "02-plan.md", "03-implement.md", "04-review.md")),
        harness_dir() / "scripts" / "check-approval.sh",
        harness_dir() / "scripts" / "validate.sh",
        Path(__file__),
    ]
    missing = [str(path.relative_to(harness_dir())) for path in required if not path.is_file()]
    if missing:
        raise HarnessError("missing harness files: " + ", ".join(missing))
    print("SELF-CHECK PASS: required Harness files are present")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("check-approval", "metrics"):
        sub = commands.add_parser(name)
        sub.add_argument("task_id")
    for name in ("stage-start", "stage-check"):
        sub = commands.add_parser(name)
        sub.add_argument("task_id")
        sub.add_argument("stage", choices=STAGES)
    state = commands.add_parser("state")
    state.add_argument("task_id")
    state.add_argument("stage", choices=STAGES)
    state.add_argument("status")
    commands.add_parser("self-check")
    return root


def main() -> None:
    args = parser().parse_args()
    try:
        if args.command == "check-approval":
            facts = approval_facts(args.task_id)
            print("APPROVED: spec and plan hashes match approval.json")
            print(json.dumps(facts, sort_keys=True))
        elif args.command == "stage-start":
            stage_start(args.task_id, args.stage)
        elif args.command == "stage-check":
            stage_check(args.task_id, args.stage)
        elif args.command == "state":
            write_state(args.task_id, args.stage, args.status)
        elif args.command == "metrics":
            metrics(args.task_id)
        else:
            self_check()
    except HarnessError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
