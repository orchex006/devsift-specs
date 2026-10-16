# DevSift Specifications

Approved product and engineering specifications for [DevSift](https://github.com/orchex006/devsift). This repository preserves the v6 design and bootstrap kit. Runtime implementation, pull requests, and the canonical execution ledger live in the [code repository](https://github.com/orchex006/devsift). Completed goal/task checklists mirror accepted implementation; see [execution progress](plan/EXECUTION-STATUS.md). The bundled ledger remains the original planning fixture; the code ledger is authoritative.

**Language-agnostic developer quality intelligence — specification and implementation progress.**

DevSift aims to detect code-quality and security issues as changes are developed, link findings to verified source locations, explain human-readable risk and provide narrowly scoped agent remediation prompts. New code can be gated; existing legacy code is recommendation-first. Code scanning never silently refactors production services.

**Repository:** https://github.com/orchex006/devsift  
**Stage:** G000 bootstrap, G001 policy and G002 CLI foundations accepted in the code repository. Analyzer/report engines and package release remain pending.  
**Independence:** usable in arbitrary projects; AgriMap, Axiom and Drevqon are optional integrations, not architectural dependencies.

## Command interface reference (CLI shell implemented; analyzers pending)

```bash
devsift scan --changed
devsift scan --all --legacy-mode recommend
devsift report --latest
devsift explain OBS-001
devsift prompt OBS-001 --mode review
devsift doctor
```

## Implementation progress

[G000](plan/goals/G000.md), [G001](plan/goals/G001.md) and [G002](plan/goals/G002.md) are accepted. Their goal and task checklists mirror verified code-repository execution and link to its evidence. See the [progress summary](plan/EXECUTION-STATUS.md) and [canonical execution ledger](https://github.com/orchex006/devsift/blob/main/plan/ledger.json).

The initial planning fixture in this repository remains unchanged for the original DAG tests. Commands below validate that fixture and the specification kit; they do not describe live execution readiness.

```bash
python tools/planctl.py validate
python tools/planctl.py frontier
python tools/validate_kit.py
python -m unittest discover -s tests -v
```

These offline commands validate the plan and files; **they do not push commits, install software or scan product code**. All implementation begins at `plan/GOALS.md` and `plan/ledger.json`, following `AGENTS.md` and `DEVELOPMENT.md`.

## Source layout

- `AGENTS.md` / `DEVELOPMENT.md`: repo-only policy, branching, worktrees, agent orchestration, review and savepoints
- `plan/`: 26 goal cards, 77 task cards, one canonical ledger, A/B entry-path decisions and first-frontier dispatch
- `skills/`: development planning/execution/checkpoint plus planned `$devsift` consumer entrypoint
- `docs/`: bootstrap runbook, repository identity, report contract, open-source process, source study and checklists
- `reference/v4/`: frozen historical source-aware lint specification; **not installed as functional engine**
- `.github/workflows/`: starter plan/test validation only; other planned quality gates come from implementation tasks

## License and maturity

Public visibility does not grant an open-source license. The repository owner has not selected a license; do not claim OSI-approved licensing, publish a package or tag a release without proper authorization and verification. See `CONTRIBUTING.md` and `SECURITY.md`.
