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

    
#mining script by Mourn 8182 discord contact
#have a fire beetle and walk by mineable cliffs or caves , if necessary add ids on lines 4-5
mineableTiles = [0x0239,0x023a,0x023B,0x022C,0x023C,0x022D,0x022E,0x022F,0x00E4,0x00E6,0x00E5,0x00DC,0x00DE,0x00DD]#map art
mineableStatics = [0x053E,0x053B,0x0540,0x0541,0x0542,0x0543,0x0544,0x0555,0x0546,0x0547,0x0548,0x0549]#statics like cave tiles

pathCoords = [[1076, 1108]]
 
miningCoords = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1],[-2,-2],[-2,2],[2,-2],[2,2]]

oreIDs = [0x19B7,0x19B8,0x19B9,0x19BA]
bankIDs = [0x1779,0x1BF2,0x1726,0x3192,0x3193,0x3195,0x3197,0x3198,]
forgeID = 0x40005971
MasterRuneBook = 0x40F8B116
BankStone = 0x402AAAF6
resourceBox = 0x413985E1
mrbBook = 19
mrbSpots = 16
bankStone = False
portableForge = False
mrbBankBook = 20

        
def go(x1, y1):
    Coords = PathFinding.Route()
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = 10
    PathFinding.Go(Coords)
    Misc.Pause(400)
      
def checkTile(x,y):
    
    global count
    x1 = Player.Position.X+x
    y1 = Player.Position.Y+y
    z1 = Statics.GetLandZ(x1,y1,Player.Map) 
    tile = Statics.GetLandID(x1,y1,Player.Map)
    statics = Statics.GetStaticsTileInfo(x1,y1,Player.Map)
    if statics:
        for static in statics:
            if static.StaticID in mineableStatics:
                Misc.SendMessage("Static Found: {} @ {} {} {}".format(static.StaticID, x1,y1,Player.Position.Z))
                Misc.SendMessage('in a cave')
                mineStatic(x1,y1,Player.Position.Z,static.StaticID)
    if not statics:
        if tile in mineableTiles:
            Misc.SendMessage("Tile Found: {} @ {} {} {}".format(tile, x1,y1,z1))
            mineTile(x1,y1,z1)

def mineTile(x,y,z):
    while Items.BackpackCount(0x0E86) > 0:
        if Journal.Search('metal') or Journal.Search('see'):
            Journal.Clear()
            break
        Misc.SendMessage("Should Be mining")        
        Items.UseItemByID(0x0E86)
        Target.WaitForTarget(1200,False)
        Misc.SendMessage("{} {} {}".format(x,y,z),222)
        Target.TargetExecute(x,y,z)
        Misc.Pause(1200)
        if Player.Weight > Player.MaxWeight -45:
            smelt()
def mineStatic(x,y,z, gfx):
    while Items.BackpackCount(0x0E86) > 0:
        if Journal.Search('metal') or Journal.Search('see'):
            Journal.Clear()
            break
        Misc.SendMessage("Should Be mining")        
        Items.UseItemByID(0x0E86)
        Target.WaitForTarget(1200,False)
        Misc.SendMessage("{} {} {}: {}".format(x,y,z, hex(gfx)),222)
        Target.TargetExecute(x,y,z,gfx)
        Misc.Pause(1200)
        if Player.Weight > Player.MaxWeight -45:
            smelt()
            
def smelt():
        if portableForge:
            for item in Player.Backpack.Contains:
                if item.ItemID in oreIDs:
                    Items.UseItem(item)
                    Target.WaitForTarget(1000,False)
                    Target.TargetExecute(forgeID)
                    Misc.Pause(1200)
            Misc.Pause(2000)
        else:
            Misc.SendMessage("Recalling to forge", 444)
            common.MasterBook(MasterRuneBook, mrbBankBook, 2, "R")
            Misc.Pause(1200)
            for item in Player.Backpack.Contains:
                if item.ItemID in oreIDs:
                    Items.UseItem(item)
                    Target.WaitForTarget(1000,False)
                    Target.TargetExecute(forgeID)
                    Misc.Pause(1200)
            Misc.Pause(2000)
        bank()
         

def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:
            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list
    
def bank():
    bankItems = find(Player.Backpack.Serial, bankIDs)
    if bankStone:
        Misc.SendMessage("BANKING", 444)
        Items.UseItem(0x402AAAF6)
        Misc.Pause(500)
        for item in bankItems:
            Items.Move(item, resourceBox, 0)
            Misc.Pause(1200)
    else:
        Misc.SendMessage("RECALL BANKING", 444)
        common.MasterBook(MasterRuneBook, mrbBankBook, 1, "R")
        Misc.Pause(1200)
        Player.ChatSay(690, "bank")
        Misc.Pause(1000)
        for item in bankItems:
            Items.Move(item, resourceBox, 0)
            Misc.Pause(1200)
       
def Main():
    while not Player.IsGhost:
        #for pcoords in pathCoords:
            # go(pcoords[0],pcoords[1])
            
        for x in range(1,mrbSpots):
            Misc.SendMessage("Recalling to {}".format(x))
            common.MasterBook(MasterRuneBook, mrbBook, x, "R")
            Misc.Pause(2000)
            for mcoords in miningCoords:
                checkTile(mcoords[0],mcoords[1])
            Misc.Pause(200)
       
        
Main()