# Feng Shui Calculator Documentation

### In progress:
1. Implement a system to represent rooms in code

### To do:
2. Create an evaluation function that determines how well a given bed placement adheres to the rules of Feng Shui
3. Create an API that takes room configuration as an input and produces the optimal bed placement as an output
4. Create a web app that allows users to input their room configuration and see the optimal bed placement

## Room Representation
### Current Limitations:
Walls but be perpendicular to each other. This means that rooms with diagonal or curved walls cannot be represented.

### Room Object
The Room object is a list of Wall objects that form a closed polygon. The order of the walls in the list is important, as it determines the order in which the walls are connected to each other. The first wall in the list is connected to the second wall, the second wall is connected to the third wall, and so on. The last wall in the list is connected to the first wall.

#### Wall Object
The wall object is meant to represent a wall in a room, as well as its orientation relative to the previous wall. It contains WallBreak objects to represent doors, windows, and the like.
    - `length`: The length of the wall in in whatever units the user desires, just ensure it is consistent throughout the room.
    - `wall_breaks`: A list of WallBreak objects. 
    - `direction`: The direction the wall extends in relative to the previous wall (only useful in the context of the Room object).

#### WallBreak Object
The WallBreak object represents doors, windows, or any interruption in the wall.
    - `position`: The position of the wall break along the wall, in units consistent with the Wall object.
    - `length`: The length of the wall break, in units consistent with the Wall object.