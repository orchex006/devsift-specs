# Concurrent authorized DevSift sessions

Two independent user-authorized sessions share this checkout and the single execution ledger.

- Existing G011-G015 session owns its claimed security, observability, report model/rendering and CI tasks.
- The current session received the explicit user instruction: `ดำเนินการต่อหน่อย G020 , G017 , G014 , G016`. Controller `controller_g014` owns the already claimed T040, T049, T050, T058 and their dependent work when prerequisites become accepted. Workers are implementer_1/implementer_2, reviewer boundary_reviewer. Integration worktree: code/worktrees/delivery-g014-g020; branch feature/g014-g016-g017-g020.

A session's narrower selected scope does not revoke another session's direct user authorization. Do not supersede, reset, archive, or clean another session's jobs/worktrees. Read execution.authorizations in the live ledger before changing another owner's status. Only each task owner changes its claim/status; preserve unrelated state with fresh-read compare-and-swap updates. Selected goals are the union of active authorized sessions, not a replaceable session-local field.

T040 is shared G014 scope and already owned by controller_g014; the G011-G015 session should skip it. T041 waits for accepted T039; T046 waits for accepted T037; T051 waits for all its existing prerequisites. No review state unlocks dependents. Share accepted source SHAs through the ledger. No additional restore checkpoints or workspace clones are needed.

CLI handoff: T043 now owns shared devsift/cli.py and cli_scan.py until accepted. T059 continues doctor module/config diagnostics only; its already-prepared CLI config flags remain an uncommitted isolated diff and will be integrated after T043 releases the path. No concurrent CLI writes by controller_g014 during this handoff.
