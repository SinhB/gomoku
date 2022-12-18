import unittest
import numpy as np
from check_side import check_side

"""
0: consec, (int)
1: additional, (int) 
2: eating, (bool)
3: block, (bool)
"""

class TestBlock(unittest.TestCase):
    def test_empty_side(self):
        asserting_result = (0, 0, False, True)
        side = np.array((), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_side_smaller(self):
        asserting_result = (0, 2, False, True)
        side = np.array((0, 1, 1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_side_smaller_but_ending_blank(self):
        asserting_result = (0, 2, False, False)
        side = np.array((0, 1, 1, 0), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_side_smaller_but_ending_op(self):
        asserting_result = (0, 2, False, True)
        side = np.array((0, 1, 1, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result
    
    def test_block_after_consec(self):
        asserting_result = (2, 0, False, True)
        side = np.array((1, 1, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_block_after_blank_without_add(self):
        asserting_result = (1, 0, False, False)
        side = np.array((1, 0, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_block_after_blank_with_add(self):
        asserting_result = (0, 1, False, True)
        side = np.array((0, 1, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_block_after_blank_with_add_and_consec(self):
        asserting_result = (1, 1, False, True)
        side = np.array((1, 0, 1, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_block_just_after_blank_with_add_and_consec(self):
        asserting_result = (1, 1, False, False)
        side = np.array((1, 0, 1, 0, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

class TestBlank(unittest.TestCase):
    def test_starting_blank(self):
        asserting_result = (0, 0, False, False)
        side = np.array((0, 0, 1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_starting_only_blank(self):
        asserting_result = (0, 0, False, False)
        side = np.array([0], dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_starting_blank_before_op(self):
        asserting_result = (0, 0, False, False)
        side = np.array((0, -1, 0), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_starting_blank_before_player(self):
        asserting_result = (0, 2, False, False)
        side = np.array((0, 1, 1, 0), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_ending_blank_after_player(self):
        asserting_result = (3, 0, False, False)
        side = np.array((1, 1, 1, 0), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_ending_blank_after_op(self):
        asserting_result = (0, 0, False, True)
        side = np.array((-1, 0), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

class TestCapture(unittest.TestCase):
    def test_capture_simple(self):
        asserting_result = (0, 0, True, False)
        side = np.array((-1, -1, 1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_not_capture_blank(self):
        asserting_result = (0, 0, False, True)
        side = np.array((-1, -1, 0), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result
    
    def test_not_capture_side_board(self):
        asserting_result = (0, 0, False, True)
        side = np.array((-1, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_not_capture_after_blank(self):
        asserting_result = (0, 0, False, False)
        side = np.array((0, -1, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_not_capture_after_player(self):
        asserting_result = (1, 0, False, True)
        side = np.array((1, -1, -1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

class TestLongLine(unittest.TestCase):
    def test_long_normal_line(self):
        asserting_result = (3, 1, False, False)
        side = np.array((1, 1, 1, 0, 1, 0, 1, 1, 0, -1, 0, 1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result

    def test_long_op_line(self):
        asserting_result = (1, 0, False, True)
        side = np.array((1, -1, 1, -1, 0, 0, -1, 1, 0, -1, 0, 1), dtype=np.int64)
        result = check_side(side, 1, False)
        assert result == asserting_result
    
if __name__ == "__main__":
    unittest.main(verbosity=2)
        