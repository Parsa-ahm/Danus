import unittest
import os
import json
import shutil

from scripts import file_indexer


class TestDanusFeatures(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.abspath("tests/tmp_data")
        os.makedirs(self.test_dir, exist_ok=True)
        self.sample_file = os.path.join(self.test_dir, "contract.txt")
        with open(self.sample_file, "w") as f:
            f.write("This contract states the payment terms.")
        if os.path.exists(file_indexer.LOG_PATH):
            os.remove(file_indexer.LOG_PATH)
        if os.path.exists(file_indexer.BACKUP_DIR):
            shutil.rmtree(file_indexer.BACKUP_DIR)

    def test_organize_and_backup(self):
        file_indexer.organize_folder(self.test_dir)
        organized = os.path.join(self.test_dir, "contracts", "contract.txt")
        self.assertTrue(os.path.exists(organized))
        new_path = file_indexer.backup_and_rename(organized)
        self.assertTrue(os.path.exists(new_path))
        backup_path = os.path.join(file_indexer.BACKUP_DIR, "contract.txt")
        self.assertTrue(os.path.exists(backup_path))
        with open(file_indexer.LOG_PATH, "r") as f:
            log = json.load(f)
        self.assertGreaterEqual(len(log), 2)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(file_indexer.BACKUP_DIR):
            shutil.rmtree(file_indexer.BACKUP_DIR)
        if os.path.exists(file_indexer.LOG_PATH):
            os.remove(file_indexer.LOG_PATH)


if __name__ == "__main__":
    unittest.main()
