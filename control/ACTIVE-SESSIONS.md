# Concurrent authorized DevSift sessions

The single live ledger is `devsift-specs/plan/ledger.json` in the primary specs checkout. Runtime, consumer skill and native tests belong to `devsift`; specs, governance and execution metadata belong to `devsift-specs`. Ignored worktrees are temporary Git checkouts, not additional sources of truth.

## Current ownership

- `controller_g014` received the direct user request: `ดำเนินการต่อหน่อย G020 , G017 , G014 , G016`. It owns G014/T040–T042, G016/T046–T048, G017/T049–T051 and G020/T058–T060. Team: implementer_1, implementer_2 and independent boundary_reviewer. All 12 tasks are accepted. Final runtime source `ebf1705ffa3393d9017b0ebf8fff9f6b2583697d` is on runtime [PR #9](https://github.com/orchex006/devsift/pull/9); specs [PR #9](https://github.com/orchex006/devsift-specs/pull/9) records the evidence. All8final Windows/Linux checks passed and runtime PR #9 merged into main `58232337a064637e4038d93b604ee174692f6086`. Specs evidence is finalized through specs PR #9. Delivery branches are `feature/g014-g016-g017-g020` and `docs/g014-g016-g017-g020`; the clean runtime integration worktree was removed after main ancestry/tree verification; the specs integration worktree is removed after its PR merges. Branch refs are retained.
- The other `controller` owns G011/G012/G013/G015 and separately authorized later autopilot goals. Preserve its existing jobs, branches, worktrees and statuses; the live ledger records their current state. G014 is exclusively routed to controller_g014, despite overlap with the earlier G011–G015 request.

## Shared contracts

A session's narrower scope does not revoke another session's direct authorization. Never supersede, reset, archive or clean another owner's work. Read `execution.authorizations`, `execution.goal_controllers` and current jobs before writes; only the task owner changes its state. Use fresh-read compare-and-swap ledger updates and preserve other-session progress. Selected goals are the union of authorized sessions.

Only accepted prerequisites unlock downstream work. No in_review state grants acceptance. Source commits and review history are recorded in the ledger and goal evidence; do not replace them with a second task tracker.

The T043/T044 shared CLI handoff is complete and the controller_g014 lease is released. Preserve accepted Doctor `--policy`/`--cache-path`, explicit case `--scan-input`/`--approval-file`, isolated installed `-I -B` invocation and outside-consumer host Git selection in later merges. The Windows 8.3 correction `93ad8ea` is included in final candidate ebf1705 and has passed actual hosted Windows regression reproof; do not consume the earlier uncorrected 33a9550 alone as a final delivery base.

Final CI runs: runtime `38901823874`, native `38901824152`, installed `38901824220`, quality `38901823972`. Runtime, installed and quality checks pass on both OS; native Linux and Windows pass, including all3T051 groups and actual Windows alias regressions. This is component acceptance, not a package release or automatic source-edit authorization.

Checkpoint means a plain unfinished-work handoff only when actually pausing. Do not create restore snapshots, cloned workspaces or per-task checkpoints. Remove only completed clean integrated worktrees, retaining branch refs and preserving active other-session work.
