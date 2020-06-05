import common as common

for x in common.razorModules:
    x = str(x)
    exec(compile("common." + x + " = " + x, "<retards>", "exec"))

common.MasterBook(0x40F8B116, 1, 8, "R")
