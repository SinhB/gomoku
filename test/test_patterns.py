import unittest
import numpy as np
from get_patterns import check_line

"""
Return
    0: has_empty,
    1: left_capture,
    2: right_capture,
    3: close_two, 
    4: semi_close_two,
    5: open_two,
    6: close_three, 
    7: semi_close_three,
    8: open_three,
    9: close_four, 
    10: semi_close_four,
    11: open_four,
    12: five,
"""

class TestFive(unittest.TestCase):
    asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)

    def test_inside_five(self):
        """Inside"""
        #Inside left
        index= 3
        line = np.array((0,0,1,0,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside middle
        index= 4
        line = np.array((0,0,1,1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside right
        index= 5
        line = np.array((0,0,1,1,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

    def test_left_side_five(self):
        """Left side"""
        index= 2
        line = np.array((0,0,0,1,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

    def test_right_side_five(self):
        """Right side"""
        index= 6
        line = np.array((0,0,1,1,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

class TestOpenFour(unittest.TestCase):
    def test_inside_open_four_with_empty(self):
        """Inside with empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)

        #Empty right side of pos
        index = 3
        line = np.array((0,1,1,0,0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left side of pos
        index = 3
        line = np.array((0,1,0,0,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_left_side_open_four_with_empty(self):
        """Left side with empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
        
        #Empty right side of pos
        index = 2
        line = np.array((0,0,0,0,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty 2 right side of pos
        index = 2
        line = np.array((0,0,0,1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty 3 right side of pos
        index = 2
        line = np.array((0,0,0,1,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_right_side_open_four_with_empty(self):
        """Right side with empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
        
        #Empty left side of pos
        index = 5
        line = np.array((0,1,1,1,0,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty 2 left side of pos
        index = 5
        line = np.array((0,1,1,0,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty 3 left side of pos
        line = np.array((0,1,0,1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_inside_open_four_without_empty(self):
        """Inside without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)

        #Inside right
        index = 3
        line = np.array((0,1,1,0,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left
        index = 3
        line = np.array((0,0,1,0,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_left_side_open_four_without_empty(self):
        """Left side without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
        index = 2
        line = np.array((0,0,0,1,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_right_side_open_four_without_empty(self):
        """Right side without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
        index = 5
        line = np.array((0,0,1,1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

class TestSemiOpenFour(unittest.TestCase):
    player = 1

    def test_inside_semi_open_four_with_empty(self):
        """Inside with empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)

        #Inside right empty left side close right
        index = 4
        line = np.array((0,1,1,0,0,1,-1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right empty left side close left
        index = 4
        line = np.array((-1,1,1,0,0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right empty left side with side of board right
        index = 4
        line = np.array((0,1,1,0,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right empty left side with side of board left
        index = 3
        line = np.array((1,1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside middle empty left side close right
        index = 3
        line = np.array((0,1,0,0,1,1,-1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside middle empty left side close left
        index = 3
        line = np.array((-1,1,0,0,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside middle empty left side with side of board right
        index = 3
        line = np.array((0,1,0,0,1,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside middle empty left side with side of board left
        index = 2
        line = np.array((1,0,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside middle empty right close left
        index = 3
        line = np.array((-1,1,1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside middle empty right close right
        index = 3
        line = np.array((0,1,1,0,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside middle empty right with side of board left
        index = 2
        line = np.array((1,1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside middle empty right with side of board right
        index = 3
        line = np.array((0,1,1,0,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left empty right close left
        index = 2
        line = np.array((-1,1,0,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left empty right close right
        index = 2
        line = np.array((0,1,0,0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left empty right with side of board left
        index = 1
        line = np.array((1,0,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left empty right with side of board right
        index = 2
        line = np.array((0,1,0,0,1,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_left_side_semi_open_four_with_empty(self):
        """Left side with empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
        #Empty left close left
        index = 1
        line = np.array((-1,0,0,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left close right
        index = 1
        line = np.array((0,0,0,1,1,1,-1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left with side of board left
        index = 0
        line = np.array((0,0,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left with side of board right
        index = 1
        line = np.array((0,0,0,1,1,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty middle close left
        index = 1
        line = np.array((-1,0,1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty middle close right
        index = 1
        line = np.array((0,0,1,0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty middle with side of board left
        index = 0
        line = np.array((0,1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty middle with side of board right
        index = 1
        line = np.array((0,0,1,0,1,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right close left
        index = 1
        line = np.array((-1,0,1,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right close right
        index = 1
        line = np.array((0,0,1,1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right with side of board left
        index = 0
        line = np.array((0,1,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right with side of board right
        index = 1
        line = np.array((0,0,1,1,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_right_side_semi_open_four_with_empty(self):
        """Right side with empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
        
        #Empty left close left
        index = 5
        line = np.array((-1,0,1,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left close right
        index = 5
        line = np.array((0,1,0,1,1,0,-1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left with side of board left
        index = 4
        line = np.array((1,0,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left with side of board right
        index = 5
        line = np.array((0,1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty middle close left
        index = 5
        line = np.array((-1,1,1,0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty middle close right
        index = 5
        line = np.array((0,1,1,0,1,0,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty middle with side of board left
        index = 4
        line = np.array((1,1,0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty middle with side of board right
        index = 5
        line = np.array((0,1,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right close left
        index = 5
        line = np.array((-1,1,1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right close right
        index = 5
        line = np.array((0,1,1,1,0,0,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right with side of board left
        index = 4
        line = np.array((1,1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right with side of board right
        index = 5
        line = np.array((0,1,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_inside_semi_open_four_without_empty(self):
        """Inside without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
        
        #Inside left close left
        index = 2
        line = np.array((-1,1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left close right
        index = 2
        line = np.array((0,1,0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left with side board left
        index = 1
        line = np.array((1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left with side board right
        index = 2
        line = np.array((0,1,0,1,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right close left
        index = 3
        line = np.array((-1,1,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right close right
        index = 3
        line = np.array((0,1,1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right with side board left
        index = 2
        line = np.array((1,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right with side board right
        index = 3
        line = np.array((0,1,1,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result
        
    def test_left_side_semi_open_four_without_empty(self):
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
        pass
    def test_right_side_semi_open_four_without_empty(self):
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
        pass

class TestClosedFour(unittest.TestCase):
    player = 1

    def test_closed_four_with_empty(self):
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
        pass
    def test_closed_four_without_empty(self):
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
        pass

class TestThree(unittest.TestCase):
    def test_open_three_with_empty(self):
        pass
    def test_open_three_without_empty(self):
        pass
    def test_semi_open_three_with_empty(self):
        pass
    def test_semi_open_three_without_empty(self):
        pass
    def test_closed_three_with_empty(self):
        pass
    def test_closed_three_without_empty(self):
        pass

class TestTwo(unittest.TestCase):
    def test_open_two_with_empty(self):
        pass
    def test_open_two_without_empty(self):
        pass
    def test_semi_open_two_with_empty(self):
        pass
    def test_semi_open_two_without_empty(self):
        pass
    def test_closed_two_with_empty(self):
        pass
    def test_closed_two_without_empty(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)