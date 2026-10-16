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

## Final autopilot routing (new direct user authorization)

Controller_g014 now owns the currently unclaimed G024/T070–T072 once accepted prerequisites unlock them. Execution subagents must use `gpt-6-luna` with low reasoning, per the user. Authorization: `execution.authorizations.autopilot_luna_final`; goal routing is explicit in `execution.goal_controllers`. The other controller keeps T069/G023 and its independent review; do not reassign or duplicate that active work. T070 is not claimed or implemented before T069 is accepted. This supplements earlier scope; it does not revoke other claims. No actual tags/package releases or license choice are authorized by this readiness work.

G024 supporting correction: controller_g014 / luna_implementer_2 owns specs `tools/resource_claims.py`, `tests/test_resource_claims.py`, `docs/RESOURCE-OWNERSHIP.md` for proven Windows CRLF false-corrupt admission. See execution.supporting_corrections.g024_windows_ledger_bytes. Existing T065 acceptance/history and other task claims are preserved. Review/source references will be recorded; keep canonical writes binary/atomic under ledger_lock.

## Final G024 delivery closure

All77tasks/all26goals are independently accepted. Luna/low execution and review completed G024 plus the minimal Windows CRLF supporting correction. Final runtime candidate2232c26 passed all8Windows/Linux checks and merged runtime PR12/main329c594; exact tree match and primary runtime checkout verified. Final specs PR11 carries actual candidate source/integrity pins, reviews, blocked-readiness results and source refs. All own worker/candidate/runtime integration worktrees were removed cleanly with refs retained; specs integration is removed after its merge. No further goal is dispatched; publication/owner license/SBOM/sign/release-review approval remain outside this preparation authorization.
