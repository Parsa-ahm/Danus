import unittest
import time
import os
from scripts import TaskScheduler, suggest_edits, apply_edits


class TestSchedulerAndEditor(unittest.TestCase):

    def test_scheduler_runs_task(self):
        scheduler = TaskScheduler()
        marker = []

        def task():
            marker.append('done')

        scheduler.schedule(task, time.time() + 0.5)
        time.sleep(1)
        scheduler.run_pending()
        self.assertEqual(marker, ['done'])

    def test_live_editor_diff_and_apply(self):
        original = 'hello world\nthis is a test'
        edited = 'hello brave new world\nthis is a test'
        suggestions = suggest_edits(original, edited)
        self.assertTrue(any(s['type'] == 'add' for s in suggestions))

        tmp_path = 'tests/tmp_edit.txt'
        apply_edits(tmp_path, edited, backup=False)
        with open(tmp_path, 'r', encoding='utf-8') as f:
            contents = f.read()
        os.remove(tmp_path)
        self.assertEqual(contents, edited)


if __name__ == '__main__':
    unittest.main()
