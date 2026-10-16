# Autopilot runtime delivery audit

The distinct reviewer accepted exact code source `86712822f7e95f45da3fd0661e7418ebff26e6b1` after all eight required checks passed. [Runtime PR #11](https://github.com/orchex006/devsift/pull/11) merged as `8c9a2c6db43f6fd069d746a21a189ca214bf9c68`. Controller fast-forwarded the clean primary code checkout and verified that its tree exactly matches the tested source. The finished integration worktree was removed with its branch and commit references retained. Active G024 worktrees belong to the separately authorized controller and remain protected.

## Actual hosted execution

All four run API records identify that exact reviewed source and completed successfully on Windows and Linux:

| Workflow | Actual run | Linux | Windows |
| --- | --- | --- | --- |
| Runtime and official schema tests | [38913551687](https://github.com/orchex006/devsift/actions/runs/38913551687) | 548 tests, 44.693s, 99 skipped | 548 tests, 722.521s, 87 skipped |
| Native and regression tests | [38913527934](https://github.com/orchex006/devsift/actions/runs/38913527934) | 548 tests, 131.680s, 20 skipped | 548 tests, 887.456s, 8 skipped |
| Installed CLI and mandatory package proof | [38913527613](https://github.com/orchex006/devsift/actions/runs/38913527613) | Package proof 11.208s; all 5 governance tests pass | Package proof 30.969s; all 5 governance tests pass |
| Quality gate and report artifacts | [38913527943](https://github.com/orchex006/devsift/actions/runs/38913527943) | Complete, exit 0, zero reported cases in declared scope | Same result and report bytes |

Skips are explicit platform/optional groups, not executed acceptance proof. The installed workflow sets `DEVSIFT_TEST_PACKAGE_INSTALL=1`: its actual offline wheel/sdist, fresh installation and synthetic-prior rollback proof runs on both systems without that opt-in being skipped. Existing module/console behavior and all installed governance checks pass.

Both runtime and native logs show the actual POSIX descriptor replacement guard on Linux and actual Windows metadata/8.3 alias and protected-handle guards on Windows. T067's 13 gate tests and T069's four cross-boundary tests pass on both systems. T068's malformed stored/deflate payload and device-alias regressions pass; the Windows junction-specific group is explicitly skipped on Linux and actually executed on Windows. These are the implemented bounded contracts, not universal secret, native offline-availability or business-impact certification.

## Report artifacts

Linux artifact `12050928848` and Windows artifact `12051850712` contain exactly the three expected reports. The reviewer downloaded both, validated JSON and SARIF against the repository's report schema and pinned official OASIS SARIF schema with locked validation libraries, and compared bytes. All three are identical across platforms:

| File | SHA256 |
| --- | --- |
| `findings.json` | `0e0e57cf76b2fd6679766ca3eec18bbd55177d07e428061b52f9cadeb8987b8b` |
| `report.md` | `a4cfbf91db7ee99a12e86d7a6b9e129fd2bf7f9b3b9468f7eab3291e25882ab8` |
| `results.sarif` | `cb171ff03db52b709ebda0f6b31fab95c4bd96c32410d76ae092d3cb5000917d` |

The quality workflow analyzes its declared tracked top-level `devsift/*.py` scope with the configured built-in security profile and explicit native availability probe. Artifact completeness and zero cases refer to that scope. SARIF records successful execution; the optional SARIF service publisher remains skipped.

## Cache observations and limits

Both quality jobs actually report an exact-key SQL NuGet cache hit and successful restore. Mandatory helper setup, fresh analysis and artifact upload still execute successfully. Observed keys:

- `devsift-nuget-v1-Linux-X64-sdk9.0.205-go1.21.3-node24-ae5e36506718277e0980f5b5a1c680f466f5b75c21f0cc0edcfe30c0df4b4ebc`
- `devsift-nuget-v1-Windows-X64-sdk9.0.205-go1.21.3-node24-a2f334e8b0cdb1cce66ae5d219536fd669d51222e808eb8e7bd4bc1c9ac2bbf6`

PR cache-save steps and optional SARIF service publishing are skipped. This audit does not assert a protected-main save, signing, live credential validation, publication permission, whole-repository coverage or wheel/native byte reproducibility. G024 release preparation has separate ownership and evidence; no actual tag, package release or owner license choice follows from these checks.

The specs implementation at `dec5a19ec62cc5fbe0dc4b6a7eef1c656ef21752` independently passed all 23 plan/ownership tests on both hosted systems in [run 38912452728](https://github.com/orchex006/devsift-specs/actions/runs/38912452728). Those logs execute the actual POSIX flock and Windows byte-range protocols, including conflict serialization, timeout/recovery, reviewed historical compatibility and controller routing. Later documentation/bookkeeping heads still require their own final plan checks before merge.
