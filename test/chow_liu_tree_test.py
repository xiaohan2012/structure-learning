import unittest
import config

from chow_liu_tree import has_loop

class HasLoopTest (unittest.TestCase):
    """
    test for has loop for undirected graph
    """
    def test_basic1 (self):
        edges = [('a', 'b'), ('b', 'c'), ('c', 'a')]
        self.assertTrue(has_loop (edges))

    def test_basic2 (self):
        edges = [('a', 'b'), ('b', 'c'), ('c', 'd')]
        self.assertFalse(has_loop (edges))

if __name__ == "__main__":
    unittest.main ()
