"""Small real cross-process fixtures for the one canonical ledger transaction."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from resource_claims import ClaimRequest, ClaimError, apply_claim, ledger_lock


class ResourceClaimsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "plan").mkdir()
        self.path = self.root / "plan/ledger.json"
        self.data = {"foreign": {"keep": ["opaque", 7]}, "tasks": {
            "T000": {"status": "accepted", "depends_on": [], "goal_id": "G000", "repo": "owner/code"},
            "T001": {"status": "pending", "depends_on": ["T000"], "goal_id": "G001", "repo": "owner/code", "resource_locks": []},
            "T002": {"status": "pending", "depends_on": ["T000"], "goal_id": "G001", "repo": "owner/specs", "resource_locks": []}},
            "execution": {"selected_goals": ["G001"], "jobs": {}, "foreign": {"preserve": True},
                          "authorizations": {"session": {"controller": "controller", "selected_goals": ["G001"], "foreign": 9}}}}
        self.write(self.data)

    def write(self, data):
        self.path.write_text(json.dumps(data), encoding="utf-8")

    def request(self, task="T001", repo="owner/code", paths=("src/one.py",), locks=()):
        return ClaimRequest(task, "worker", repo, paths, locks, {"branch": "feature/fixture"})

    def apply(self, request, **kwargs):
        return apply_claim(self.root, request, controller="controller", authorization_id="session", **kwargs)

    def test_admission_preserves_foreign_fields_and_does_not_accept_or_execute(self):
        before = self.path.read_bytes()
        outcome = self.apply(self.request(), expected_digest=hashlib.sha256(before).hexdigest())
        self.assertTrue(outcome.admitted)
        updated = json.loads(self.path.read_text())
        self.assertEqual(updated["foreign"], self.data["foreign"])
        self.assertEqual(updated["execution"]["foreign"], {"preserve": True})
        self.assertEqual(updated["execution"]["authorizations"], self.data["execution"]["authorizations"])
        self.assertEqual(updated["tasks"]["T000"], self.data["tasks"]["T000"])
        self.assertEqual(updated["tasks"]["T001"]["status"], "claimed")
        self.assertEqual(updated["execution"]["jobs"]["T001"]["owner"], "worker")
        self.assertEqual(outcome.after_digest, hashlib.sha256(self.path.read_bytes()).hexdigest())

    def test_invalid_not_ready_unauthorized_and_stale_leave_ledger_unchanged(self):
        original = self.path.read_bytes()
        self.assertFalse(apply_claim(self.root, self.request(), controller="stranger", authorization_id="session").admitted)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse(self.apply(self.request(), expected_digest="0" * 64).admitted)
        self.assertEqual(self.path.read_bytes(), original)
        assigned = copy.deepcopy(self.data)
        assigned["tasks"]["T001"]["assignee"] = "other-session-worker"
        self.write(assigned)
        assigned_bytes = self.path.read_bytes()
        self.assertFalse(self.apply(self.request()).admitted)
        self.assertEqual(self.path.read_bytes(), assigned_bytes)
        not_ready = copy.deepcopy(self.data)
        not_ready["tasks"]["T000"]["status"] = "in_review"
        self.write(not_ready)
        original = self.path.read_bytes()
        self.assertFalse(self.apply(self.request()).admitted)
        self.assertEqual(self.path.read_bytes(), original)
        self.path.write_text('{"tasks":{},"tasks":{}}', encoding="utf-8")
        original = self.path.read_bytes()
        self.assertFalse(self.apply(self.request()).admitted)
        self.assertEqual(self.path.read_bytes(), original)
        self.path.unlink()
        self.assertFalse(self.apply(self.request()).admitted)
        self.assertFalse(self.path.exists())

    def test_reviewed_inactive_non_task_history_preserved_and_ambiguous_history_denied(self):
        historical = {"status": "accepted", "locks": [], "owner": "prior_writer",
                      "reviewer": "prior_reviewer", "review_result": "accepted",
                      "source_sha": "a" * 40, "integrated_sha": "b" * 40,
                      "opaque_history": {"keep": [1, 2]}}
        self.data["execution"]["jobs"]["historical-integration"] = historical
        self.write(self.data)
        self.assertTrue(self.apply(self.request()).admitted)
        self.assertEqual(json.loads(self.path.read_text())["execution"]["jobs"]["historical-integration"], historical)
        for changes in ({"status": "running"}, {"status": "unknown"}, {"locks": ["write:held"]},
                        {"locks": None}, {"review_result": "pending"}, {"reviewer": "prior_writer"},
                        {"reviewer": None}, {"source_sha": "not-a-sha"}, {"integrated_sha": "0" * 40}):
            data = copy.deepcopy(self.data)
            data["execution"]["jobs"]["historical-integration"] = {**historical, **changes}
            self.write(data)
            before = self.path.read_bytes()
            with self.subTest(changes=changes):
                self.assertFalse(self.apply(self.request()).admitted)
                self.assertEqual(self.path.read_bytes(), before)
        data = copy.deepcopy(self.data)
        data["execution"]["jobs"]["T999"] = data["execution"]["jobs"].pop("historical-integration")
        self.write(data)
        before = self.path.read_bytes()
        self.assertFalse(self.apply(self.request()).admitted)
        self.assertEqual(self.path.read_bytes(), before)

    def test_selected_authorization_does_not_override_existing_goal_controller(self):
        self.data["execution"]["goal_controllers"] = {"G001": "other_controller"}
        self.write(self.data)
        before = self.path.read_bytes()
        self.assertFalse(self.apply(self.request()).admitted)
        self.assertEqual(self.path.read_bytes(), before)

    def test_path_prefix_conflicts_are_repository_scoped_contracts_are_global(self):
        self.assertTrue(self.apply(self.request(paths=("src/",), locks=("write:shared/model",))).admitted)
        self.assertTrue(self.apply(self.request("T002", "owner/specs", ("src/child.py",))).admitted)
        # Existing leases are never automatically stolen, even if timestamps claim expiry.
        current = json.loads(self.path.read_text())
        current["tasks"]["T003"] = {"status": "pending", "depends_on": [], "goal_id": "G001", "repo": "owner/code", "resource_locks": []}
        current["execution"]["jobs"]["T001"]["expires_at"] = "1900-01-01T00:00:00Z"
        self.write(current)
        before = self.path.read_bytes()
        self.assertFalse(self.apply(self.request("T003", paths=("SRC/child.py",))).admitted)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertFalse(self.apply(self.request("T003", paths=("elsewhere.py",), locks=("write:shared",))).admitted)
        self.assertEqual(self.path.read_bytes(), before)

    def race(self, requests):
        code = """import json,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from resource_claims import ClaimRequest,apply_claim
root=Path(sys.argv[2]); index=sys.argv[3]; request=ClaimRequest(**json.loads(sys.argv[4]))
(root/('ready-'+index)).write_text('ready')
deadline=time.monotonic()+20
while not (root/'go').exists():
    if time.monotonic()>deadline: raise RuntimeError('Fixture barrier timed out')
    time.sleep(.01)
result=apply_claim(root,request,controller='controller',authorization_id='session',timeout_seconds=2)
print(json.dumps({'admitted':result.admitted,'reason':result.reason}))
"""
        processes = []
        try:
            for index, request in enumerate(requests):
                processes.append(subprocess.Popen([sys.executable, "-I", "-B", "-c", code, str(ROOT / "tools"),
                                                   str(self.root), str(index), json.dumps(request.to_dict())],
                                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
            deadline = time.monotonic() + 20
            while not all((self.root / ("ready-" + str(index))).exists() for index in range(len(requests))):
                self.assertLess(time.monotonic(), deadline, "Fixture startup exceeded generous host bound")
                time.sleep(.01)
            (self.root / "go").write_text("go")
            outcomes = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=20)
                self.assertEqual(process.returncode, 0, stderr)
                outcomes.append(json.loads(stdout))
            return outcomes
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                process.wait(timeout=5)

    def test_actual_processes_same_contract_only_one_admitted(self):
        requests = [self.request(locks=("write:contract/report",)),
                    self.request("T002", "owner/specs", ("other.py",), ("write:contract/report",))]
        outcomes = self.race(requests)
        self.assertEqual(sum(item["admitted"] for item in outcomes), 1)
        self.assertEqual(len(json.loads(self.path.read_text())["execution"]["jobs"]), 1)

    def test_actual_processes_disjoint_domains_both_admitted_without_lost_fields(self):
        outcomes = self.race([self.request(), self.request("T002", "owner/specs")])
        self.assertTrue(all(item["admitted"] for item in outcomes))
        current = json.loads(self.path.read_text())
        self.assertEqual(set(current["execution"]["jobs"]), {"T001", "T002"})
        self.assertEqual(current["foreign"], self.data["foreign"])

    def test_actual_processes_disjoint_paths_in_same_repository_both_admitted(self):
        self.data["tasks"]["T002"]["repo"] = "owner/code"
        self.write(self.data)
        outcomes = self.race([self.request(paths=("src/one.py",)),
                              self.request("T002", "owner/code", ("docs/guide.md",))])
        self.assertTrue(all(item["admitted"] for item in outcomes))

    def test_actual_os_lock_timeout_and_recovery_without_deleting_lock_inode(self):
        code = """import sys
sys.path.insert(0,sys.argv[1])
from resource_claims import ledger_lock,ClaimError
try:
    with ledger_lock(sys.argv[2],timeout_seconds=.05): print('unexpected')
except ClaimError as error: print(error.code)
"""
        original = self.path.read_bytes()
        with ledger_lock(self.root):
            child = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(ROOT / "tools"), str(self.root)],
                                   capture_output=True, text=True, timeout=20)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(child.stdout.strip(), "LOCK_TIMEOUT")
        self.assertEqual(self.path.read_bytes(), original)
        self.assertTrue(self.apply(self.request()).admitted)

    def test_fixed_lock_path_cannot_create_an_external_dangling_symlink_target(self):
        directory = self.root / ".devsift/local"
        directory.mkdir(parents=True)
        with tempfile.TemporaryDirectory() as other:
            outside = Path(other) / "must-not-be-created"
            try:
                (directory / "resource-claims.lock").symlink_to(outside)
            except OSError:
                self.skipTest("Host does not permit fixture symlinks")
            before = self.path.read_bytes()
            self.assertFalse(self.apply(self.request()).admitted)
            self.assertFalse(outside.exists())
            self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
