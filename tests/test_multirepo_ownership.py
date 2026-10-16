"""Actual cooperative controllers: separate repo overrides and serialized schema ownership.

These fixtures do not implement a second runtime policy parser or authenticate
operators. Only disposable ledgers and declared configuration ownership are used.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from resource_claims import ClaimRequest, apply_claim, ledger_lock


class MultirepoOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "plan").mkdir()
        self.path = self.root / "plan/ledger.json"
        self.data = {"tasks": {
            "T000": {"status": "accepted", "depends_on": [], "goal_id": "G000", "repo": "owner/specs"},
            "T001": {"status": "pending", "depends_on": ["T000"], "goal_id": "G001", "repo": "owner/repo-a", "resource_locks": []},
            "T002": {"status": "pending", "depends_on": ["T000"], "goal_id": "G002", "repo": "owner/repo-b", "resource_locks": []}},
            "execution": {"selected_goals": ["G001", "G002"], "jobs": {},
                "authorizations": {"session": {"controller": "controller", "selected_goals": ["G001", "G002"]}}},
            "declared_repo_overrides": {"owner/repo-a": {"quality_gate": {"block_on": ["Critical", "Error"]}},
                                       "owner/repo-b": {"quality_gate": {"block_on": []}}},
            "foreign": {"do_not_lose": ["opaque", 7]}}
        self.path.write_text(json.dumps(self.data), encoding="utf-8")
        for name in ("repo-a", "repo-b"):
            target = self.root / name / ".devsift"
            target.mkdir(parents=True)
            (target / "policy.json").write_text(json.dumps(self.data["declared_repo_overrides"]["owner/" + name]), encoding="utf-8")

    def request(self, index, lock):
        return ClaimRequest("T00" + str(index), "writer_" + str(index), "owner/repo-" + ("a" if index == 1 else "b"),
                            (".devsift/policy.json",), (lock,))

    def race(self, requests):
        code = """import json,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from resource_claims import ClaimRequest,apply_claim
root=Path(sys.argv[2]);index=sys.argv[3]
(root/('ready-'+index)).write_text('ready')
deadline=time.monotonic()+20
while not (root/'go').exists():
    if time.monotonic()>deadline: raise RuntimeError('Fixture startup timeout')
    time.sleep(.01)
result=apply_claim(root,ClaimRequest(**json.loads(sys.argv[4])),controller='controller',authorization_id='session')
print(json.dumps({'admitted':result.admitted,'reason':result.reason}))
"""
        processes = []
        try:
            for index, request in enumerate(requests):
                processes.append(subprocess.Popen([sys.executable, "-I", "-B", "-c", code, str(ROOT / "tools"),
                    str(self.root), str(index), json.dumps(request.to_dict())], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
            deadline = time.monotonic() + 20
            while not all((self.root / ("ready-" + str(i))).exists() for i in range(len(processes))):
                self.assertLess(time.monotonic(), deadline)
                time.sleep(.01)
            (self.root / "go").write_text("go")
            outcomes = []
            for process in processes:
                out, err = process.communicate(timeout=20)
                self.assertEqual(process.returncode, 0, err)
                outcomes.append(json.loads(out))
            return outcomes
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                process.wait(timeout=5)

    def test_disjoint_repo_override_ownership_admitted_concurrently_without_config_mutation(self):
        configs = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.glob("repo-*/.devsift/policy.json")}
        outcomes = self.race((self.request(1, "write:config/repo-a"), self.request(2, "write:config/repo-b")))
        self.assertTrue(all(row["admitted"] for row in outcomes))
        current = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(set(current["execution"]["jobs"]), {"T001", "T002"})
        self.assertEqual(current["declared_repo_overrides"], self.data["declared_repo_overrides"])
        self.assertEqual(current["foreign"], self.data["foreign"])
        self.assertEqual(configs, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in configs})
        self.assertTrue(all(job["status"] == "claimed" for job in current["execution"]["jobs"].values()))

    def test_shared_policy_contract_serializes_even_across_repositories(self):
        requests = (self.request(1, "write:policy/schema"), self.request(2, "write:policy/schema"))
        outcomes = self.race(requests)
        self.assertEqual(sum(row["admitted"] for row in outcomes), 1)
        winner = next(i for i, row in enumerate(outcomes) if row["admitted"])
        loser = 1 - winner
        # Simulate the trusted controller recording completed independent review
        # in this TEMP fixture only. apply_claim itself never accepts or releases.
        with ledger_lock(self.root) as path:
            current = json.loads(path.read_text(encoding="utf-8"))
            task = requests[winner].task_id
            current["tasks"][task]["status"] = "accepted"
            current["execution"]["jobs"][task].update(status="accepted", locks=[], reviewer="fixture_reviewer")
            temporary = path.with_suffix(".fixture-tmp")
            temporary.write_text(json.dumps(current), encoding="utf-8")
            temporary.replace(path)
        retry = apply_claim(self.root, requests[loser], controller="controller", authorization_id="session")
        self.assertTrue(retry.admitted)
        current = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(current["tasks"][requests[winner].task_id]["status"], "accepted")
        self.assertEqual(current["tasks"][requests[loser].task_id]["status"], "claimed")
        self.assertEqual(current["foreign"], self.data["foreign"])

    def test_selected_overrides_do_not_grant_other_controller_ownership(self):
        self.data["execution"]["goal_controllers"] = {"G001": "controller", "G002": "other_controller"}
        self.path.write_text(json.dumps(self.data), encoding="utf-8")
        before = self.path.read_bytes()
        denied = apply_claim(self.root, self.request(2, "write:config/repo-b"), controller="controller", authorization_id="session")
        self.assertFalse(denied.admitted)
        self.assertEqual(denied.reason, "UNAUTHORIZED_CONTROLLER")
        self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
