import common as common

for x in common.razorModules:
    x = str(x)
    exec(compile("common." + x + " = " + x, "<retards>", "exec"))

common.MasterBook(0x40F8B116, 2, 1, "R")
Misc.Pause(3000)
common.MasterBook(0x40F8B116, 2, 2, "R")
Misc.Pause(3000)