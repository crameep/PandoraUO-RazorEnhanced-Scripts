import time
import sys
import math

if not Misc.CurrentScriptDirectory() in sys.path:
    sys.path.append(Misc.CurrentScriptDirectory())

import common

from System.Collections.Generic import List
from System import Byte, Int32

Journal.Clear()
Packhorse = 0x40056C38

shovelID = 0x0F39
pickaxeID = 0x0E86
waitForTarget = 5000
waitAfterMining = 2000
waitAfterPickAxe = 4000
pickaxe_spots = List[int] (( 0x136D, 0x1367, 0x136A)) 

Motion_directions = [
                     ("North", 0, -1), 
                     ("Right", +1, -1),
                     ("East", +1, 0),
                     ("Down", +1, +1),
                     ("South", 0, +1),
                     ("Left", -1, +1),
                     ("West", -1, 0),
                     ("Up", -1, -1),
                     ("North", 0, -1), 
                     ("Right", +1, -1),
                     ("East", +1, 0),
                     ("Down", +1, +1),
                     ("South", 0, +1),
                     ("Left", -1, +1),
                     ("West", -1, 0),
                     ("Up", -1, -1),
                     ] 
MotionMap = {
             "North": (0, -1), 
             "Right": (+1, -1),
             "East": (+1, 0),
             "Down": (+1, +1),
             "South": (0, +1),
             "Left": (-1, +1),
             "West": (-1, 0),
             "Up": (-1, -1),
             "North": (0, -1), 
             "Right": (+1, -1),
             "East": (+1, 0),
             "Down": (+1, +1),
             "South": (0, +1),
             "Left": (-1, +1),
             "West": (-1, 0),
             "Up": (-1, -1),
             } 
                     

def adjacent_passable(x, y, right):
    # right True means process top to bottom, False means bottom to top
    list_range = range( 0, len(Motion_directions)+1, 1)
    if not right:
        list_range = range(len(Motion_directions)-1, -1, -1)
    
    if right:
        index = 0
        passable = True
        while index < len(Motion_directions) and passable:
            Misc.SendMessage("index: {}".format(index))
            new_x = x+Motion_directions[index][1]
            new_y = y+Motion_directions[index][2]
            land_id = Statics.GetLandID(new_x, new_y, Player.Map)
            passable = not (Statics.GetLandFlag(land_id, "Impassable"))
            index += 1
        # index should be first not passable    
        while index < len(Motion_directions) and not passable:
            Misc.SendMessage("index: {}".format(index))    
            new_x = x+Motion_directions[index][1]
            new_y = y+Motion_directions[index][2]
            land_id = Statics.GetLandID(new_x, new_y, Player.Map)
            passable = not (Statics.GetLandFlag(land_id, "Impassable"))
            index += 1
    else:
        index = len(Motion_directions)-1
        passable = True
        while index >= 0 and passable:
            Misc.SendMessage("index: {}".format(index))
            new_x = x+Motion_directions[index][1]
            new_y = y+Motion_directions[index][2]
            land_id = Statics.GetLandID(new_x, new_y, Player.Map)
            passable = not (Statics.GetLandFlag(land_id, "Impassable"))
            index -= 1
        # index should be first not passable    
        while index >= 0 and not passable:    
            new_x = x+Motion_directions[index][1]
            new_y = y+Motion_directions[index][2]
            land_id = Statics.GetLandID(new_x, new_y, Player.Map)
            passable = not (Statics.GetLandFlag(land_id, "Impassable"))
            index -= 1
            
    Misc.SendMessage("Checking X: {} Y: {} passable: {}".format(new_x, new_y, passable))
    if passable:
       Misc.SendMessage("Found adjacent passable at X: {} Y: {} passable: {}".format(new_x, new_y, passable))
       return new_x, new_y                
    return 0,0
   
def compute_cur_square(x, y):
    SquareSize = 9
    square_points = []
    origin_x = (int(x/SquareSize)) * SquareSize
    origin_y = (int(y/SquareSize)) * SquareSize
    for new_x in range(origin_x, origin_x+8):
        for new_y in range(origin_y, origin_y+8):
            square_points.append( (new_x, new_y) )
    return square_points
    
def find_new_spot(x, y):
    cur_square = compute_cur_square(x, y)
    facing = Player.Direction
    Mobiles.Message(Player.Serial, 5, facing)
    cur_x = x
    cur_y = y
    for _ in range(0, 200):
        goto_tuple = adjacent_passable(cur_x, cur_y, True)
        if goto_tuple not in cur_square:
           #Misc.SendMessage("cur_square : {}".format(str(cur_square))) 
           Misc.SendMessage("Found a Place: {}".format(str(goto_tuple)))  
           break
        else:
            cur_x = goto_tuple[0]
            cur_y = goto_tuple[1]
    if goto_tuple[0] != 0:
        Misc.SendMessage("You should go to X: {} Y: {}".format(goto_tuple[0], goto_tuple[1]))
        return goto_tuple[0], goto_tuple[1]
    Misc.SendMessage("Could not find a new spot X: {} Y: {}".format(x, y))
    return 0, 0
    
    
def getVeins():
    findVeins = Items.Filter()
    findVeins.Enabled = True
    findVeins.OnGround = 1
    findVeins.Movable = False
    findVeins.RangeMin = -1
    findVeins.RangeMax = 2
    findVeins.Graphics = pickaxe_spots
    findVeins.Hues = List[int]((  ))
    findVeins.CheckIgnoreObject = True
    listVeins = Items.ApplyFilter(findVeins)
    return listVeins

#    
CaveTiles = [ 0x245, 0x246, 0x247, 0x248, 0x249, 0x22b, 0x22c, 0x22d, 0x22e, 0x22f ]    
def MineSpot():
    x_delta, y_delta = MotionMap[Player.Direction]
    x = Player.Position.X + x_delta
    y = Player.Position.Y + y_delta
    land_id = Statics.GetLandID(x, y, Player.Map)
    Misc.SendMessage("X: {} Y: {} LandID: 0x{:x} ImPassable: {}".format(x, y, land_id, Statics.GetLandFlag(land_id, "Impassable")))
    if Statics.GetLandFlag(land_id, "Impassable") or land_id in CaveTiles:
        Journal.Clear()
        while True:
            if Journal.Search('no metal'):
                break
            if Journal.Search('Target cannot be seen'):
                break
            if Journal.Search('You can\'t mine there'):
                break
            tileinfo = Statics.GetStaticsLandInfo(x, y, Player.Map)
            Items.UseItemByID(shovelID,0)
            Target.WaitForTarget(waitForTarget,False)                    
            tiles = Statics.GetStaticsTileInfo(x, y, Player.Map)
            Misc.SendMessage("LandID: 0x{:x} #tiles{}".format(tileinfo.StaticID, len(tiles)), 5)
            if tileinfo.StaticID in CaveTiles and len(tiles) > 0:
                #Misc.SendMessage("StaticID: 0x{:x} #tiles{}".format(tiles[0].StaticID, len(tiles)), 5)
                Target.TargetExecute(x, y, 0, tiles[0].StaticID)
            else:
                Target.TargetExecuteRelative(Player.Serial, 1)
            Misc.Pause(waitAfterMining)
            if Target.HasTarget(): 
                Target.Cancel()                    
            CheckWeight()    
    listVeins = getVeins()
    if listVeins != None and len(listVeins) > 0:
        for vein in listVeins:
            while Items.FindBySerial(vein.Serial):
                Items.UseItemByID(pickaxeID,0)
                Target.WaitForTarget(waitForTarget,False)
                Target.TargetExecute(vein)
                Misc.Pause(waitAfterMining)
                CheckWeight()
            if Target.HasTarget(): 
                Target.Cancel()
            #tileinfo = Statics.GetStaticsTileInfo(Player.Position.X,Player.Position.Y, Player.Map)
            #if tileinfo.Count > 0:
            #    for tile in tileinfo:
            #    if tile.StaticID > 1340 and tile.StaticID < 1350 and tile.StaticZ == Player.Position.Z :

def CheckWeight():
    if Player.Weight > (Player.MaxWeight*.9):
        if Misc.CheckSharedValue("BagOfHolding"):
            BOH = Misc.ReadSharedValue("BagOfHolding")
            ore = Items.FindByID(0x19B9, -1, Player.Backpack.Serial)
            while ore != None:
                Items.Move(ore, BOH, 0)
                Misc.Pause(2000)
                ore = Items.FindByID(0x19B9, -1, Player.Backpack.Serial)
                if Player.Weight < Player.MaxWeight:
                    Journal.Clear()    
        else:
            # Move to Packhorse
            ore = Items.FindByID(0x19B9, -1, Player.Backpack.Serial)
            while ore != None:
                Items.Move(ore, Packhorse, 0)
                Misc.Pause(2000)
                ore = Items.FindByID(0x19B9, -1, Player.Backpack.Serial)
                if Player.Weight < Player.MaxWeight:
                    Journal.Clear()
                
def WeaponInHand():
    w_r = Player.GetItemOnLayer('RightHand')
    #Misc.SendMessage("right={}".format(w_r))
    w_l = Player.GetItemOnLayer('LeftHand')
    #Misc.SendMessage("left={}".format(w_l))
    if w_l != None: 
       weapon = w_l
    elif w_r != None:    
       weapon = w_r
    else:
       weapon = None       
    return weapon

stop = False
while not stop:    
    CheckWeight()
    MineSpot()
    new_x, new_y = 0, 0 #find_new_spot(Player.Position.X, Player.Position.Y)
    if new_x != 0:
        land_id = Statics.GetLandID(new_x, new_y, Player.Map)
        passable =Statics.GetLandFlag(land_id, "Impassable")
        Misc.SendMessage("Go To X: {} Y: {} passable: {}".format(new_x, new_y, passable))    
        route = PathFinding.Route()
        route.X = new_x
        route.Y = new_y
        route.MaxRetry = 5
        route.StopIfStuck = True
        result = PathFinding.Go(route)
        Misc.SendMessage("Go result is {}".format(result))
    orig_x = Player.Position.X
    orig_y = Player.Position.Y    
    for i in range(0, 8):
        Player.Walk(Player.Direction)
    if orig_x == Player.Position.X and orig_y == Player.Position.Y:
        stop = True
    
