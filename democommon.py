# Razor module]
mods = """
AutoLoot
BandageHeal
BuyAgent
DPSMeter
Dress
Friend
Gumps
Items
Journal
Misc
Mobiles
Organizer
PathFinding
Player
Restock
Scavenger
SellAgent
Spells
Statics
Target
Timer
Vendor
"""

razorModules = [x.strip() for x in mods.split("\n") if len(x) > 0]


def go(x1, y1):
    Coords = PathFinding.Route() 
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = -1
    PathFinding.Go(Coords)
