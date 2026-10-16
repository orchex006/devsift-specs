# DevSift specifications maintainer policy

Scope: `orchex006/devsift-specs`. This repo owns requirements, acceptance criteria, the single live plan/ledger.json, task/goal cards, governance, maintainer skills and review evidence. Runtime, consumer skill, native builds and runtime tests belong to the explicitly selected `orchex006/devsift` checkout. Do not mirror the ledger or consumer skill.

Before writes inspect status, branch, applicable rules, user scope, ledger and accepted prerequisites. Validate with `python tools/planctl.py validate`; inspect frontier. Controller owns ledger transitions, exclusive path/contract locks and integration. Claim only authorized ready work. Independent reviewer acceptance and actual integrated evidence are required for accepted status; in_review does not unlock downstream. Do not mark incomplete work accepted during migration.

Use scoped branches and reviewed PRs, no direct main writes, force push, broad staging, reset or dirty-work deletion. Preserve unrelated changes and source commits in evidence. Use ignored worktrees/<job>; remove only completed clean integrated or documented superseded worktrees with refs retained. Source commits in evidence refer to the code repo.

Scan and review are read-only; consumer repairs require authorization. Never invent capabilities, test results or provenance. Runtime changes and tests happen in the code checkout. Plan-tool tests and validation run here. No release without authorization.

Checkpoint means a plain handoff when pausing work: unfinished work, branches, dirty files, blockers and next actions. Do not create restore snapshots, clone workspaces or checkpoint after every commit/task. Git preserves committed history. Resume checks actual repository state before continuing.
