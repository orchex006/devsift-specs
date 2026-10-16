# Repository ownership

- `orchex006/devsift-specs`: specifications, acceptance requirements, plans, live ledger, maintainer skills, governance, historical references and review evidence.
- `orchex006/devsift`: consumer skill, Python runtime, native analyzers, schemas, policy defaults, runtime tests, build/CI and usage docs.

The live ledger moved from code to specs without changing acceptance state. `reference/bootstrap/ledger.json` preserves the old initial fixture. Older session evidence describing a frozen specs ledger records the previous arrangement and is not current policy. Source commits in evidence remain code-repository commits; moving documents does not move Git history.

Use the specifications repository for planning tools. Resolve source paths recorded by jobs against the explicitly selected code checkout, not the specs root. Do not copy specification assets back into code. Old bootstrap scripts are historical and refuse existing repositories; never rerun them to recreate the old layout.

The consumer skill is installed separately into the host skill directory; install the Python package into the environment used by that host. From a consumer Git root it calls `python -m devsift`. Native tools require explicit trusted configuration. Unsupported reports and incomplete scans must remain clearly identified.
