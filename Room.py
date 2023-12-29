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
            if i == 0: continue
            if wall_break.position < wall_breaks[i-1].get_end_point():
                raise Exception(f"Wall breaks overlap. Wall break {wall_break} overlaps with wall break {wall_breaks[i-1]}")
            if wall_break.position + wall_break.width > self.length:
                raise Exception(f"Wall break {wall_break} is out of bounds. Wall length: {self.length}")
            
    def get_feature(self, point: int):
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

    def get_feature(self, wall_index: int, point: int):
        """Gets the feature of a wall at a given point.
        
        Args:
            wall_index (int): The index of the wall to check.
            point (int): The point to check.
            
        Returns:
            The feature of the given wall at the given point.

        Raises:
            Exception: If the wall index is out of bounds.
        """
        if wall_index < 0 or wall_index >= len(self.walls):
            raise Exception(f"Wall index {wall_index} is out of bounds. Number of walls: {len(self.walls)}")
        return self.walls[wall_index].get_feature(point)
