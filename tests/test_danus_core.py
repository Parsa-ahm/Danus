import unittest
import os
from scripts import file_indexer

class TestDanusCore(unittest.TestCase):

    def setUp(self):
        self.test_folder = os.path.abspath("tests/sample_data")
        os.makedirs(self.test_folder, exist_ok=True)
        self.sample_txt_path = os.path.join(self.test_folder, "test.txt")
        with open(self.sample_txt_path, "w") as f:
            f.write("This is a test file for contract agreement and payment terms.")

    def test_scan_folder(self):
        try:
            file_indexer.scan_folder(self.test_folder)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"scan_folder raised an exception: {e}")

    def test_search_files(self):
        file_indexer.scan_folder(self.test_folder)
        result = file_indexer.search_files("contract")
        print("Search Result:", result)
        self.assertTrue(result is not None and len(result) > 0)

    def test_answer_question_human_like(self):
        file_indexer.scan_folder(self.test_folder)
        result = file_indexer.answer_question_human_like("What are the contract terms?")
        print("Answer Summary:", result.get("summary", ""))
        self.assertIn("summary", result)
        self.assertIn("matches", result)
        self.assertGreater(len(result["matches"]), 0)

    def tearDown(self):
        if os.path.exists(self.sample_txt_path):
            os.remove(self.sample_txt_path)
        if os.path.exists(self.test_folder):
            os.rmdir(self.test_folder)

if __name__ == "__main__":
    unittest.main()