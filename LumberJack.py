import time
import sys
import math
from System.Collections.Generic import List

import common as common

for x in common.razorModules:
    x = str(x)
    exec(compile("common." + x + " = " + x, "<retards>", "exec"))
#Misc.SendMessage(str(common.__dir__()), 4095)


axeID = 0x4050B751
masterBook = 0x40F8B116    

recallSpots = {
  "Spot 1" : {
      "bookIndex" : 18,
      "spotIndex" : 1,
      "x" : 1187,
      "y" : 561,
      "z" : -88,
      "unk": 3287
  },
  "Spot 2" : {
      "bookIndex" : 18,
      "spotIndex" : 2,
      "x" : 1185,
      "y" : 538,
      "z" : -90,
      "unk": 3294
  },
}

  
def doRecall(bookIndex, spotIndex):
    currentX = Player.Position.X
    currentY = Player.Position.Y
    common.MasterBook(masterBook, bookIndex, spotIndex, "R")
    Misc.Pause(3000)
    if Player.Position.X == currentX and Player.Position.Y == currentY:
        return False
    else:
        return True
        
def mineSpot(spotX, spotY, spotZ, unk):
    for x in range(6):   
        Items.UseItem(axeID)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(spotX, spotY, spotZ, unk)
        Misc.Pause(2000)
        if Journal.Search("not enough"):
            Journal.Clear()
            Misc.Pause(1000)

ScanRadius = 5
TreeStaticID = [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274, 3275, 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3365, 3367, 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486, 3488, 3490, 3492, 3496]



# Variabili Sistema

            
tileinfo = List[Statics.TileInfo]
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
    Misc.SendMessage('--> Total Trees: %i' % (treenumber), 77)
        

##MainLoop###
for x in recallSpots:
    recall = doRecall( recallSpots[x]['bookIndex'], recallSpots[x]['spotIndex'])
    if recall:
        ScanStatic()
        for x in treeposx:
            spotnumber = treeposx.index(x)
            Misc.SendMessage("Going to {} {} {}".format(treeposx[spotnumber],treeposy[spotnumber], treeposz[spotnumber]))
            #common.go(Player.Position.X + 1, Player.Position.Y + 1)  ## WORKS
            #common.go(treeposx[spotnumber],treeposy[spotnumber])   ## DOES NOT WORK
            Player.PathFindTo(treeposx[spotnumber], treeposy[spotnumber], treeposx[spotnumber])
            
            Misc.Pause(1000)
            mineSpot(treeposx[spotnumber], treeposy[spotnumber], treeposz[spotnumber], treegfx[spotnumber])

Misc.Pause(3000)

