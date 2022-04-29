# wanderer
Wanderer game - Home Assignment

In the uml directory, there are two files.
uml_full.png contains all the anchestors, not only those that are created as part of the project.
uml_simple.png contins only classes created as part of the project.

The Wanderer game can be started by running the main.py
Extra features of the game:
-Enemy movement is based on a graph using Breadth First Search, all the enemies are moving to the direction of the Hero https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
-The game has sound, it is tested only on Windows

Features to be implemented:
-The game should use multi-threading, so the graphic tasks wouldn't be blocked by the code that is responsible for the game logic
-The development hasn't been started based on tests, it would be better to write the tests first
-There is no logic right now to cover the scenario when multiple enemies are stepping to the same tile. It is avoided only when the game starts.


