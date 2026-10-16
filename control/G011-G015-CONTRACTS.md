# G011–G015 session contracts

This document records the original G011–G015 delivery. The user subsequently
authorized autopilot across following ready goals on 2026-10-16. Current ready
autopilot jobs are T055/G019 and T061/G021 on isolated branches, kept out of runtime
PR #8. Existing G016/G017/G020 ownership remains unchanged. G014 artifacts shared by
`controller_g014` are consumed after source/review verification; the separate
authorization registry is preserved rather than overwritten by this session.

Runtime integration branch `feature/g011-g015-analysis-reporting` and its primary
code checkout are owned by this session. Other delivery branches must integrate
in their isolated worktrees. Do not switch or pull another controller's primary
checkout while its runtime changes/tests are active. Ledger updates here use a
fresh-read compare-and-swap guard and preserve unrelated fields. Canonical scope
is the authorization union; this session's own dispatch remains G011–G015.

T037 reviewed source `09d39c2` is integrated. `report_model.assemble_report` returns
a sealed immutable `Report`/`ReportCase`, with fresh `.to_dict()` and exact
`.find_case()`. Source is re-proved, imported lifecycle defaults UNKNOWN,
`trusted_lifecycles=True` is only for actual in-process classifier integration.
All case fields already exist with explicit unknown/pending defaults; no patch,
consumer measurements or approval is invented. Context arrays start empty.

T038 renderer owns only `markdown_report.py` and its tests/docs. T039 will own JSON
and SARIF serializers. Consumers wait for acceptance before claiming their
contracts. T041 substantive risk/context additions may require reviewed model
extension and serializer handling; do not bypass seals or silently drop nonempty
context. All source-bearing references still require actual immutable reproof.

T043 reviewed submission is `9f237e8` (pending independent acceptance). CLI `ci`
supports explicit manifest/digest, actual `--base`, `--all`/`--changed`/exact-file
`--paths`, `--security` and supported `Critical`/`Error` minimum severity.
`ci_gate.run_ci` returns `CiRun.scan_record()` (actual scan envelope) and
`.to_dict()` (CI envelope). Native/source work runs now; dirty clean bytes fail
the immutable HEAD check. Independent security review remains distinct from
legacy quality blocking. No report JSON is accepted as an authoritative CI scan.

T043 final reviewed source `3b1b8a3` is now accepted and integrated. T044 immediately
owns `cli.py`/`cli_scan.py` for report output and CI artifact integration; doctor
flags remain isolated until that next accepted handoff. Do not apply them in this
primary checkout or switch its branch. T044 waits for accepted T039 exporter
contracts before consuming or editing their files/workflows. No overlapping edits,
automatic installation during scans or implicit release is authorized here.

Shared T040 source `5352b1d` (only its three files) was independently checked by
this session's reviewer against the current runtime and merged separately here;
controller integration ran its nine actual Git tests successfully. Other-owner
G016/G017/G020 runtime artifacts are not included by that merge.

T039 is accepted at `253d94496024c6d25bf7420ab924ae867e4de596`, integrated as
`f4491d98eba26e65fac83d24187e245fcb8320d1`. T041 can consume JSON/SARIF serializers;
the current serializers deliberately reject nonempty contextual recommendations
until their handling is independently reviewed. T044 integrates only the public
`assemble_report`/`render_*` APIs, so compatible accepted model extensions can be
consumed after review. Please record exact T041/T042 source commits for scoped
integration into the G011–G015 runtime branch; no full foreign branch merge.

The runtime draft PR for this session is #8. The shared canonical specs checkout
has other-controller cards/evidence/AGENTS changes: their owning controller should
commit those artifacts and keep source references intact before any final shared
ledger delivery. This session will not discard or silently stage those files.

T044 is now accepted at `9ce8cf369f7e6930449372abe2491a439c4576e2` after independent
review and actual Windows/Linux quality workflow `38895632235` success. CLI path
ownership is released for the other controller's isolated Doctor/case wiring.
Please base that isolated integration on the accepted CLI source and preserve
`scan --security`, `--report-format`, `ci_artifacts.attach_reports`, and the actual
in-process CI lifecycle/policy trust boundary. T045 changes only CI cache/test/docs
paths and does not retain CLI locks. Do not switch or modify this primary checkout.

Accepted T041 source `47c757f7aecc4e762e96a6b51a071dc2506e36a4` is now separately
merged as `29bf1cc88db96f1a06e5ff08fb71c007d3a719ec`. Root compatibility checks ran
its actual Git context tests, with official schema integration additionally enabled.

T042 compatibility issue found before integration: source `35f63e3` imports
`case_prompts` and `case_approval` (G016), which are absent from this strictly
G011–G015 branch. T042 depends on T041, not G016. Please keep the mixed baseline/
source/export fixtures independently runnable on accepted G011–G015 APIs: move
the G016 approval integration check to its owning G016 tests, or replace that part
with assertions on the existing sealed report case prompts/pending approval.
This controller will consume only scoped T042 fixtures/docs/tests after that
dependency is resolved; it will not merge G016 runtime modules to make tests pass.

Resolved in this consumer branch at `0f49505001d17186771f860fad07605f7bd42e62`:
scoped T042 fixtures/tests/docs are integrated with the G016-only test segment
replaced by sealed report prompt/pending-approval assertions. No production module
changed. Independent reviewer accepted the scoped variant; the changed real Git/
schema group passed in 25.800s, and controller integration ran all three groups
with official schemas enabled in 136.403s. The first two fixture groups and all
seven source fixtures match original `35f63e3` byte for byte. Foreign canonical
T042 acceptance/source/ownership remain intact; no G016 runtime files are included.

Delivery closure: runtime PR #8 merged as `f9ba7eec7fded3d6d3f479ee93c5c5a3372f8ebe`
after all eight required checks passed; specs PR #8 merged as
`dfd9037c643d1d8b6c4de1e24be306156aade355` after both platform checks passed.
All five G011–G015 goals and fifteen tasks are accepted. Their completed owned
worktree folders were removed with source refs/cleanup evidence retained.

Autopilot canonical branch is now `docs/autopilot-next-goals` in the same specs
checkout; branch rename preserved every dirty file. Do not replace its live ledger
from the older isolated specs worktree. Existing task owners stay unchanged.
Future runtime integration lives in `worktrees/autopilot-next-goals`, branch
`feature/autopilot-next-goals`, draft code PR #10. T055 and T061 are accepted there;
T056 is accepted in specs (its explicit source_repository is devsift-specs, in line
with the repository separation). T057 and T062 are the current following jobs.
The primary code checkout is clean main at the merged G011–G015 tree.

Integration advisory for the G014/G016/G017/G020 owner: runtime PR #9's older
`01e0d3d` Windows runtime run `38899831021` failed two Doctor metadata tests:
`test_explicit_valid_policy_and_missing_cache_are_read_only` and
`test_valid_json_and_cache_metadata_preserve_bytes_without_enumerating_children`.
Valid explicit policy/cache paths returned incomplete. `_diagnostic_path` checks
the caller's absolute spelling against the already-resolved root before resolving
that spelling; Windows TEMP 8.3 aliases are a possible cause (also observed during
T044 fault injection). Preserve the original-component reparse walk and final
canonical containment/identity guards when correcting the alias case. This is an
advisory, not a claim/status change or permission to weaken link/traversal checks.
T052 now runs from accepted T051 `33a9550`; its package changes remain isolated.

Autopilot closure update: G019/G021 independently accepted sources integrated in
runtime PR #10, final reviewed head `8504c0340374f73869a69006c2840d0a762c56e5`.
All eight final Windows/Linux checks passed; optional SARIF service publishing
was skipped by configuration. PR #10 merged as
`8d9c97f6902521b6daafcdb9b38cb35aacff84dd`. Primary code checkout is clean main
at that commit. The completed `autopilot-next-goals` folder was removed; refs
remain. Following G018/G022/G023/G025 artifacts integrate in ignored
`devsift/worktrees/autopilot-packaging-policy`, runtime draft PR #11.
G025's three tasks are independently accepted there. G018 archives are source
ZIP bundles, not reproducible wheels/native binaries; installation/rollback
verification remains T054. Shared canonical specs ownership remains unchanged.

G024 handoff to `controller_g014`: the new `autopilot_luna_final` authorization
and explicit routing are respected. Root's public claim attempt was correctly
denied; no T070 job or worktree was created. T054 is now accepted at source
`b1a9cd61db980d48c0f5673d4c2d69d70c97f532`, with actual hosted mandatory offline
installation/rollback passing Linux9.725s and Windows27.478s on integrated
`0a0dc1b4432eff0036bd21a1232b0a647ea1d6a5`, run38912637912. T069 is accepted at
`ea8f24056edea563f5952a178bc73b66fa9b8b0a`, integrated as
`289a1cbe33362fab966fbb8214a79aa8bc2b6ec1`; all G018/G023 prerequisites are
accepted. Use that runtime lineage (PR #11), which contains accepted T052/T053
packaging, T064 policy discovery, T067 gate, T068 bounded artifact checker and
T069 acceptance fixtures; main8d9c97f alone predates them. Root is freezing final
release-independent docs and will merge PR #11 after exact-head8checks pass.
No G024 authoring is performed here. All canonical mutation writers must now
hold the accepted `ledger_lock`; new ownership uses `apply_claim` with the
correct named authorization and existing goal route. Do not nest admission in
that mutex or modify a worktree's frozen ledger.

Read-only standards research available for release docs: SemVer2.0.0 official
https://semver.org/spec/v2.0.0.html ; SPDX2.3 pages now redirect to the official
2.3.1 maintenance text https://spdx.github.io/spdx-spec/v2.3.1/ . Product license
and release version remain owner-unselected; SPDX metadata licensing is distinct
from product license. No tagged release, publication or license choice implied.

Read-only G024 documentation advisory for its owner (source `75dfa10`): T071's
acceptance explicitly names SemVer and SPDX/license. The reviewed draft/checklist
currently records unknown licenses and source manifests but does not explicitly
name/link the SemVer policy or SPDX identifiers. Please cover those bounded
requirements before closing T071, preserving the current development placeholder
and owner-unselected product license; official references are above. After the
actual T072 dry run, reconcile statements that still call that run merely
planned. T054 installation/rollback is already observed on both OS for the
accepted implementation; distinguish that scoped proof from still-pending
release-specific evidence for a future chosen candidate. This is a read-only
advisory, not a task claim or an edit to the G024 owner's files.

Runtime PR #11 is now MERGED as
`8c9a2c6db43f6fd069d746a21a189ca214bf9c68` after all eight required checks passed
at independently reviewed source `86712822f7e95f45da3fd0661e7418ebff26e6b1`.
Primary code checkout is being fast-forwarded and its tree checked against that
exact tested source. G024 owner should consume this main lineage before its
final CI; the difference from your base289 is reviewed final docs only. Root
will remove only its completed packaging integration worktree, preserving G024
folders and all branch refs. Full audit includes actual 2OS package rollback,
policy protected reads, security/ZIP bypass fixtures, report schemas/byte equality
and observed exact-key NuGet cache hits; service publishing remains skipped.
