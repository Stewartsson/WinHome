import sys
import os
import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import io

# 7. Test file with sys.path.append (not sys.path.insert(0))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import plugin

class TestDockerComposePlugin(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_home = Path(self.temp_dir.name)
        
    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("sys.stdin", io.StringIO(""))
    def test_empty_stdin(self):
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            with self.assertRaises(SystemExit):
                plugin.main()
            self.assertIn("Empty stdin", fake_out.getvalue())

    @patch("plugin.get_config_path")
    def test_check_installed(self, mock_path):
        mock_path.return_value = self.mock_home / ".docker" / "config.json"
        req = {"requestId": "test-req", "action": "check_installed"}
        
        with patch("sys.stdin", io.StringIO(json.dumps(req))):
            with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                plugin.main()
                self.assertEqual(fake_out.getvalue().strip(), "true")

    @patch("plugin.get_config_path")
    def test_apply_settings(self, mock_path):
        config_file = self.mock_home / ".docker" / "config.json"
        mock_path.return_value = config_file
        
        # Setup existing mocked config
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"wslEngine": True, "compose": {"projectName": "old_name"}}, f)
            
        req = {
            "requestId": "req-123",
            "action": "apply",
            "args": {
                "settings": {
                    "experimental": True,
                    "projectName": "new_name",
                    "profiles": ["dev", "debug"]
                },
                "dryRun": False
            }
        }
        
        with patch("sys.stdin", io.StringIO(json.dumps(req))):
            with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                plugin.main()
                out = json.loads(fake_out.getvalue())
                
                # Check protocol constraints
                self.assertEqual(out.get("requestId"), "req-123")
                self.assertNotIn("success", out)
                self.assertNotIn("data", out)
                
        # Verify JSON state & Deep Merge behavior
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertTrue(data["wslEngine"]) # Original non-compose key preserved
            self.assertEqual(data["compose"]["projectName"], "new_name")
            self.assertTrue(data["compose"]["experimental"])
            self.assertEqual(data["compose"]["profiles"], ["dev", "debug"])
        
        # Verify POSIX trailing newline
        with open(config_file, "rb") as f:
            content = f.read()
            self.assertTrue(content.endswith(b"\n"))

if __name__ == "__main__":
    unittest.main()

