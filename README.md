# Engineering Harnesses

This repository contains focused starter packs for Flutter and Spring Boot.
Each pack uses the same four-stage workflow:

1. `spec`: turn a request into a task contract.
2. `plan`: inspect the repository and write an implementation plan.
3. `implement`: write code and tests, validate, and record the outcome.
4. `review`: independently review the result against the artifacts and code.

Each pack contains a technology-specific `AGENTS.md`, four prompts in
`prompts/`, a `work/<task-id>/` artifact convention, optional templates in
`templates/`, and a technical validation script. Read the selected pack's
`README.md` for installation and use.

The operator chooses a task ID but does not create its work directory. The
active stage prompt runs `harnessctl.py stage-start`, which validates the ID,
creates `harness/work/<task-id>/`, and records the stage baseline.

## Workflow Profiles

- **Full** (default for feature, cross-layer, ambiguous, or high-risk work):
  `SPEC -> PLAN -> APPROVAL -> IMPLEMENT -> VALIDATE -> REVIEW`.
- **Lite** (only for small, low-risk, fully specified changes): produce a
  compact SPEC and PLAN in one preparation session, then run
  `APPROVAL -> IMPLEMENT -> VALIDATE`.
  Escalate to Full for public contracts, persistence, authentication,
  concurrency, migrations, destructive work, or material ambiguity.

`scripts/harnessctl.py` is a lightweight enforcement helper, not an agent
runtime. It validates task IDs and approval JSON, binds approval to SPEC and
PLAN, records `state.json`, captures stage baselines, and checks file
ownership. Run `bash harness/scripts/self-check.sh` after installation.

All packs share the same contract. SPEC is the normative requirement truth.
PLAN proposes an implementation strategy and must not weaken, remove, or
reinterpret a SPEC requirement. Project constitutions and phase gates provide
repository constraints; they do not make a PLAN authoritative over SPEC.
Observed truth is verified repository reality; evidence is what actually
happened. Conflicts must be classified as an expected implementation delta,
`NEEDS_REVISION`, or `BLOCKED`. Machine evidence overrides contradictory
narrative claims.

The authority hierarchy is:

```
SPEC > PLAN
```

`approval.json` authorizes execution of the exact SHA-256-bound PLAN. It does
not authorize a requirement change. A material normative change requires a
revised SPEC, a new PLAN, and new approval.

The common lifecycle statuses are `BLOCKED`, `NEEDS_REVISION`, `FAILED`,
`COMPLETED`, `APPROVED`, `CHANGES_REQUESTED`, and `ABORTED`. IMPLEMENT owns
implementation completion and validation state and must not self-approve.
REVIEW exclusively owns the final acceptance verdict. Phase ownership is
explicit: SPEC writes `spec.md`, PLAN writes `plan.md`, IMPLEMENT writes
approved source, tests, `development.md`, and generated validation evidence,
and REVIEW writes `review.md` plus permitted non-authoritative memory where
supported.

## Method

Use the optional templates to decompose a project top-down, then execute each
task bottom-up through the four stages:

1. `templates/project-constitution.md` – fill once at inception and store the
   filled copy as the project's root `AGENTS.md`. It holds stable project
   facts and governance; it does not hold the active phase or task status.
2. `templates/phase.md` – store filled copies under project-owned paths such as
   `docs/phases/phase-1.md`. Pass the governing phase path explicitly when
   starting SPEC. `spec` records that path and must not cross its gate.
3. `templates/project-baseline.md` – fill the project baseline (requirements /
   API contract / state model / quality gates) and use it as a source input
   for `spec`.
4. Break the phase into task contracts, then run each task through the four
   stages (`spec` -> `plan` -> `implement` -> `review`) as described below.

The dividing line: mechanism lives here in `templates/`, content lives in the
project (project root `AGENTS.md`, project `docs/`, and `work/` artifacts).
All templates are optional; the four-stage flow works without them.
