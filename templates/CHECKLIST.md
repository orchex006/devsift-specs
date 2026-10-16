# Maintainer execution checklist

Copy only into authorized maintainer work in devsift-specs. Check a box only
when its stated event happened and evidence is attached. Use `not applicable:
<reason>` for excluded checks; do not mark unrun checks passed. Keep unknowns
and limitations visible. This checklist never creates a goal from conversation.

## Before claim — Controller

- [ ] User selected this work; exact scope/repository and canonical task/goal identified.
- [ ] Task DAG validates; transitive A/B and each true entry's gates computed separately.
- [ ] Every prerequisite accepted with distinct review and integrated evidence; in_review is blocked.
- [ ] Owner, exclusive path/contract locks, lease, source repository and full base SHA reserved.
- [ ] Actual host capacity checked; serial-fallback used when delegation is unavailable. No assumed host API or nested quotas.
- [ ] Goal budget including review/integration <=165 active minutes; bounded task share assigned.

## Before submission — Author

- [ ] Read actual source status, applicable instructions, accepted contracts and task criteria.
- [ ] Changed only owned paths; target governance and user authorization preserved.
- [ ] Relevant verification actually ran; commands, repository, results, evidence and limits recorded.
- [ ] Full source_repository/base_sha/commit_sha and changed paths supplied; no release/publication claim.
- [ ] Risks, rollback and concrete next step supplied; status submitted for independent review.

## Before accepted — Distinct reviewer and Controller

- [ ] Reviewer differs from author and checked exact source/base SHA, scope, evidence and relevant negative cases.
- [ ] Rework, missing proof, incomplete checks and unresolved risks are explicitly recorded; none treated as acceptance.
- [ ] Controller integrated reviewed artifact; full integrated repository/SHA and actual integration checks recorded.
- [ ] Controller alone updated canonical ledger to accepted, released locks and recomputed readiness.
- [ ] Goal complete only when all required tasks accepted; optional unselected work not dispatched.
- [ ] Clean completed worktree removed only after integration or documented supersession with refs preserved; dirty/unique work retained.

Compact mode: use one line each for authorization/prerequisites, ownership/base/
budget, implementation/checks, independent review, integration/acceptance and
next action. Evidence and truthful check states remain mandatory. Do not create
per-task checkpoints. Write a plain handoff only when actually pausing; preserve
unfinished changes, refs, locks, blockers and next actions without snapshots.
