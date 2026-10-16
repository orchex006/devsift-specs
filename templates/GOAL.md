# G<NNN> — <measurable outcome>

Maintainer template; fill only for explicitly authorized tracked work. It is not
consumer skill content. Unfilled placeholders are not evidence or authorization.

- Canonical ID: G<NNN>; derived alias: GA<NNN> or GB<NNN>.
- User authorization/reference and selected scope: <reference; exclusions>.
- Source repository: <orchex006/devsift or orchex006/devsift-specs>.
- Outcome and observable acceptance: <behavior/artifacts and verification>.
- Required task IDs: <canonical IDs, each owned by this goal exactly once>.
- Optional work: <unselected ideas, not dispatchable; no filler tasks>.
- Ownership: <exact repository paths and shared contract locks>.
- Active budget: <implementation + independent review + integration, total <=165 minutes>; remaining: <measured/unknown>.
- Status/evidence: <actual status and evidence links, or pending/none>.

## Structural entry paths

Compute from the actual task DAG, including transitive predecessors. A true entry
has no direct OR transitive predecessor in this goal. Do not derive class from
numeric ordering, task status or a union of different entry paths.

| True entry task | All transitive predecessor IDs | Full predecessor-goal gates on this entry | Partial task prerequisites by goal | Accepted/blocking evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| <TNNN> | <IDs or empty> | <goals whose entire required task set is in this path> | <goal: subset IDs> | <accepted SHA/review/integration, or blockers> | <wait/claim when authorized and locks/capacity free> |

Class rationale: <B iff EVERY true entry has a full predecessor-goal gate;
A iff ANY true entry has none>. An A path can still be blocked. A B path can
start independently once its own prerequisites are accepted. Recompute aliases
only on graph changes; preserve canonical IDs and migration evidence.

## Completion

- [ ] Every required task independently reviewed and integrated with actual evidence.
- [ ] Each entry's prerequisites accepted before claim; in_review never unlocks.
- [ ] Exact source_repository, author/reviewer, source and integrated SHAs, commands/results and limits recorded.
- [ ] No unselected optional work, release or unauthorized consumer changes.
- [ ] Controller verified integration, updated canonical ledger, released locks and refreshed readiness.

Next action: <one concrete eligible action or named blocker>.
At a real budget/complexity overrun, stop expanding scope and record a bounded
split with authorization; do not claim completion. At an actual pause only, use
a plain handoff with unfinished work and next actions, never restore snapshots
or automatic per-task checkpoints.

Compact mode: retain ID/alias, authorization, outcome/repository/locks, required
IDs, budget, EVERY entry-path row/rationale, evidence/status and next action in
one short card. Acceptance and independent review gates are unchanged.
