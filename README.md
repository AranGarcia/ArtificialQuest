# Artificial Quest
Project for artificial intelligence class. The main purpose of the project is to
simulate the activity of intelligent agents on a map, with established goals and
obstacles to analyze.

## Usage
Execute the run.py script from the root of the project with the name of scenario.

`./run.py [dungeon|world1|world2]`

### Dungeon
The dungeon is the basic environment for blind search algorithms. The interaction with the map is mostly setting a start point and a goal. Also, the algorithm is choosable for graphic visualization of the amount of nodes explored until the goal is reached.

After points are set the start button blacks out the screen, simulating the effect of the knowledge of the agent about the map. Black tiles are unexplored while lit tiles are otherwise.

In this environment, the search algorithms used are:

- Breadth first search
- Depth first search
- Iterative depth first search

One important thing to notices is that depth first and iterative depth first require having an order of directions to go (e.g. in order: UP, LEFT, RIGHT, DOWN), which are input with they arrow keys.

### World 1

The world map is a multi agent environment (heroes) in which the team must finish all the missions with a minimum cost for the the group as a whole. The cost is the sum of the efforts each agent has done to walk a certain path with different types of terrains; each terrain affects each hero differently (e.g. an octopus travels with less effort through water than through desert, while a monkey travels forest with ease while water tiles are more costly). After each mission is done, a portal will open and all heroes must go to the portal and successfully acomplish their mission.

The user must set the objectives on a map by selecting the icon at the bottom at the screen and click the tile where the objective will be set. The position of the heroes are set in the same way. When all is set, the start button will start calculating costs before assigning missions to heroes.

The search algorithm used is:
- A* search algorithm

### World 2

The search algorithm used in this map:
- Genetic algorithm

# Map customization
The maps are included in **src/maps**. To overwrite a map to customize it, be sure to use the following digits that correspond to a certain terrain:

| Terrain | Value |
|-------- |-------|
|  Wall   |   0   |
|  Road   |   1   |
| Mountain|   2   |
|  Land   |   3   |
|  Water  |   4   |
|  Sand   |   5   |
| Forest  |   6   |

If an invalid value is written to the map data file, it will be saved as 0.
