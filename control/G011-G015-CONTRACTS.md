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
