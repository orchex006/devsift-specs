# Maintainer goal, task and checklist templates

[GOAL](../templates/GOAL.md), [TASK](../templates/TASK.md) and
[CHECKLIST](../templates/CHECKLIST.md) are fillable maintainer documents, not
runtime assets or executable orchestration. They belong only in devsift-specs.
Do not install them with the consumer skill or copy them into the runtime repo.
Product invocation follows its consumer instructions and target-project rules;
it does not require these templates or create tracked work from a question.

Use them only after explicit authorization for planning/tracked maintenance.
Read [repository ownership](REPOSITORY-SEPARATION.md),
[A/B semantics](../governance/AB-GOAL-PLANNING.md) and the
[execution protocol](AGENT-EXECUTION-PROTOCOL.md). Existing
[delegation packets](../templates/DELEGATION-PACKET.md) and
[independent review checks](../templates/REVIEW-CHECKLIST.md) remain applicable.
Actual host capacity/capabilities govern execution; documents do not supply a
subagent API. Use serial-fallback when isolation/delegation is unavailable.

## Fill from actual state

1. Select canonical IDs, exact user scope and source_repository. Runtime changes
   point to orchex006/devsift; maintainer governance points to orchex006/devsift-specs.
   Record full base, submitted and integrated SHAs with their repositories.
2. Enumerate actual task edges and one owner per task. Compute transitive
   predecessors and true entry paths; never merge gates from different paths.
   A/B is structural, while readiness uses accepted evidence. in_review is never
   sufficient. Producer APIs must be accepted before dependent implementations.
3. Controller reserves exact files/contracts and available capacity before
   claim. Bound the whole goal to <=165 active minutes including independent
   review and integration; split an overrun explicitly rather than omit checks.
4. Fill observable acceptance, proportionate verification, limitations, rollback
   and next action. A checked box means a verified event, not a plan. Empty
   placeholders, generated files and green tests alone never establish accepted.
5. Submit exact commit/evidence for a reviewer distinct from the author.
   Controller verifies integration and records its SHA/checks before accepted.
   Only Controller mutates the canonical primary plan/ledger.json. A worktree's
   ledger is an immutable planning input for a worker, not another live ledger.

Compact mode shortens presentation, not authorization, A/B reasoning, exact
ownership, budget, truthful verification or review/integration requirements.
Optional ideas remain unselected and undispatched. The current planctl graph
uses each goal's task_ids as its required set; do not invent an optional-task
schema or silently drop members. Any selected graph change requires explicit
coordination, validation and alias migration evidence where classification changes.

## Concrete compact example (illustrative, not a new task claim)

Assume G901 owns required T901 and T902. G902 owns T903 and T904.
T903 depends on T901. T904 depends on T901 and T902. No other edges exist.

| G902 true entry | Transitive prerequisites | Full gates | Partial prerequisites |
| --- | --- | --- | --- |
| T903 | T901 | none | G901: T901 |
| T904 | T901, T902 | G901 | none |

G902 is GA902 (A): at least one true entry has no full-goal gate. If T901
is accepted and T902 is in_review, T903 is structurally ready while T904 is
blocked. Authorization, locks and host capacity must still be checked before
claiming T903. Changing T902 to accepted readies T904 and leaves G902 A.
If the graph instead makes BOTH entries depend on both T901/T902, the alias
becomes GB902; readiness is still per entry. That is a graph migration, not a
status-driven rename. Preserve G902 and old immutable evidence.

A compact T903 card would retain: authorization=<actual reference>;
source_repository=orchex006/devsift-specs; owner/locks=<exact files+contract>;
base_sha=<actual full SHA>; depends_on=T901; accepted proof=<actual review+
integrated SHA>; goal=G902/GA902; budget=<share of <=165 active minutes>;
outcome=<measurable result>; checks=<executed commands/results or pending>;
source commit=<actual SHA or none>; reviewer=<distinct/unassigned>;
integrated commit=<actual SHA or none>; status=pending; next=Controller claim
only after the remaining authorization/ownership/capacity checks. Placeholders
must be replaced from actual evidence before claiming or reporting acceptance.

## Offline verification and limits

Run `python -B tools/planctl.py validate`, `python -B tools/planctl.py classify`
and `python -B tools/planctl.py frontier` in the explicitly selected specs
checkout. The actual graph evaluator rejects missing/duplicate ownership,
unknown references and cycles and derives the entry paths above. It computes
readiness from ledger statuses; it does not authenticate review evidence, enforce
locks, validate every template field or perform integration. Controller and
reviewer must verify those separately. No new schema/parser or host automation
is implemented by these prose templates.

Do not create restore snapshots, clone workspaces or checkpoint every task.
At an actual pause use the existing plain handoff with unfinished work, branches,
dirty files, evidence, locks, blockers and next actions. Resume checks actual
state. Releases and consumer source changes require their own authorization.
