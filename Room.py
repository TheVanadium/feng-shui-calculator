VALID_WALL_BREAK_TYPES = ["window", "entrance door", "miscellaneous door"]

class WallBreak:
    def __init__(self, position: int, width: int, type: str):
        self.position = position
        if self.position < 0:
            raise Exception(f"Wall break position must be at least 0. Input wall break position: {self.position}")
        self.width = width
        if self.width < 0:
            raise Exception(f"Wall break width must be at least 0. Input wall break width: {self.width}")
        self.type = type
        if self.type not in VALID_WALL_BREAK_TYPES:
            raise Exception(f"Invalid wall break type: {self.type}")
    
    def __lt__(self, other):
        return self.position < other.position
    def __le__(self, other):
        return self.position <= other.position
    def __eq__(self, other):
        return self.position == other.position
    def __ne__(self, other):
        return self.position != other.position
    def __gt__(self, other):
        return self.position > other.position
    def __ge__(self, other):
        return self.position >= other.position

    def __str__(self):
        return f"{self.type} of width {self.width} at position {self.position}"

    def get_end_point(self):
        return self.position + self.width

VALID_DIRECTION = ["north", "south", "east", "west"]  
class Wall:
    def __init__ (self, length: int, wall_breaks: [WallBreak], direction: str):
        self.wall_breaks = wall_breaks
        self.wall_breaks.sort()
        self.length = length

        if direction not in VALID_DIRECTION:
            raise Exception(f"Invalid wall direction: {direction}")
        self.direction = direction

        wall_breaks = sorted(wall_breaks)
        for i, wall_break in enumerate(wall_breaks):
            if wall_break.position + wall_break.width > self.length:
                raise Exception(f"Wall break {wall_break} is out of bounds. Wall length: {self.length}")
            if i == 0: continue
            if wall_break.position < wall_breaks[i-1].get_end_point():
                raise Exception(f"Wall breaks overlap. Wall break {wall_break} overlaps with wall break {wall_breaks[i-1]}")
            
    def get_feature(self, point: int):
        # Note: if there are two adjacent features on the same point, the one that is first in the list is returned
        if point < 0 or point > self.length:
            raise Exception(f"Point {point} is out of bounds. Wall length: {self.length}")
        for wall_break in self.wall_breaks:
            if point >= wall_break.position and point <= wall_break.get_end_point():
                return wall_break.type
        return None
          
class Room:
    def __init__ (self, walls: [Wall]):
        self.walls = walls

        HOME_POSITION = (0, 0)
        current_position = HOME_POSITION

        for i, wall in enumerate(walls):
            # checks if walls are oriented in impossible directions
            if i != 0:
                if wall.direction == walls[i-1].direction:
                    raise Exception(f"Consecutive wall directions cannot be the same. Wall {i} direction: {wall.direction}. Wall {i-1} direction: {walls[i-1].direction}")
                if walls[i-1].direction == "north" and wall.direction == "south" or \
                   walls[i-1].direction == "south" and wall.direction == "north" or \
                   walls[i-1].direction == "east" and wall.direction == "west" or \
                   walls[i-1].direction == "west" and wall.direction == "east": 
                    raise Exception (f"Consecutive wall directions cannot be opposite. Wall {i} direction: {wall.direction}. Wall {i-1} direction: {walls[i-1].direction}")
            
            # traces walls to see if they close the room
            if wall.direction == "north": current_position = (current_position[0], current_position[1] + wall.length)
            elif wall.direction == "south": current_position = (current_position[0], current_position[1] - wall.length)
            elif wall.direction == "east": current_position = (current_position[0] + wall.length, current_position[1])
            elif wall.direction == "west": current_position = (current_position[0] - wall.length, current_position[1])
            # note: this should never happen, because the direction is checked in the Wall class
            else: raise Exception(f"Invalid wall direction: {wall.direction}")
        
        if current_position != HOME_POSITION: raise Exception(f"Room is not closed. End wall terminates at: {current_position}")

    def get_length(self) -> int:
        """Gets the length of the room, the sum of the lengths of all walls.
        
        Returns:
            The length of the room."""
        length = 0
        for wall in self.walls:
            length += wall.length
        return length

    def get_feature(self, point: int, wall_index: int=None):
        """Gets the feature of a wall at a given point.
        
        Args:
            wall_index (int) (optional): The index of the wall to check. If not given, the wall is found by the point.
            point (int): The point to check.
            
        Returns:
            The feature of the given wall at the given point. If the point is not on a wall break, returns None.
            If the wall index is not given, returns the feature of the point is determined by tracing the walls.

        Raises:
            Exception: If the wall index is out of bounds.
            Exception: If the point is out of bounds.
        """
        if wall_index is None:
            if point < 0 or point > self.get_length():
                raise Exception(f"Point {point} is out of bounds. Room length: {self.get_length()}")
            for wall in self.walls:
                if point <= wall.length:
                    return wall.get_feature(point)
                point -= wall.length

        if wall_index < 0 or wall_index >= len(self.walls):
            raise Exception(f"Wall index {wall_index} is out of bounds. Number of walls: {len(self.walls)}")
        print (len(self.walls))
        return self.walls[wall_index].get_feature(point)

    def get_opposing_feature(self, point: int, wall_index: int=None):
        """Gets the feature of the opposing wall at a given point.
        
        Args:
            wall_index (int) (optional): The index of the wall to check. If not given, the wall is found by the point.
            point (int): The point to check.
            
        Returns:
            The feature of the opposing wall at the given point. If the point is not on a wall break, returns None.
            If the wall index is not given, returns the feature of the point is determined by tracing the walls.

        Raises:
            Exception: If the wall index is out of bounds.
            Exception: If the point is out of bounds.
        """
        # get wall of point, to get point-wall form (changes point to be relative to wall)
        if wall_index is None:
            wall_index = 0
            if point < 0 or point > self.get_length():
                raise Exception(f"Point {point} is out of bounds. Room length: {self.get_length()}")
            for wall in self.walls:
                if point <= wall.length:
                    break
                point -= wall.length
                wall_index += 1

        # get direction of wall
        wall_direction = self.walls[wall_index].direction
        opposite_directions = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east"
        }
        # find opposing wall, which is the first wall with the opposite direction which length > wall.length - point
        opposing_wall_index = wall_index
        while True:
            opposing_wall_index = (opposing_wall_index + 1) % len(self.walls)
            if self.walls[opposing_wall_index].direction == opposite_directions[wall_direction] and \
               self.walls[opposing_wall_index].length >= len(self.walls) - point:
                print (f"Opposite of wall is {opposing_wall_index}")
                break
            if opposing_wall_index == wall_index:
                # this should never happen, because the room is closed
                raise Exception(f"Could not find opposing wall for wall {wall_index} with direction {wall_direction} at point {point}")
        # get feature of opposing wall at point
        return self.walls[opposing_wall_index].get_feature(self.walls[opposing_wall_index].length - point)
