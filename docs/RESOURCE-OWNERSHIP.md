# Cooperative canonical-ledger resource admission

`tools/resource_claims.py` is maintainer tooling in **devsift-specs**. It uses the
single `plan/ledger.json`; it is not a runtime scheduler, second ledger, approval
engine or detector of user authorization. The execution ledger's authorizations
and accepted prerequisite statuses remain controller-maintained authority.

```python
from tools.resource_claims import ClaimRequest, apply_claim

request = ClaimRequest(
    task_id="T065", owner="policy_writer", repository="orchex006/devsift-specs",
    paths=("tools/resource_claims.py", "tests/test_resource_claims.py",
           "docs/RESOURCE-OWNERSHIP.md"),
    locks=("write:policy/ownership",),
    job_fields={"branch": "feature/g022-t065-owner-locks"},
)
# Example shape only: T065 is already owned, so this does not authorize reclaim.
result = apply_claim("/explicit/specs/root", request, controller="controller",
                     authorization_id="autopilot_next_goals", timeout_seconds=2)
```

Admission holds a real cross-process OS lock across fresh read, validation,
conflict checks, a final digest check and atomic replacement. Windows uses a
nonblocking `msvcrt` byte-range lock; POSIX uses `flock`. Each process opens the
same fixed contained `.devsift/local/resource-claims.lock`. This persistent file
is transport only: never delete/recreate its inode to release a lock. It stores
no leases, owners, acceptance or alternate state. Range initialization occurs
under the lock. Handles close when the context ends or acquisition fails.

All canonical mutation tools must cooperate, including submit, acceptance and
cleanup helpers. Every caller must select the same canonical shared specs
checkout, never an isolated worktree's frozen ledger. The API does not discover,
merge or create ledgers. For trusted maintainer transactions use the public context:

```python
from tools.resource_claims import ledger_lock

with ledger_lock("/explicit/specs/root", timeout_seconds=2) as ledger_path:
    # Authorized maintainer code owns its own specific mutation/review checks.
    # Fresh-read ledger_path here, validate, and atomically replace before exit.
    pass
```

The context is synchronization only, not authority to mutate anything. It calls
no artifact callback and performs no task transition. Do not nest `apply_claim`
inside it: admission already acquires that same lock. Lock timeouts must be
finite, positive and at most five seconds; default is two seconds. The timeout
bounds acquisition, not arbitrary filesystem delays or the caller's critical
section. Cooperative controllers should keep transactions short. `ClaimError`
has a fixed private message and a bounded failure code.

`apply_claim` accepts only a new **pending** task with no existing execution job.
A different existing assignee cannot be overwritten, even without a job record.
The named `execution.authorizations[authorization_id]` must name the supplied
controller and include the task's goal in `selected_goals`; that goal must also
be selected in `execution`. Every transitive prerequisite must have canonical
`accepted` status. `in_review` never unlocks work. The request repository must
match the task's `repo`, and all task `resource_locks` must be requested explicitly.
Controller identity here is a cooperative trusted-maintainer role checked against
ledger data, not cryptographic authentication or an OS security principal.

Path claims are exclusive, repository-scoped and compared on component boundaries
with case folding: `src/` conflicts with `SRC/file.py`, but `src-old/file.py` does
not overlap. Code and specs repositories may own the same relative spelling
concurrently. Shared `write:` contract locks are global across repositories and
also overlap by prefix: `write:contracts` conflicts with
`write:contracts/source`. There is no read-lock, wildcard or implicit repository-
root ownership mode. Paths reject absolute/traversal and trailing-dot/space forms;
limits are 256 paths of at most 1,024 characters and 128 locks of at most 256.
These are representation bounds, not permission to broaden a task's scope.
Controllers must supply canonical Git path spellings: these declarative resources
do not resolve real runtime filesystem aliases or prove artifact ownership.

Active `claimed/running/in_review/rework/paused/blocked` leases remain exclusively
in `execution.jobs`. Existing job compatibility uses `source_repository` or the
canonical task repository when that older job field is absent. Missing/invalid
active ownership metadata and unknown states fail closed. Accepted historical
jobs are inactive only with accepted canonical task status and cleared locks.
An expiry string, old timestamp or crashed owner never triggers stealing,
reassignment, cleanup, implicit release or acceptance. A new admission changes
only that task's status/assignee/history and creates its execution job. Immutable
requests copy nested metadata; returned digests record before/after bytes, not
authenticated approval. Branch/worktree/base/lease fields are declarations only,
never executed, resolved as artifacts or treated as test/review evidence.

Unknown and foreign JSON fields survive semantic roundtrip. Missing, malformed,
duplicate-key, nonfinite, stale-digest, unauthorized or conflicting inputs cannot
replace the ledger. Input/output is capped at 8 MB and task/job collections at
512 entries. Temporary output is flushed and fsynced in the ledger directory,
then `os.replace` publishes it atomically. Reads and writes use binary byte
semantics, preserving the ledger's physical UTF-8 bytes and LF or CRLF line
endings for size checks and expected-digest comparisons; atomic output is UTF-8
with LF line endings. This establishes atomic visibility
under normal filesystem operation, not universal power-loss durability. Storage
components and existing files reject observed links/reparse points and non-regular
objects; no lock location, ledger filename or callback can be supplied separately.
Hostile concurrent filesystem substitution or external writers that ignore the
lock are outside the cooperative guarantee. The final digest comparison detects
an already observed external edit but cannot close a race against a nonparticipant.
The old CAS-only helper must not claim serialization until it adopts this lock
around its **entire** fresh-read-to-replace transaction.

Runtime policy precedence is separate from maintainer ownership: accepted T064
uses built-in defaults, then one validated repository-local `.devsift/policy.json`
or one explicitly selected in-root JSON path. Missing default discovery may use
defaults; malformed-present/explicit-missing input stays incomplete. There is no
ancestor/global/remote configuration search, executable loading or native trust
grant. Accepted G001 validation merges that project data with defaults and retains
independent canonical Critical security escalation. This maintainer helper neither
imports runtime code nor changes that precedence or severity floor.

Tests use tiny temporary canonical-shaped ledgers only, never the live ledger.
Actual child processes prove same-contract exclusion, disjoint-domain admission
without lost foreign fields, lock timeout and later recovery. Other fixtures
check prefix/case conflicts, expired-looking leases, rejected inputs and a
dangling lock-path symlink whose external target must never be created. Windows
execution tests the actual byte-range branch; POSIX tests use the actual flock
branch when run on POSIX. Neither result should be represented as the other OS.

Compatibility with the existing canonical ledger preserves reviewed historical
integration/correction jobs whose keys are not task IDs. Only explicitly accepted
records with exactly empty locks, an accepted review by a distinct named reviewer,
and full nonzero source/integrated SHAs are inactive. Unknown task-shaped IDs,
active or ambiguous historical records fail closed; no history is removed or
converted into an invented task. These metadata checks do not re-prove old Git
artifacts or authenticate a reviewer. Explicit `execution.goal_controllers`
routing also remains binding: broader selected authorization does not override
another controller's existing goal route.

## Multirepo override acceptance fixtures

`tests/test_multirepo_ownership.py` starts two actual isolated controller child
processes against one disposable ledger. Separate repository-local policy file
claims coexist without changing either configuration. A shared policy/schema
contract admits one owner across repositories, and admits the second only after
the fixture controller records completion and clears the first lease under the
same OS lock. This is cooperative ownership serialization, not a filesystem lock
on application files. A broader selected session cannot override another explicit
goal controller. Opaque foreign state and declared override data survive.

The fixture's override JSON is passive declared data, not another implementation
of runtime policy validation or evidence of effective quality enforcement. Actual
precedence and the independent Critical security floor remain the accepted code
repository's T064 discovery and G001 policy contracts/tests. Fixture acceptance
records simulate trusted coordination only; they do not claim real review,
release authorization or task acceptance for production artifacts.
