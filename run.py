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
    argument = sys.argv[1].lower()

    if argument == "dungeon":
        gtype = aqgame.GameType.DUNGEON
    elif argument == "world1":
        gtype = aqgame.GameType.WORLD1
    elif argument == "world2":
        gtype = aqgame.GameType.WORLD2
    else:
        print("\nUsage\n\trun.py [dungeon|world1|world2]")
        exit()

    game = aqgame.Game(gtype)
    game.run()
    
