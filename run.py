#!/usr/bin/env python3
'''
Executable script for project. Although refered to as a "game", the project
is actually a simulation for Artificial Intelligence class
'''
import sys
from game import artificialquest as aqgame

if len(sys.argv) < 2:
    print ("\n\tIntroduce practice2 or project.\n")
else:
    if sys.argv[1] == "practice2":
        game = aqgame.Game(False)
        game.run()
    elif sys.argv[1] == "project":
        game = aqgame.Game(True)
        game.run()
    else:
        print ("This option is not valid.")
