import unittest
import os
from scripts import file_indexer

class TestDanusExtended(unittest.TestCase):

    def setUp(self):
        self.test_folder = os.path.abspath("tests/sample_data_ext")
        os.makedirs(self.test_folder, exist_ok=True)
        self.sample_file1 = os.path.join(self.test_folder, "file1.txt")
        self.sample_file2 = os.path.join(self.test_folder, "file2.txt")
        self.sample_contract = os.path.join(self.test_folder, "contract_terms.txt")

        with open(self.sample_file1, "w") as f:
            f.write("Hello world. This file is unrelated.")
        with open(self.sample_file2, "w") as f:
            f.write("Another generic document with no contract relevance.")
        with open(self.sample_contract, "w") as f:
            f.write("This contract includes payment terms: Net 30, termination clause, and deliverables.")

    def test_index_and_search_accuracy(self):
        file_indexer.scan_folder(self.test_folder)
        results = file_indexer.search_files("termination clause")
        print("Search Results:", results)
        self.assertTrue(results is not None and len(results) > 0)
        found = any("termination" in r["preview"].lower() for r in results)
        self.assertTrue(found, "Relevant contract term not found in top results")

    def test_qa_accuracy_from_contract(self):
        file_indexer.scan_folder(self.test_folder)
        result = file_indexer.answer_question_human_like("What are the payment terms?")
        print("QA Summary:", result.get("summary", ""))
        self.assertTrue("summary" in result and result["summary"])
        self.assertTrue("net" in result["summary"].lower() or "terms" in result["summary"].lower())

    def test_no_match_behavior(self):
        file_indexer.scan_folder(self.test_folder)
        result = file_indexer.answer_question_human_like("Describe quantum mechanics in this folder")
        self.assertIn("summary", result)
        self.assertTrue(isinstance(result["summary"], str))

    def tearDown(self):
        for f in [self.sample_file1, self.sample_file2, self.sample_contract]:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(self.test_folder):
            os.rmdir(self.test_folder)

if __name__ == "__main__":
    unittest.main()