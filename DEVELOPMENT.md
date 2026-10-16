# Working on DevSift specifications

This repo owns product design and execution coordination. The code repo owns consumer skill/runtime. Use one canonical plan/ledger.json here; reference runtime artifacts by code repository commit. Historical bootstrap files describe the initial setup and are not current operating instructions.

Run `python tools/planctl.py validate`, `python tools/validate_kit.py`, `python -m unittest discover -s tests -v` and `git diff --check`. Run runtime/native/installed CLI checks in the selected code checkout according to its DEVELOPMENT.md. Plan source paths must be resolved against that checkout explicitly.

Use Conventional Commits, scoped branches and independently reviewed PRs. Preserve IDs, dependency DAG and accepted evidence. Controller serializes task/lock updates and marks accepted only after independent review plus actual integration. Allocate ready work according to authorized scope and available host capacity; never infer approval from a plan. Preserve dirty work and unique commits; use ignored worktrees/<job> for parallel jobs.

Before an actual pause, record a concise handoff using templates/SAVEPOINT.md. Include current branches, unfinished changes, blockers and next actions. No restore snapshots or automatic per-task checkpoints. Resume inspects real status and current ledger. Do not publish packages or releases as part of specification maintenance.
