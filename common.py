
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
    Coords.DebugMessage = True
    #Misc.SendMessage("GO")
    PathFinding.Go(Coords)
    
    
 ## Find an array of items ##   
def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:

            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list     
    
##### Master Rune Book Code  
def MasterBook(serial, book, rune, spell="R"):
    nbook = book + 1
    baseRune = 0
    if spell == 'R':  # recall
        baseRune = 5
    elif spell == 'G':   # gate
        baseRune = 6
    elif spell == 'S':   # sacred journey
        baseRune = 7
    else:
        Misc.SendMessage("Spell should be one of R, G or S, quitting", 4095)
        return

    newrune = (rune - 1) * 6 + baseRune
    Mbook = Items.FindBySerial(serial)
    if Mbook != None:
        Items.UseItem(Mbook)
        Misc.Pause(200)
        Gumps.WaitForGump(354527139, 10000)
        Gumps.SendAction(354527139, nbook)
        Gumps.WaitForGump(128397316, 10000)
        Gumps.SendAction(128397316, newrune)
    else:
        Misc.SendMessage("Can't find the book")



        
### Static Scanner #####
from System.Collections.Generic import List

       
ScanRadius = 10
TreeStaticID = [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274, 3275, 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3365, 3367, 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486, 3488, 3490, 3492, 3496]



#tileinfo = List[Statics.TileInfo]
treeposx = []
treeposy = []
treeposz = []
treegfx = []
treenumber = 0
blockcount = 0
lastrune = 5
onloop = True

def ScanStatic( ): 
    global treenumber
    Misc.SendMessage("--> Start Tile Scan", 77)
    minx = Player.Position.X - ScanRadius
    maxx = Player.Position.X + ScanRadius
    miny = Player.Position.Y - ScanRadius
    maxy = Player.Position.Y + ScanRadius

    while miny <= maxy:
        while minx <= maxx:
            tileinfo = Statics.GetStaticsTileInfo(minx, miny, Player.Map)
            if tileinfo.Count > 0:
                for tile in tileinfo:
                    for staticid in TreeStaticID:
                        if staticid == tile.StaticID:
                            Misc.SendMessage('--> Tree X: %i - Y: %i - Z: %i' % (minx, miny, tile.StaticZ), 66)
                            treeposx.Add(minx)
                            treeposy.Add(miny)
                            treeposz.Add(tile.StaticZ)
                            treegfx.Add(tile.StaticID)
            else:
                Misc.NoOperation()
            minx = minx + 1
        minx = Player.Position.X - ScanRadius            
        miny = miny + 1
    treenumber = treeposx.Count 
    if treenumber > 0:
        return tree
    Misc.SendMessage('--> Total Trees: %i' % (treenumber), 77)
    
    def checkPositionChanged(self, posX, posY, noise=False):
        recallStatus = None
        while Player.Position.X == posX and Player.Position.Y == posY:
            if Journal.Search("blocked"):
                Journal.Clear()
                if noise:
                    Misc.SendMessage("Rune Blocked", 100)
                recallStatus = "blocked"
                return recallStatus
            elif Journal.Search("mana"):
                Journal.Clear()
                if noise:
                    Misc.SendMessage("out of mana", 100)
                recallStatus = "mana"
            else:
                recallStatus = "good"

        return recallStatus
    
