# Concurrent authorized DevSift sessions

Two independent user-authorized sessions share this checkout and the single execution ledger.

- Existing G011-G015 session owns its claimed security, observability, report model/rendering and CI tasks.
- The current session received the explicit user instruction: `ดำเนินการต่อหน่อย G020 , G017 , G014 , G016`. Controller `controller_g014` owns the already claimed T040, T049, T050, T058 and their dependent work when prerequisites become accepted. Workers are implementer_1/implementer_2, reviewer boundary_reviewer. Integration worktree: code/worktrees/delivery-g014-g020; branch feature/g014-g016-g017-g020.

A session's narrower selected scope does not revoke another session's direct user authorization. Do not supersede, reset, archive, or clean another session's jobs/worktrees. Read execution.authorizations in the live ledger before changing another owner's status. Only each task owner changes its claim/status; preserve unrelated state with fresh-read compare-and-swap updates. Selected goals are the union of active authorized sessions, not a replaceable session-local field.

T040 is shared G014 scope and already owned by controller_g014; the G011-G015 session should skip it. T041 waits for accepted T039; T046 waits for accepted T037; T051 waits for all its existing prerequisites. No review state unlocks dependents. Share accepted source SHAs through the ledger. No additional restore checkpoints or workspace clones are needed.

CLI handoff: T043 now owns shared devsift/cli.py and cli_scan.py until accepted. T059 continues doctor module/config diagnostics only; its already-prepared CLI config flags remain an uncommitted isolated diff and will be integrated after T043 releases the path. No concurrent CLI writes by controller_g014 during this handoff.

Goal-level routing: controller_g014 owns all tasks of G014 (T040/T041/T042), G016 (T046/T047/T048), G017 (T049/T050/T051) and G020 (T058/T059/T060) under the explicit new user request. This includes the independent G014 entry T041 after accepted T039. The G011-G015 session owns G011/G012/G013/G015 prerequisites and should skip all G014 claims, not only T040. No task is claimed before prerequisites are accepted.

Current shared CLI handoff: T043 is accepted; T044 now owns CLI integration until accepted. controller_g014 keeps Doctor config flags and case CLI tests in its isolated worktree and will commit combined Doctor/prompt entry wiring after T044 releases the path. Please hand back CLI after T044; T045 CI tests can run independently.

Current delivery update (2026-10-16): T043/T044/T045 are accepted and their shared CLI handoff is complete. Controller_g014 integrated final Doctor/case CLI, isolated consumer invocation and host Git selection at runtime source `345d55b`, independently accepted for T048. All G014/G016/G020 tasks are accepted. T051 is now claimed by implementer_1 in `devsift/worktrees/g017-full-gate` after every prerequisite became accepted; source base `01e0d3d` includes runtime main `f9ba7ee`. Draft runtime delivery PR: https://github.com/orchex006/devsift/pull/9 . Preserve this session ownership while the other session proceeds with its separately authorized later goals.
