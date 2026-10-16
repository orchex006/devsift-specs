# Working on DevSift specifications

This repo owns product design and execution coordination. The code repo owns consumer skill/runtime. Use one canonical plan/ledger.json here; reference runtime artifacts by code repository commit. Historical bootstrap files describe the initial setup and are not current operating instructions.

Run `python tools/planctl.py validate`, `python tools/validate_kit.py`, `python -m unittest discover -s tests -v` and `git diff --check`. Run runtime/native/installed CLI checks in the selected code checkout according to its DEVELOPMENT.md. Plan source paths must be resolved against that checkout explicitly.

Use Conventional Commits, scoped branches and independently reviewed PRs. Preserve IDs, dependency DAG and accepted evidence. Controller serializes task/lock updates and marks accepted only after independent review plus actual integration. Allocate ready work according to authorized scope and available host capacity; never infer approval from a plan. Preserve dirty work and unique commits; use ignored worktrees/<job> for parallel jobs.

Before an actual pause, record a concise handoff using templates/SAVEPOINT.md. Include current branches, unfinished changes, blockers and next actions. No restore snapshots or automatic per-task checkpoints. Resume inspects real status and current ledger. Do not publish packages or releases as part of specification maintenance.

Use `tools/resource_claims.py` for cooperative canonical ownership admission and
hold its `ledger_lock` for the full transaction in every other ledger writer.
See [resource ownership](docs/RESOURCE-OWNERSHIP.md) for the shared OS lock,
accepted-prerequisite gates, global contracts and explicit controller routing.
Task status, authorizations and accepted review still belong to the canonical
ledger; the lock file is transport, not another tracker or an approval engine.

Create isolated jobs only under this repository's ignored `worktrees/<job>`, for
example `git worktree add worktrees/example -b feature/example HEAD`. After
independent acceptance and integration, verify clean status and ancestry (or a
documented reviewed replacement), then remove the finished folder with
`git worktree remove worktrees/example`. Preserve branch/commit references and
cleanup evidence. Never remove active, dirty or unique worktrees. Code jobs use
the same convention inside the explicitly selected code repository. A worktree's
checked-out ledger is historical context; all live coordination uses the one
primary specs ledger.
