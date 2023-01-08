import unittest
import numpy as np
from check_vulnerability import check_line_breakable

"""
Return
    0: is_breakable,
    1: is_left,
    2: index,
"""

class TestBreakingRight(unittest.TestCase):
    def test_index_2(self):
        asserting_result = (True, False, 2)
        starting_index = 3
        line = np.array((-1,0,-1,0,1,0,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == asserting_result

    def test_index_1(self):
        asserting_result = (True, False, 1)
        starting_index = 3
        line = np.array((-1,-1,1,0,0,-1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == asserting_result

class TestBreakingLeft(unittest.TestCase):
    def test_index_2(self):
        asserting_result = (True, True, 2)
        starting_index = 3
        line = np.array((-1,0,1,0,-1,0,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == asserting_result

    def test_index_1(self):
        asserting_result = (True, True, 1)
        starting_index = 3
        line = np.array((-1,-1,0,0,1,-1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == asserting_result

class TestNoBreaking(unittest.TestCase):
    asserting_result = (False, False, 0)

    def test_1(self):
        starting_index = 3
        line = np.array((-1,0,1,0,1,0,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result

    def test_2(self):
        starting_index = 3
        line = np.array((-1,-1,-1,0,-1,-1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result

    def test_3(self):
        starting_index = 3
        line = np.array((-1,-1,0,0,0,-1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result

    def test_4(self):
        starting_index = 3
        line = np.array((-1,-1,1,0,1,-1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result

    def test_5(self):
        starting_index = 3
        line = np.array((-1,-1,1,0,-1,-1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result

    def test_6(self):
        starting_index = 3
        line = np.array((-1,-1,-1,0,1,-1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result

    def test_7(self):
        starting_index = 3
        line = np.array((-1,-1,0,0,0,1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result

    def test_8(self):
        starting_index = 3
        line = np.array((-1,1,0,0,0,1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result

    def test_9(self):
        starting_index = 3
        line = np.array((-1,1,0,0,0,-1,1,0))
        result = check_line_breakable(line, starting_index, 1)
        assert result == self.asserting_result