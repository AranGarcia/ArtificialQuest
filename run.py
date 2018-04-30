#!/usr/bin/env python3
'''
Executable script for project. Although refered to as a "game", the project
is actually a simulation for Artificial Intelligence class
'''
import sys
from game import artificialquest as aqgame

if len(sys.argv) < 2:
    print("\nUsage\n\trun.py [dungeon|world]")
else:
    if sys.argv[1] == "dungeon":
        game = aqgame.Game(False)
        game.run(False)
    elif sys.argv[1] == "world":
        game = aqgame.Game(True)
        game.run(True)
    else:
        print("\nUsage\n\trun.py [dungeon|world]")
