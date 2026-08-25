# Phase <N> – <Name>

> Optional, fill-in at the start of each phase. Records the scope gate that
> applies across all tasks in this phase: which external contracts may be
> touched, which are blocked, and when the phase is complete. The spec stage
> checks each task against this gate and must not cross it. Project facts
> only; delete this usage note when filling. This file is a mechanism, not
> authoritative content.

## Phase Goal

- [What this phase establishes, in one or two sentences]

## API Gate

### Allowed

| Method | Path | Purpose |
|---|---|---|
|  |  |  |

### Blocked

- [e.g. all endpoints under a feature not yet in scope]
- [e.g. any multipart upload]

## Phase Constraints

- [Technical / domain prohibitions for this phase, e.g. "no domain entities yet"]

## Phase Success Criteria

- [Testable, observable exits, e.g. "app authenticates against the real backend"]
