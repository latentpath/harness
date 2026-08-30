# Project Constitution

> Optional, fill-in-once skeleton for a project's "Main" layer. At project
> inception, fill a first draft and keep the filled copy as the project's
> root `AGENTS.md` (or in the project `docs/`). This file is a mechanism:
> the facts you fill in belong to the project, not to the harness pack.
> `harness/AGENTS.md` stays generic and unchanged; this constitution is the
> project-specific layer that sits beside it. The spec stage treats
> Repository Context facts, not this file, as the source of truth.

## Role

- [Describe the engineering role and decision stance for this project]

## Project Objective

- [One-paragraph objective; incremental delivery plus the core architecture stance]

## Non-Negotiable Architecture Rules

### Layering

- Presentation / UI:
- Application / Controller:
- Data access / Repository:
- Core / infrastructure:

### Navigation And State

- Single source of truth:
- How UI reaches navigation (state-driven vs direct):
- Derived-state rules:

### Data / Offline-First Contract (if applicable)

- Write path (local / pending / sync):
- Sync strategy:
- Compatibility rule for later phases:

### Technology Stack (Frozen)

- Language / framework:
- State management:
- Networking:
- Persistence:
- Other pinned choices:

## Forbidden

- [e.g. UI calling APIs directly]
- [e.g. application layer bypassing repository]
- [e.g. multiple competing state sources]

## Phase Governance

- Project phase definitions live outside the Harness, for example under
  `docs/phases/`.
- Do not record the active phase in this constitution.
- Every task identifies its governing phase definition when SPEC starts.
- SPEC records the governing phase path and verifies that the task remains
  within its allowed scope and contract gates.
- Crossing a phase gate requires `BLOCKED` or `NEEDS_REVISION`, not silent
  scope expansion.
- Phase completion and advancement require an explicit human decision.
