#!/usr/bin/env python3
import os
import sys
import json
import unittest
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import plugin

class TestWallpaperEnginePlugin(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = os.path.join(self.test_dir, "Steam", "steamapps", "common", "wallpaper_engine", "config")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.orig_p86 = os.environ.get("ProgramFiles(x86)")
        os.environ["ProgramFiles(x86)"] = self.test_dir

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        if self.orig_p86:
            os.environ["ProgramFiles(x86)"] = self.orig_p86

    def test_deep_merge_logic(self):
        target = {"volume": 0.5, "libraryCategories": ["anime"]}
        source = {"volume": 0.8, "fps": 60}
        result = plugin.deep_merge(target, source)
        self.assertEqual(result["volume"], 0.8)
        self.assertEqual(result["fps"], 60)

    def test_file_atomic_write(self):
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, "w") as f:
            f.write(json.dumps({"volume": 0.2}))
        args = {"requestId": "test-001", "action": "apply", "settings": {"fps": 30, "volume": 0.7}}
        plugin.apply(args)
        with open(self.config_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data["volume"], 0.7)

if __name__ == "__main__":
    unittest.main()
