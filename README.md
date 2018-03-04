# Artificial Quest
Project for artificial intelligence class. The main purpose of the project is to
simulate the activity of intelligent agents on a map, with established goals and
obstacles to analyze.

# Usage
Execute the run.py script from the root of the project.
`./run.py`

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
