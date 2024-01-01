import unittest

import sys
sys.path.append('..')
from Room import Room, Wall, WallBreak

# also tests room components: Wall, WallBreak
class TestRoomClass(unittest.TestCase):
    def setUp(self):
        wall_break_1 = WallBreak(0, 2, "entrance door")
        wall_break_2 = WallBreak(1, 4, "window")
        walls = [
            Wall(5, [wall_break_1], "north"),
            Wall(7, [wall_break_2], "east"),
            Wall(5, [], "south"),
            Wall(7, [], "west")
        ]
        self.valid_room = Room(walls)

    # Room Tests:
    def test_valid_room(self):
        self.assertEqual(self.valid_room.get_length(), 24)

    def test_invalid_consecutive_directions(self):
        invalid_walls = [
            Wall(5, [], "north"),
            Wall(7, [], "north"),
            Wall(5, [], "east")
        ]
        with self.assertRaises(Exception) as context:
            Room(invalid_walls)
        self.assertTrue("Consecutive wall directions cannot be the same." in str(context.exception))

    def test_invalid_opposite_directions(self):
        invalid_walls = [
            Wall(5, [], "north"),
            Wall(7, [], "south"),
            Wall(5, [], "east")
        ]
        with self.assertRaises(Exception) as context:
            Room(invalid_walls)
        self.assertTrue("Consecutive wall directions cannot be opposite." in str(context.exception))

    def test_unclosed_room(self):
        # Test when the room is not closed (doesn't return to the starting point)
        unclosed_walls = [
            Wall(5, [], "north"),
            Wall(7, [], "east"),
            Wall(3, [], "south"),
            Wall(7, [], "west")
        ]
        with self.assertRaises(Exception) as context:
            Room(unclosed_walls)
        self.assertTrue("Room is not closed" in str(context.exception))

    def test_get_feature_valid_point(self):
        wall_break_1 = WallBreak(0, 2, "window")
        wall_break_2 = WallBreak(0, 6, "entrance door")
        walls = [
            Wall(5, [wall_break_1], "north"),
            Wall(7, [wall_break_2], "east"),
            Wall(5, [], "south"),
            Wall(7, [], "west")
        ]
        room = Room(walls)
        feature = room.get_feature(10)
        self.assertEqual(feature, "entrance door")

    def test_get_feature_invalid_point(self):
        with self.assertRaises(Exception) as context:
            self.valid_room.get_feature(25)
        self.assertTrue("Point 25 is out of bounds." in str(context.exception))

    def test_get_feature_invalid_wall_index(self):
        with self.assertRaises(Exception) as context:
            self.valid_room.get_feature(3, 4)
        self.assertTrue("Wall index 4 is out of bounds." in str(context.exception))

    # Wall Tests:
    def test_invalid_wall_direction(self):
        try:
            invalid_wall = Wall(7, [], "invalid direction")
            self.fail("Expected an exception, but none was raised.")
        except Exception as e:
            self.assertTrue("Invalid wall direction: invalid direction" in str(e))

    def test_wall_break_overlapping(self):
        with self.assertRaises(Exception) as context:
            wall_with_overlapping_wall_break = Wall(7, [WallBreak(0, 2, "window"), WallBreak(1, 2, "entrance door")], "north")
            self.fail("Expected an exception, but none was raised.")
        self.assertTrue("Wall breaks overlap." in str(context.exception))

    def test_adjacent_wall_breaks(self):
        wall_with_adjacent_wall_breaks = Wall(7, [WallBreak(0, 2, "window"), WallBreak(2, 2, "entrance door")], "north")
        self.assertEqual(wall_with_adjacent_wall_breaks.get_feature(0), "window")

    def test_wall_break_out_of_bounds(self):
        with self.assertRaises(Exception) as context:
            wall_with_out_of_bounds_wall_break = Wall(7, [WallBreak(6, 2, "entrance door")], "north")
            self.fail("Expected an exception, but none was raised.")
        self.assertTrue("is out of bounds. Wall length" in str(context.exception))

    def test_wall_breaks_on_edges(self):
        wall_with_edge_wall_break = Wall(7, [WallBreak(0, 2, "window"), WallBreak(6, 1, "entrance door")], "north")
        self.assertEqual(wall_with_edge_wall_break.get_feature(0), "window")
        self.assertEqual(wall_with_edge_wall_break.get_feature(6), "entrance door")

    # Wall Break Tests:
    def test_invalid_wall_type(self):
        try:
            invalid_wall_break = WallBreak(0, 2, "invalid type")
            self.fail("Expected an exception, but none was raised.")
        except Exception as e:
            self.assertTrue("Invalid wall break type: invalid type" in str(e))

if __name__ == '__main__':
    unittest.main()
