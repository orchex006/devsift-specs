# DevSift Specifications

This repository owns product specifications, requirements, acceptance criteria, goal/task cards, the canonical execution ledger, development orchestration skills and review evidence. [devsift](https://github.com/orchex006/devsift) owns the consumer skill, Python CLI, native analyzers, runtime tests and usage documentation.

The live plan is [plan/ledger.json](plan/ledger.json), migrated from code without changing task acceptance states. The old planning fixture is [historical bootstrap reference](reference/bootstrap/ledger.json), not live execution state.

The code checkout still contains the prior ledger snapshot while [code PR #7](https://github.com/orchex006/devsift/pull/7) is pending. Both snapshots record the same 32 accepted tasks through G010. The runtime cleanup is a separate migration; this progress update does not approve or merge it. Do not advance the two copies independently. See [current migration state](docs/REPOSITORY-SEPARATION.md).

```sh
python tools/planctl.py validate
python tools/validate_kit.py
python -m unittest discover -s tests -v
```

Read [product requirements](docs/SPEC-V6.md). Maintainer skills here guide development. The consumer skill exists only in code. Bootstrap tooling is historical and must never be rerun against existing repositories.
