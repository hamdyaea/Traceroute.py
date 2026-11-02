# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock

spec = importlib.util.spec_from_file_location("trace_app", Path(__file__).resolve().parents[1] / "Traceroute.py")
app = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = app
spec.loader.exec_module(app)

class TraceTests(unittest.TestCase):
    def test_safe_argument_list(self):
        runner = Mock(return_value=Mock(returncode=0, stdout="ok", stderr=""))
        result = app.trace("example.com", finder=lambda name: "/usr/bin/traceroute", runner=runner)
        self.assertEqual(result.stdout, "ok")
        self.assertEqual(runner.call_args.args[0], ["traceroute", "-m", "30", "-w", "2", "example.com"])
    def test_reject_injection(self):
        for host in ("-x", "a;rm", "a b", ""):
            with self.assertRaises(ValueError):
                app.validate_host(host)
    def test_missing_binary(self):
        with self.assertRaises(RuntimeError):
            app.trace("example.com", finder=lambda name: None)
    def test_bad_hops(self):
        with self.assertRaises(ValueError):
            app.trace("example.com", max_hops=0)

if __name__ == "__main__":
    unittest.main()
