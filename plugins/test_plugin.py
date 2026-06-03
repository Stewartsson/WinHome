import unittest
from src.plugin import check_installed, deep_merge

class TestRustupPlugin(unittest.TestCase):
    def test_check_installed_returns_bool(self):
        # Verify the installation detector outputs a clean boolean data type
        result = check_installed()
        self.assertIn(result, [True, False])

    def test_deep_merge_logic(self):
        # Validate that dict components merge without losing unknown properties
        src = {"settings": {"profile": "minimal"}}
        dest = {"settings": {"default_toolchain": "stable"}, "custom_key": 123}
        merged = deep_merge(src, dest)
        self.assertEqual(merged["settings"]["profile"], "minimal")
        self.assertEqual(merged["settings"]["default_toolchain"], "stable")
        self.assertEqual(merged["custom_key"], 123)

if __name__ == '__main__':
    unittest.main()
