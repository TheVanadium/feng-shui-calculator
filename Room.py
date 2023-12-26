VALID_WALL_BREAK_TYPES = ["window", "entrance door", "miscellaneous door"]

class WallBreaks:
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
        return f"Wall break position: {self.position}, width: {self.width}, type: {self.type}"

    def get_end_point(self):
        return self.position + self.width

class Room:
    def __init__(self, dimension_ratio: float, wall_breaks: [WallBreaks]):
        self.dimension_ratio = dimension_ratio
        if self.dimension_ratio <= 0:
            raise Exception(f"Dimension ratio must be greater than 0. Input dimension ratio: {self.dimension_ratio}")
        
        self.wall_breaks = wall_breaks
        self.wall_breaks.sort()
        for i, wall_break in enumerate(wall_breaks):
            if i == 0: continue
            if wall_break.position < self.wall_breaks[i-1].get_end_point():
                raise Exception(f"Wall breaks cannot overlap. Overlapping wall break: {self.wall_breaks[i-1]} and {wall_break}")
        
        def get_corner_points(self):
            corner_points = []

            horizontal_wall_length = 50-(50/(self.dimension_ratio+1))
            vertical_wall_length = 50-horizontal_wall_length

            corner_points.append(0)
            corner_points.append(horizontal_wall_length)
            corner_points.append(50)
            corner_points.append(100-vertical_wall_length)

            corner_points = [round(point, 3) for point in corner_points]

            return corner_points
        self.corner_points = get_corner_points()