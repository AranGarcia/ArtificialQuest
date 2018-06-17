#!/usr/bin/env python3
'''
Executable script for project. Although refered to as a "game", the project
is actually a simulation for Artificial Intelligence class
'''
import sys
from game import artificialquest as aqgame

def printUsage():
    print("\nUsage\n\trun.py [dungeon|world1|world2]")

if len(sys.argv) < 2:
    printUsage()
else:
    argument = sys.argv[1].lower()

    if argument == "dungeon":
        gtype = aqgame.GameType.DUNGEON
    elif argument == "world1":
        gtype = aqgame.GameType.WORLD1
    elif argument == "world2":
        gtype = aqgame.GameType.WORLD2
    else:
        printUsage()
        exit(1)

    game = aqgame.Game(gtype)
    game.run()
    
