import os
import sys
import unittest

# 🧠 THE ROUTING FIX: Injects the proper absolute plugin source folder mappings into the runtime execution tree
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from plugin import GreenshotPlugin


class TestGreenshotPlugin(unittest.TestCase):
    """Automated unit verification validation test suite patterns for the Greenshot plugin integration."""

    def test_apply_configuration_matrix(self):
        args = {
            "requestId": "test-req-293",
            "dryRun": True,
            "settings": {
                "Capture\\CaptureMode": "Region",
                "Capture\\CaptureMousepointer": True,
                "Destination\\CopyToClipboard": True,
                "General\\Language": "en-US",
            },
        }
        plugin = GreenshotPlugin(args)
        result = plugin.apply()

        self.assertEqual(result["requestId"], "test-req-293")
        self.assertTrue(result["dryRun"])


if __name__ == "__main__":
    unittest.main()
