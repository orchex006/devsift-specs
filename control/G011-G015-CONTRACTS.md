# G011–G015 session contracts

This controller implements only the user's G011–G015 request. It does not dispatch
G016/G017/G020 work or modify another owner's claims. G014 artifacts shared by
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
