---
name: devsift-checkpoint
description: Write a concise work handoff when pausing DevSift development, or resume by checking current repository state.
---

On an actual request to pause, record unfinished scope, branches, uncommitted files, held decisions, blockers and the next action using templates/SAVEPOINT.md. Keep the handoff in the specifications repository. Do not create restore snapshots, duplicate repositories or per-task checkpoints. Git preserves committed history. On resume inspect actual Git status and the live ledger; never restore files or assume old locks are still held.
