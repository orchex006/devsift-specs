# DevSift Specifications

This repository owns product specifications, requirements, acceptance criteria, goal/task cards, the canonical execution ledger, development orchestration skills and review evidence. [devsift](https://github.com/orchex006/devsift) owns the consumer skill, Python CLI, native analyzers, runtime tests and usage documentation.

The live plan is [plan/ledger.json](plan/ledger.json), migrated from code without changing task acceptance states. The old planning fixture is [historical bootstrap reference](reference/bootstrap/ledger.json), not live execution state.

The runtime separation is complete in [code PR #7](https://github.com/orchex006/devsift/pull/7), with all Windows/Linux CI checks passing. There is no code-ledger copy. Use the specifications ledger for all future coordination.

```sh
python tools/planctl.py validate
python tools/validate_kit.py
python -m unittest discover -s tests -v
```

Read [product requirements](docs/SPEC-V6.md). Maintainer skills here guide development. The consumer skill exists only in code. Bootstrap tooling is historical and must never be rerun against existing repositories.
