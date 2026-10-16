"""Cooperative maintainer admission against the single canonical specs ledger.

This is synchronization for trusted controllers, not authentication, a scheduler,
an approval engine, or protection against writers that ignore this OS lock.
"""
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
import time

_MAX_BYTES = 8_000_000
_ACTIVE = {"claimed", "running", "in_review", "rework", "paused", "blocked"}


class ClaimError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__("Resource ownership transaction unavailable")


def _require(condition, code="INVALID_REQUEST"):
    if not condition:
        raise ClaimError(code) from None


def _identifier(value):
    _require(type(value) is str and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", value) is not None)


def _task(value):
    _require(type(value) is str and re.fullmatch(r"T[0-9]{3}", value) is not None)


def _repository(value):
    _require(type(value) is str and re.fullmatch(r"[A-Za-z0-9_.-]{1,128}/[A-Za-z0-9_.-]{1,128}", value) is not None)
    _require(all(part not in (".", "..") for part in value.split("/")))
    return value.casefold()


def _paths(values):
    _require(type(values) in (list, tuple) and 0 < len(values) <= 256)
    normalized = []
    for value in values:
        _require(type(value) is str and 0 < len(value) <= 1024)
        path = value.removesuffix("/")
        _require(not any(ord(char) < 32 or ord(char) == 127 or char in '\\:<>"|?*' for char in path))
        parts = path.split("/")
        _require(all(part not in ("", ".", "..") and part.casefold() != ".git"
                     and not part.endswith((" ", ".")) for part in parts))
        normalized.append(path.casefold())
    _require(len(set(normalized)) == len(normalized))
    return tuple(normalized)


def _locks(values):
    _require(type(values) in (list, tuple) and len(values) <= 128)
    result = []
    for value in values:
        _require(type(value) is str and len(value) <= 256 and value.startswith("write:"))
        name = value[6:]
        _require(all(re.fullmatch(r"[A-Za-z0-9_.-]+", part) is not None and part not in (".", "..")
                     for part in name.split("/")))
        result.append(name.casefold())
    _require(len(set(result)) == len(result))
    return tuple(result)


@dataclass(frozen=True)
class ClaimRequest:
    task_id: str
    owner: str = field(repr=False)
    repository: str
    paths: tuple[str, ...] = field(repr=False)
    locks: tuple[str, ...]
    job_fields: tuple[tuple[str, str], ...] = field(default=(), repr=False)

    def __post_init__(self):
        _task(self.task_id)
        _identifier(self.owner)
        _repository(self.repository)
        _paths(self.paths)
        _locks(self.locks)
        fields = self.job_fields
        if type(fields) is dict:
            fields = tuple(sorted(fields.items()))
        _require(type(fields) in (tuple, list) and len(fields) <= 4)
        _require(all(type(pair) in (tuple, list) and len(pair) == 2
                     and type(pair[0]) is str and pair[0] in {"branch", "worktree", "base_sha", "lease"}
                     and type(pair[1]) is str and 0 < len(pair[1]) <= 4096
                     and not any(ord(char) < 32 for char in pair[1]) for pair in fields))
        _require(len({pair[0] for pair in fields}) == len(fields))
        object.__setattr__(self, "paths", tuple(self.paths))
        object.__setattr__(self, "locks", tuple(self.locks))
        object.__setattr__(self, "job_fields", tuple(tuple(pair) for pair in fields))

    def to_dict(self):
        return {"task_id": self.task_id, "owner": self.owner, "repository": self.repository,
                "paths": list(self.paths), "locks": list(self.locks), "job_fields": dict(self.job_fields)}


@dataclass(frozen=True)
class ClaimResult:
    admitted: bool
    reason: str
    before_digest: str | None = None
    after_digest: str | None = None


def _ordinary(path, *, directory):
    info = path.lstat()
    _require(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "UNSAFE_STORAGE")
    _require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode), "UNSAFE_STORAGE")
    return info


def _root(specs_root):
    try:
        original = Path(specs_root).absolute()
        _require(".." not in original.parts, "UNSAFE_STORAGE")
        current = Path(original.anchor)
        _ordinary(current, directory=True)
        for part in original.parts[1:]:
            current /= part
            _ordinary(current, directory=True)
        return original.resolve(strict=True)
    except (OSError, TypeError, ValueError, RuntimeError):
        raise ClaimError("UNSAFE_STORAGE") from None


@contextmanager
def ledger_lock(specs_root, timeout_seconds=2):
    """Hold the fixed OS lock across a trusted maintainer's entire transaction.

    Yield the canonical ledger Path. Do not nest apply_claim inside this lock;
    it acquires the same protocol itself. Never unlink the persistent lock inode.
    All canonical writers must cooperate, including acceptance and cleanup tools.
    """
    _require(type(timeout_seconds) in (int, float) and math.isfinite(timeout_seconds)
             and 0 < timeout_seconds <= 5)
    try:
        root = _root(specs_root)
        ledger = root / "plan/ledger.json"
        _ordinary(root / "plan", directory=True)
        directory = root
        for part in (".devsift", "local"):
            directory /= part
            directory.mkdir(exist_ok=True)
            _ordinary(directory, directory=True)
        lock_path = directory / "resource-claims.lock"
        try:
            _ordinary(lock_path, directory=False)  # Includes dangling reparse points before O_CREAT.
        except FileNotFoundError:
            pass
    except OSError:
        raise ClaimError("STORAGE_UNAVAILABLE") from None
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    fd = None
    acquired = False
    try:
        fd = os.open(lock_path, flags, 0o600)
        info = _ordinary(lock_path, directory=False)
        opened = os.fstat(fd)
        _require((info.st_dev, info.st_ino) == (opened.st_dev, opened.st_ino), "UNSAFE_STORAGE")
        deadline = time.monotonic() + timeout_seconds
        while not acquired:
            try:
                if os.name == "nt":
                    import msvcrt
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except OSError:
                if time.monotonic() >= deadline:
                    raise ClaimError("LOCK_TIMEOUT") from None
                time.sleep(min(.01, max(0, deadline - time.monotonic())))
        # OS range locks may extend past EOF. Initialize only after acquisition
        # so two first-use controllers cannot race an unlocked marker write.
        if os.fstat(fd).st_size == 0:
            os.lseek(fd, 0, os.SEEK_SET)
            os.write(fd, b"\0")
        current = _ordinary(lock_path, directory=False)
        _require((current.st_dev, current.st_ino) == (opened.st_dev, opened.st_ino), "UNSAFE_STORAGE")
        yield ledger
    except OSError:
        raise ClaimError("STORAGE_UNAVAILABLE") from None
    finally:
        if fd is not None:
            try:
                if acquired:
                    if os.name == "nt":
                        import msvcrt
                        os.lseek(fd, 0, os.SEEK_SET)
                        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:
                pass
            finally:
                os.close(fd)


def _read(path):
    _ordinary(path.parent, directory=True)
    before = _ordinary(path, directory=False)
    _require(before.st_size <= _MAX_BYTES, "CORRUPT_LEDGER")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0)
                 | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    try:
        opened = os.fstat(fd)
        _require(stat.S_ISREG(opened.st_mode) and (before.st_dev, before.st_ino) ==
                 (opened.st_dev, opened.st_ino), "UNSAFE_STORAGE")
        pieces, total = [], 0
        while chunk := os.read(fd, min(65536, _MAX_BYTES + 1 - total)):
            pieces.append(chunk)
            total += len(chunk)
            _require(total <= _MAX_BYTES, "CORRUPT_LEDGER")
        raw = b"".join(pieces)
        opened = os.fstat(fd)
    finally:
        os.close(fd)
    after = _ordinary(path, directory=False)
    _require(len(raw) == opened.st_size and (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
             == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
             == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), "CORRUPT_LEDGER")
    return raw


def _unique(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "CORRUPT_LEDGER")
        result[key] = value
    return result


def _decode(raw):
    try:
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_unique,
                          parse_constant=lambda _: _require(False, "CORRUPT_LEDGER"))
        _require(type(data) is dict and type(data.get("tasks")) is dict
                 and 0 < len(data["tasks"]) <= 512 and type(data.get("execution")) is dict, "CORRUPT_LEDGER")
        execution = data["execution"]
        _require(type(execution.get("jobs")) is dict and len(execution["jobs"]) <= 512
                 and type(execution.get("authorizations")) is dict, "CORRUPT_LEDGER")
        return data
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise ClaimError("CORRUPT_LEDGER") from None


def _overlap(left, right):
    return any(a == b or a.startswith(b + "/") or b.startswith(a + "/") for a in left for b in right)


def _ready(tasks, task_id):
    visiting, seen = set(), set()
    def visit(current, root=False):
        _require(current in tasks and type(tasks[current]) is dict and current not in visiting, "CORRUPT_LEDGER")
        if current in seen:
            return
        visiting.add(current)
        task = tasks[current]
        _require(root or task.get("status") == "accepted", "PREREQUISITE_NOT_ACCEPTED")
        deps = task.get("depends_on")
        _require(type(deps) is list and len(deps) <= 512, "CORRUPT_LEDGER")
        for dependency in deps:
            _task(dependency)
            visit(dependency)
        visiting.remove(current)
        seen.add(current)
    visit(task_id, True)


def _admit(data, request, controller, authorization_id):
    tasks, execution = data["tasks"], data["execution"]
    _require(request.task_id in tasks and type(tasks[request.task_id]) is dict, "UNKNOWN_TASK")
    task = tasks[request.task_id]
    goal = task.get("goal_id")
    _require(type(goal) is str and re.fullmatch(r"G[0-9]{3}", goal) is not None, "CORRUPT_LEDGER")
    authorization = execution["authorizations"].get(authorization_id)
    _require(type(authorization) is dict and authorization.get("controller") == controller
             and type(authorization.get("selected_goals")) is list
             and task.get("goal_id") in authorization["selected_goals"]
             and type(execution.get("selected_goals")) is list
             and task.get("goal_id") in execution["selected_goals"], "UNAUTHORIZED_CONTROLLER")
    controllers = execution.get("goal_controllers", {})
    _require(type(controllers) is dict and len(controllers) <= 128, "CORRUPT_LEDGER")
    for routed_goal, routed_controller in controllers.items():
        _require(type(routed_goal) is str and re.fullmatch(r"G[0-9]{3}", routed_goal) is not None, "CORRUPT_LEDGER")
        _identifier(routed_controller)
    _require(goal not in controllers or controllers[goal] == controller, "UNAUTHORIZED_CONTROLLER")
    for goals in (authorization["selected_goals"], execution["selected_goals"]):
        _require(len(goals) <= 128 and all(type(item) is str and re.fullmatch(r"G[0-9]{3}", item) is not None
                                          for item in goals), "CORRUPT_LEDGER")
    _require(task.get("status") == "pending" and request.task_id not in execution["jobs"], "ALREADY_CLAIMED")
    _require(task.get("assignee") in (None, "", "unassigned", request.owner), "ALREADY_ASSIGNED")
    _require(_repository(task.get("repo")) == _repository(request.repository), "REPOSITORY_MISMATCH")
    _ready(tasks, request.task_id)
    required = task.get("resource_locks")
    _locks(required)
    _require(set(required) <= set(request.locks), "REQUIRED_LOCK_MISSING")
    requested_paths, requested_locks = _paths(request.paths), _locks(request.locks)
    for task_id, job in execution["jobs"].items():
        _require(type(job) is dict, "CORRUPT_LEDGER")
        if task_id not in tasks:
            # Reviewed integration/correction jobs predate task-only allocation.
            # Preserve their records without inventing tasks or active leases.
            _identifier(task_id)
            _require(re.fullmatch(r"T[0-9]{3}", task_id) is None, "CORRUPT_LEDGER")
            _require(job.get("status") == "accepted" and job.get("locks") == []
                     and job.get("review_result") == "accepted", "CORRUPT_LEDGER")
            _identifier(job.get("owner"))
            _identifier(job.get("reviewer"))
            _require(job["owner"] != job["reviewer"], "CORRUPT_LEDGER")
            for key in ("source_sha", "integrated_sha"):
                value = job.get(key)
                _require(type(value) is str and re.fullmatch(r"(?:[a-f0-9]{40}|[a-f0-9]{64})", value) is not None
                         and set(value) != {"0"}, "CORRUPT_LEDGER")
            continue
        _task(task_id)
        status = job.get("status")
        if status == "accepted":
            _require(tasks[task_id].get("status") == "accepted" and job.get("locks", []) == [], "CORRUPT_LEDGER")
            continue
        _require(type(status) is str and status in _ACTIVE, "CORRUPT_LEDGER")
        _identifier(job.get("owner"))
        paths, locks = _paths(job.get("paths")), _locks(job.get("locks"))
        repository = job.get("source_repository", tasks[task_id].get("repo"))
        _require(_repository(repository) == _repository(tasks[task_id].get("repo")), "CORRUPT_LEDGER")
        _require(not _overlap(requested_locks, locks), "RESOURCE_CONFLICT")
        if _repository(repository) == _repository(request.repository):
            _require(not _overlap(requested_paths, paths), "RESOURCE_CONFLICT")
    history = task.get("history", [])
    _require(type(history) is list and len(history) < 10000, "CORRUPT_LEDGER")
    task.update(status="claimed", assignee=request.owner)
    task["history"] = history + [{"status": "claimed", "actor": controller,
                                  "at": datetime.now(timezone.utc).isoformat(),
                                  "reason": "Resource admission under cooperative canonical-ledger OS lock."}]
    execution["jobs"][request.task_id] = {**dict(request.job_fields), "owner": request.owner, "status": "claimed",
                                           "paths": list(request.paths), "locks": list(request.locks),
                                           "source_repository": request.repository, "claim_controller": controller,
                                           "authorization_id": authorization_id}


def _atomic(path, payload):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=".resource-claims-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def apply_claim(specs_root, request, *, controller, authorization_id, expected_digest=None, timeout_seconds=2):
    """Admit one new pending task; never submit/accept/reassign/steal/release it."""
    before_digest = None
    try:
        _require(type(request) is ClaimRequest)
        ClaimRequest(**request.to_dict())
        _identifier(controller)
        _identifier(authorization_id)
        _require(expected_digest is None or (type(expected_digest) is str
                 and re.fullmatch(r"[a-f0-9]{64}", expected_digest) is not None))
        with ledger_lock(specs_root, timeout_seconds) as path:
            try:
                raw = _read(path)
            except FileNotFoundError:
                raise ClaimError("MISSING_LEDGER") from None
            before_digest = hashlib.sha256(raw).hexdigest()
            _require(expected_digest is None or expected_digest == before_digest, "STALE_DIGEST")
            data = _decode(raw)
            _admit(data, request, controller, authorization_id)
            payload = (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
            _require(len(payload) <= _MAX_BYTES, "CORRUPT_LEDGER")
            # Best-effort CAS detects an already changed noncooperating writer;
            # only the shared OS-lock protocol closes races among participants.
            _require(hashlib.sha256(_read(path)).hexdigest() == before_digest, "STALE_DIGEST")
            _atomic(path, payload)
            return ClaimResult(True, "ADMITTED", before_digest, hashlib.sha256(payload).hexdigest())
    except ClaimError as error:
        return ClaimResult(False, error.code, before_digest)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RuntimeError, RecursionError, OverflowError):
        return ClaimResult(False, "STORAGE_OR_LEDGER_UNAVAILABLE", before_digest)
