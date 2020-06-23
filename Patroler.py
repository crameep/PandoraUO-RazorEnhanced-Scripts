import time
import sys
import math
#
if not Misc.CurrentScriptDirectory() in sys.path:
    sys.path.append(Misc.CurrentScriptDirectory())
#

import System
import common as common
import hoboconstants as hobo

for x in common.razorModules:
    x = str(x)
    exec(compile("common." + x + " = " + x, "<retards>", "exec"))

startX = Player.Position.X
startY = Player.Position.Y

positions = { 
    1: [15,15],
    2: [-15,15],
    3: [-15,0],
    4: [15,0],
    5: [-15,-0],
    6: [1,1]
    }

#Recal To Luna Moongate    

while not Player.IsGhost:
    for pos in positions:
        Misc.SendMessage(positions[pos][1])
        common.go(startX + positions[pos][0], startY + positions[pos][1])
        Misc.Pause(6000)