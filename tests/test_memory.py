import unittest
import os
from scripts import add_message, get_history

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.mem_dir = os.path.join(os.getcwd(), 'danus_memory')
        if os.path.exists(self.mem_dir):
            for f in os.listdir(self.mem_dir):
                os.remove(os.path.join(self.mem_dir, f))

    def test_add_and_retrieve(self):
        add_message('user', 'hello')
        add_message('assistant', 'hi there')
        history = get_history(days=1)
        self.assertGreaterEqual(len(history), 2)
        roles = [h[0] for h in history]
        self.assertIn('user', roles)
        self.assertIn('assistant', roles)

if __name__ == '__main__':
    unittest.main()
