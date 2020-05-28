import common as common

for x in common.razorModules:
    x = str(x)
    exec(compile("common." + x + " = " + x, "<retards>", "exec"))
 
common.go(Player.Position.X + 1, Player.Position.Y + 1) # insula bank
