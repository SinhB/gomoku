import unittest
import numpy as np
from check_line import check_line
# from get_patterns import check_line

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
        line = np.array((-1,1,0,1,1,0,0))
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
        """Left side without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)

        #Close left
        index = 1
        line = np.array((-1,0,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        index = 1
        line = np.array((0,0,1,1,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side left
        index = 0
        line = np.array((0,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side right
        index = 1
        line = np.array((0,0,1,1,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        
    def test_right_side_semi_open_four_without_empty(self):
        """Right side without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)

        #Close left
        index = 4
        line = np.array((-1,1,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        index = 4
        line = np.array((0,1,1,1,0,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side left
        index = 3
        line = np.array((1,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side right
        index = 4
        line = np.array((0,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

class TestClosedFour(unittest.TestCase):
    asserting_result = (False, False, False, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)

    def test_inside_closed_four(self):
        """Inside"""
        #Inside left
        index = 2
        line = np.array((-1,1,0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside left with board side left
        index = 1
        line = np.array((1,0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside left with board side right
        index = 2
        line = np.array((-1,1,0,1,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside left with both board side
        index = 1
        line = np.array((1,0,1,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside right
        index = 3
        line = np.array((-1,1,1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside right with board side left
        index = 2
        line = np.array((1,1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside right with board side right
        index = 3
        line = np.array((-1,1,1,0,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside right with both board side
        index = 2
        line = np.array((1,1,0,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

    def test_left_side_closed_four(self):
        """Left side"""
        
        #Left side
        index = 1
        line = np.array((-1,0,1,1,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side with board side left
        index = 0
        line = np.array((0,1,1,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side with board side right
        index = 1
        line = np.array((-1,0,1,1,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side with both board side
        index = 0
        line = np.array((0,1,1,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

    def test_right_side_closed_four(self):
        """Right side"""
        
        #Right side
        index = 4
        line = np.array((-1,1,1,1,0,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side with board side left
        index = 3
        line = np.array((1,1,1,0,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side with board side right
        index = 4
        line = np.array((-1,1,1,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side with both board side
        index = 3
        line = np.array((1,1,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

class TestOpenThree(unittest.TestCase):
    def test_inside_open_three_with_empty(self):
        """Inside"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
        
        #Inside left
        index = 2
        line = np.array((0,1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right
        index = 3
        line = np.array((0,1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside  with 2 empty
        index = 3
        line = np.array((0,1,0,0,0,1,0))
        result = check_line(line, index, 1)
        assert result != asserting_result

    def test_left_side_open_three_with_empty(self):
        """Left side"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
        
        #Left side empty left
        index = 1
        line = np.array((0,0,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Left side empty right
        index = 1
        line = np.array((0,0,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_right_side_open_three_with_empty(self):
        """Right side"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
        
        #Right side empty left
        index = 4
        line = np.array((0,1,0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Right side empty right
        index = 4
        line = np.array((0,1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_open_three_without_empty(self):
        """Without Empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
        
        #Left side
        index = 1
        line = np.array((0,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Middle
        index = 2
        line = np.array((0,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Right side
        index = 3
        line = np.array((0,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

class TestSemiOpenThree(unittest.TestCase):
    def test_inside_semi_open_three_with_empty(self):
        """Inside empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)

        #Inside left close left
        index = 2
        line = np.array((-1,1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left close right
        index = 2
        line = np.array((0,1,0,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left with board side left
        index = 1
        line = np.array((1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside left with board side right
        index = 2
        line = np.array((0,1,0,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right close left
        index = 3
        line = np.array((-1,1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right close right
        index = 3
        line = np.array((0,1,0,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right with board side left
        index = 2
        line = np.array((1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Inside right with board side right
        index = 3
        line = np.array((0,1,0,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result


    def test_left_side_semi_open_three_with_empty(self):
        """Left side with empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
        
        #Empty left close left
        index = 1
        line = np.array((-1,0,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left close right
        index = 1
        line = np.array((0,0,0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left with board side left
        index = 0
        line = np.array((0,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left with board side right
        index = 1
        line = np.array((0,0,0,1,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right close left
        index = 1
        line = np.array((-1,0,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right close right
        index = 1
        line = np.array((0,0,1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right with board side left
        index = 0
        line = np.array((0,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right with board side right
        index = 1
        line = np.array((0,0,1,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result


    def test_right_side_semi_open_three_with_empty(self):
        """Right side with empty"""
        asserting_result = (True, False, False, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
        
        #Empty left close left
        index = 4
        line = np.array((-1,1,0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left close right
        index = 4
        line = np.array((0,1,0,1,0,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left with board side left
        index = 3
        line = np.array((1,0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty left with board side right
        index = 4
        line = np.array((0,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right close left
        index = 4
        line = np.array((-1,1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right close right
        index = 4
        line = np.array((0,1,1,0,0,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right with board side left
        index = 3
        line = np.array((1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Empty right with board side right
        index = 4
        line = np.array((0,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_inside_semi_open_three_without_empty(self):
        """Inside without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
    
        #Close left
        index = 2
        line = np.array((-1,1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        index = 2
        line = np.array((0,1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side left
        index = 1
        line = np.array((1,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side right
        index = 2
        line = np.array((0,1,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_left_side_semi_open_three_without_empty(self):
        """Left without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)

        #Close left
        index = 1
        line = np.array((-1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        index = 1
        line = np.array((0,0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side left
        index = 0
        line = np.array((0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side right
        index = 1
        line = np.array((0,0,1,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_right_side_semi_open_three_without_empty(self):
        """Right side without empty"""
        asserting_result = (False, False, False, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)

        #Close left
        index = 3
        line = np.array((-1,1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        index = 3
        line = np.array((0,1,1,0,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side left
        index = 2
        line = np.array((1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board side right
        index = 3
        line = np.array((0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

class TestClosedThree(unittest.TestCase):
    asserting_result = (False, False, False, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0)
    
    def test_inside_closed_three(self):
        #Inside
        index = 2
        line = np.array((-1,1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside with board side left
        index = 1
        line = np.array((1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside with board side right
        index = 2
        line = np.array((-1,1,0,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Inside with both board side
        index = 1
        line = np.array((1,0,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

    def test_left_side_closed_three(self):
        #Left side
        index = 1
        line = np.array((-1,0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side with board side left
        index = 0
        line = np.array((0,1,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side with board side right
        index = 1
        line = np.array((-1,0,1,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side with both board side
        index = 0
        line = np.array((0,1,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

    def test_right_side_closed_three(self):
        #Right side
        index = 3
        line = np.array((-1,1,1,0,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side with board side left
        index = 2
        line = np.array((1,1,0,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side with board side right
        index = 3
        line = np.array((-1,1,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side with both board side
        index = 2
        line = np.array((1,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

class TestOpenTwo(unittest.TestCase):
    def test_left_side_open_two_with_empty(self):
        """Left with empty"""
        asserting_result = (True, False, False, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
        
        index = 1
        line = np.array((0,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_right_side_open_two_with_empty(self):
        """Right with empty"""
        asserting_result = (True, False, False, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
        index = 3
        line = np.array((0,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_left_side_open_two_without_empty(self):
        """Left without empty"""
        asserting_result = (False, False, False, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
        
        index = 1
        line = np.array((0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_right_side_open_two_without_empty(self):
        """Right without empty"""
        asserting_result = (False, False, False, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
        index = 2
        line = np.array((0,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

class TestSemiOpenTwo(unittest.TestCase):
    def test_left_side_semi_open_two_with_empty(self):
        """Left with empty"""

        #Close left
        asserting_result = (True, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 1
        line = np.array((-1,0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        asserting_result = (True, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 1
        line = np.array((0,0,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board left
        asserting_result = (True, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 0
        line = np.array((0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board right
        asserting_result = (True, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 1
        line = np.array((0,0,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result
    
    def test_right_side_semi_open_two_with_empty(self):
        """Right with empty"""

        #Close left
        asserting_result = (True, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 3
        line = np.array((-1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        asserting_result = (True, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 3
        line = np.array((0,1,0,0,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board left
        asserting_result = (True, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 2
        line = np.array((1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board right
        asserting_result = (True, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 3
        line = np.array((0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result
    
    def test_left_side_semi_open_two_without_empty(self):
        """Left side without empty"""

        #Close left
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 1
        line = np.array((-1,0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 2
        line = np.array((0,0,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board left
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 0
        line = np.array((0,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board right
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 2
        line = np.array((0,0,0,1))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_right_side_semi_open_two_without_empty(self):
        """Right side without empty"""

        #Close left
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 2
        line = np.array((-1,1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Close right
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 3
        line = np.array((0,0,1,0,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board left
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 1
        line = np.array((1,0,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

        #Board right
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 3
        line = np.array((0,0,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

class TestClosedTwo(unittest.TestCase):
    asserting_result = (False, False, False, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    def test_left_closed_two(self):
        """Left side"""
        
        #Left side
        index = 1
        line = np.array((-1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side board left
        index = 0
        line = np.array((0,1,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side board right
        index = 1
        line = np.array((-1,0,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Left side both side board
        index = 0
        line = np.array((0,1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result
        
    def test_right_closed_two(self):
        """right side"""
        
        #Right side
        index = 2
        line = np.array((-1,1,0,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side board left
        index = 1
        line = np.array((1,0,-1))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side board right
        index = 2
        line = np.array((-1,1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

        #Right side both side board
        index = 1
        line = np.array((1,0))
        result = check_line(line, index, 1)
        assert result == self.asserting_result

class TestExoticCapture(unittest.TestCase):
    def test_open_two_to_open_three(self):
        #Should eat left and create open three
        asserting_result = (False, True, False, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
        index = 4
        line = np.array((0,1,-1,-1,0,1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_eat_right_for_nothing(self):
        #Should only eat right and create nothing
        asserting_result = (False, False, True, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 2
        line = np.array((-1,-1,0,-1,-1,1,0,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_eat_everyone(self):
        #Should only eat left right up down ...
        asserting_result = (False, True, True, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 3
        line = np.array((1,-1,-1,0,-1,-1,1,0))
        result = check_line(line, index, 1)
        assert result == asserting_result

class TestLongLine(unittest.TestCase):
    def test_long_line(self):
        asserting_result = (False, False, False, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        index = 4
        line = np.array((0,0,-1,0,0,1,-1,1,0,1,-1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_another_long_line(self):
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
        index = 9
        line = np.array((1,0,0,1,0,0,1,0,1,0,1,0,-1,1,-1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_another_long_line_again(self):
        asserting_result = (False, False, False, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0)
        index = 9
        line = np.array((1,0,0,1,0,0,1,0,-1,0,1,1,-1,0,-1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

    def test_another_long_line_again(self):
        #Closed four with empty ->> strong like semi-closed-four ???
        asserting_result = (True, False, False, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
        index = 9
        line = np.array((1,0,0,1,0,0,0,-1,1,0,1,0,1,-1,-1,0,1,-1))
        result = check_line(line, index, 1)
        assert result == asserting_result

if __name__ == "__main__":
    unittest.main(verbosity=2)