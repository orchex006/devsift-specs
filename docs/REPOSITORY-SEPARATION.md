# Repository ownership

- `orchex006/devsift-specs`: specifications, acceptance requirements, plans, live ledger, maintainer skills, governance, historical references and review evidence.
- `orchex006/devsift`: consumer skill, Python runtime, native analyzers, schemas, policy defaults, runtime tests, build/CI and usage docs.

The live ledger moved from code to specs without changing acceptance state. `reference/bootstrap/ledger.json` preserves the old initial fixture. Older session evidence describing a frozen specs ledger records the previous arrangement and is not current policy. Source commits in evidence remain code-repository commits; moving documents does not move Git history.

Current integration state: [specs PR #5](https://github.com/orchex006/devsift-specs/pull/5) and [code PR #7](https://github.com/orchex006/devsift/pull/7) are merged. Code PR #7 was independently reviewed and passed runtime, installed CLI and native analyzer checks on Windows and Linux. The code main branch contains no specification/planning assets or duplicate ledger. All 32 accepted task states through G010 are retained in the live specifications ledger. Use that ledger for future coordination.

Use the specifications repository for planning tools. Resolve source paths recorded by jobs against the explicitly selected code checkout, not the specs root. Do not copy specification assets back into code. Old bootstrap scripts are historical and refuse existing repositories; never rerun them to recreate the old layout.

The consumer skill is installed separately into the host skill directory; install the Python package into the environment used by that host. From a consumer Git root it calls `python -m devsift`. Native tools require explicit trusted configuration. Unsupported reports and incomplete scans must remain clearly identified.
