"""Exercise conflict handling in isolated Git repositories, never GitHub."""
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/promote-dev.sh"
MANIFEST = "kubernetes/overlays/dev/kustomization.yaml"


class PromotionTests(unittest.TestCase):
    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", *args], cwd=cwd or self.repo,
                                       stderr=subprocess.STDOUT, text=True).strip()

    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.root = Path(self.work.name)
        self.repo = self.root / "source"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Promotion test")
        self.git("config", "user.email", "test@example.com")
        path = self.repo / MANIFEST
        path.parent.mkdir(parents=True)
        path.write_text("images:\n  - name: backend\n    newTag: sha-bootstrap\n"
                        "  - name: frontend\n    newTag: sha-bootstrap\n")
        self.git("add", ".")
        self.git("commit", "-m", "base")
        self.base = self.git("rev-parse", "HEAD")
        self.git("switch", "-c", "deploy/dev")
        path.write_text(path.read_text().replace("sha-bootstrap", "sha-" + "a" * 40))
        self.git("commit", "-am", "previous generated promotion")
        self.dev = self.git("rev-parse", "HEAD")
        self.git("switch", "main")
        # Same formatting change that caused the observed real promotion failure.
        path.write_text(path.read_text().replace("  - name:", "- name:").replace("    newTag:", "  newTag:"))
        (self.repo / "validated-source.txt").write_text("new validated manifests\n")
        self.git("add", ".")
        self.git("commit", "-m", "validated source reformats manifest")
        self.source = self.git("rev-parse", "HEAD")
        self.remote = self.root / "remote.git"
        self.git("clone", "--bare", str(self.repo), str(self.remote))

    def tearDown(self):
        self.work.cleanup()

    def run_promotion(self):
        clone = self.root / "runner"
        self.git("clone", "--single-branch", "--branch", "main", str(self.remote), str(clone))
        self.git("config", "user.name", "Promotion test", cwd=clone)
        self.git("config", "user.email", "test@example.com", cwd=clone)
        result = subprocess.run(["bash", str(SCRIPT), self.source], cwd=clone,
                                capture_output=True, text=True)
        return clone, result

    def test_generated_tag_conflict_is_resolved_and_not_pushed_implicitly(self):
        clone, result = self.run_promotion()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        text = (clone / MANIFEST).read_text()
        self.assertEqual(text.count("sha-" + self.source), 2)
        self.assertTrue((clone / "validated-source.txt").exists())
        self.git("merge-base", "--is-ancestor", self.source, "HEAD", cwd=clone)
        self.git("merge-base", "--is-ancestor", self.dev, "HEAD", cwd=clone)
        self.assertEqual(self.git("rev-parse", "deploy/dev", cwd=self.remote), self.dev)

    def test_manual_manifest_edits_are_preserved_and_conflict_is_rejected(self):
        self.git("switch", "deploy/dev")
        path = self.repo / MANIFEST
        path.write_text(path.read_text().replace("name: backend", "name: manual-backend"))
        self.git("commit", "-am", "manual dev configuration")
        manual = self.git("rev-parse", "HEAD")
        self.git("push", str(self.remote), "deploy/dev")
        clone, result = self.run_promotion()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("non-generated edits", result.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=clone), manual)
        self.assertIn("name: manual-backend", (clone / MANIFEST).read_text())
        self.assertEqual(self.git("status", "--porcelain", cwd=clone), "")

    def test_first_promotion_starts_from_validated_source(self):
        self.git("update-ref", "-d", "refs/heads/deploy/dev", cwd=self.remote)
        clone, result = self.run_promotion()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((clone / MANIFEST).read_text().count("sha-" + self.source), 2)
        self.git("merge-base", "--is-ancestor", self.source, "HEAD", cwd=clone)


if __name__ == "__main__":
    unittest.main()
