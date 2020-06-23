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

    
#Recal To Luna Moongate    
common.MasterBook(hobo.MasterRuneBook, 1, 8, "R")
