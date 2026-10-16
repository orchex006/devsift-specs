# T<NNN> — <bounded deliverable>

Maintainer template; use after authorization and dependency/ownership checks.
This card does not itself claim work or grant a worker integration permission.

- Goal: <canonical GNNN; derived GANNN/GBNNN and entry path>.
- source_repository: <explicit repository owning changed files>.
- User scope/reference: <authorization; non-goals>.
- Direct depends_on: <actual task IDs or empty>; transitive prerequisites: <computed IDs>.
- Accepted prerequisites: <each artifact SHA + independent review + integrated evidence>; blockers: <IDs/status>.
- Status: <pending/claimed/running/in_review/accepted/blocked/paused/rework>; evidence: <actual links or none>.
- Author/controller: <identities>; independent reviewer: <distinct identity or unassigned>.
- Exact owned paths/symbols: <allowlist>; forbidden paths: <exclusions>.
- Exclusive locks: <repository/path prefixes + shared contract IDs, owner/lease>.
- source_repository base_sha: <full SHA>; branch: <name>; worktree: <repo>/worktrees/<job> or serial-fallback.
- Applicable rules: <AGENTS/DEVELOPMENT/task/contracts, versions or hashes>.
- Goal active budget: <total <=165 minutes>; task allocation/remaining: <bounded share>.

## Deliver and verify

Outcome: <one observable bounded result>.
Acceptance: <concrete assertions, positive/negative cases, relevant evidence>.
Inputs/outputs: <accepted producer APIs, fixtures and produced artifacts>.
Verification: <actual commands, working repository, expected behavior; no invented successes>.
Safety/limits: <read-only/authorization boundary, unknowns, excluded capabilities>.
Rollback: <bounded reversal and preserved commit refs; no destructive reset>.

- [ ] Controller verified authorization, accepted prerequisites, exact base and free locks/capacity before claim.
- [ ] Author inspected actual state and applicable rules; preserved unrelated work.
- [ ] Scoped implementation/docs complete; relevant checks actually executed.
- [ ] Submission includes changed paths, diff, full source SHA, commands/results, evidence, risks and next action.
- [ ] Distinct reviewer checked the submitted SHA and scope; result/evidence recorded.
- [ ] Controller integrated and verified the result, recording repository + integrated SHA and checks.
- [ ] Only then Controller marked accepted and refreshed readiness; unaccepted/rework never unlocks consumers.

Worker return: source_repository=<repo>; base_sha=<SHA>; commit_sha=<SHA>;
changed_paths=<list>; test_command/result=<actual>; evidence_uri=<link>;
risk/limits=<text>; rollback=<text>; next_step=<text>; status=in_review.
Do not substitute a specs SHA for a runtime SHA or vice versa. Producer contract
acceptance precedes dependent implementation. Workers do not self-claim extra
work, spawn nested quotas, push/merge/publish, mark accepted or clean worktrees.

Compact mode: collapse into identity/repository/authorization, prerequisites and
accepted proof, ownership/base/budget, outcome/acceptance, actual verification,
submission/review/integration evidence and next action. Keep all gates. On a
real pause, add a plain handoff; no automatic checkpoint or restore snapshot.
