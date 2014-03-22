import unittest

from config import DIRNAME
from data_reader import read_row_data

class ReadRowData (unittest.TestCase):
    def test_basic (self):
        path = DIRNAME + "/data/fake_data.txt"
        result = read_row_data (path)
        expected = [
            {"a": '1', "b": '1', "c": '1', "count": 2},
            {"a": '1', "b": '2', "c": '3', "count": 1},
            {"a": '2', "b": '1', "c": '1', "count": 1}
        ]
        
        self.assertEqual (sorted(result), sorted(expected))


if __name__ == "__main__":
    unittest.main ()
