import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "infrastructure" / "local"))
import docker_ready as d


class ReadinessTests(unittest.TestCase):
    @patch.object(d.shutil, "which", return_value="docker")
    def test_ready_engine_does_not_restart_and_does_not_mutate_host_env(self, _):
        with patch.dict(os.environ, {"DOCKER_API_VERSION": "1.56"}), \
             patch.object(d, "_probe", return_value=(True, "")) as probe, \
             patch.object(d, "_run") as run:
            env = d.ensure_docker(".", platform="nt")
            self.assertNotIn("DOCKER_API_VERSION", env)
            self.assertEqual(os.environ["DOCKER_API_VERSION"], "1.56")
            self.assertNotIn("DOCKER_API_VERSION", probe.call_args.args[0])
            run.assert_not_called()

    @patch.object(d.shutil, "which", return_value="docker")
    def test_restart_then_engine_becomes_ready(self, _):
        with patch.object(d, "_probe", side_effect=[(False, "500"), (True, "")]), \
             patch.object(d, "_run", return_value=subprocess.CompletedProcess([], 0)) as run:
            env = d.ensure_docker(".", platform="nt")
            self.assertIsInstance(env, dict)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(run.call_args.args[0], ["docker", "desktop", "restart"])

    @patch.object(d.shutil, "which", return_value="docker")
    def test_launch_once_when_desktop_cli_is_unavailable(self, _):
        with patch.object(d, "_probe", side_effect=[(False, "500"), (True, "")]), \
             patch.object(d, "_run", return_value=subprocess.CompletedProcess([], 1)), \
             patch.object(d, "_desktop_exe", return_value=Path("Docker Desktop.exe")), \
             patch.object(d.subprocess, "Popen") as launch:
            d.ensure_docker(".", platform="nt")
            launch.assert_called_once()

    @patch.object(d.shutil, "which", return_value="docker")
    def test_failed_recovery_reports_diagnostics_without_reset(self, _):
        with patch.object(d.time, "monotonic", side_effect=[0, 0, 2]), \
             patch.object(d, "_probe", return_value=(False, "500 Internal Server Error")), \
             patch.object(d, "_run", return_value=subprocess.CompletedProcess([], 1)), \
             patch.object(d, "_desktop_exe", return_value=None), \
             patch.object(d, "_diagnostics", return_value="docker-diagnostics.txt") as diag:
            with self.assertRaisesRegex(d.DockerNotReady, "500 Internal Server Error"):
                d.ensure_docker(".", platform="nt", timeout=1)
            diag.assert_called_once()

    def test_missing_docker_has_actionable_error(self):
        with patch.object(d.shutil, "which", return_value=None):
            with self.assertRaisesRegex(d.DockerNotReady, "Docker not found"):
                d.ensure_docker(".", platform="nt")

    def test_empty_server_version_is_not_success(self):
        with patch.object(d, "_run", return_value=subprocess.CompletedProcess([], 0, b"", b"")):
            self.assertFalse(d._probe({})[0])

    def test_diagnostics_work_even_when_optional_commands_are_missing(self):
        with tempfile.TemporaryDirectory() as folder, \
             patch.object(d, "_run", return_value=subprocess.CompletedProcess([], 1, b"", b"missing")) as run:
            report = d._diagnostics(folder, {}, "500")
            self.assertIn("500", Path(report).read_text())
            commands = [call.args[0] for call in run.call_args_list]
            self.assertIn(["wsl", "--status"], commands)
            self.assertFalse(any("--shutdown" in c or "--unregister" in c for c in commands))

    def test_wsl_utf16_output_is_readable(self):
        self.assertEqual(d._text("Ubuntu Stopped".encode("utf-16-le")), "Ubuntu Stopped")


if __name__ == "__main__":
    unittest.main()
