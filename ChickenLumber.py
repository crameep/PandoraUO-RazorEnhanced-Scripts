# SETUP
LogBag = 0x413985E1 # Serial of log bag
OtherResourceBag = 0x401F5898 # Serial of other resource bag
SerialAxe = 0x4050B751 # Serial Axe
ScanRange = 15
RuneBookBank = 0x404C8545 # Runebook for Bank
BankRunePosition = 14
RuneBookTrees = 0x402ABA35 # Runebook for tree spots
MasterRuneBook = True
MRBSerial = 0x40F8B116
MRBLogBook = 18 
MRBBankBook = 1  
MRBBankSpot = 1
MBRRuneSlots = 4
UseStorageBox = True  #### Set Log Bag to Resource Storage Box
NoBank = True ## Use Bank Stone Instead of Banking
BankStoneSerial = 0x402AAAF6

###########

# Variables
WeightLimit = Player.MaxWeight - 80
TreeStaticID = [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274, 3275, 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3365, 3367, 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486, 3488, 3490, 3492, 3496]
EquipaxeDelay = 2000
TimeoutOnWaitAction = 4000
ChopDelay = 1500
RecallPause = 4000 
DragDelay = 1200
LogID = 0x1BDD
BoardsID = 0x1BD7
BankResourceID = [ 0x1BD7,12687, 12697, 12127, 12688, 12689]

"""   ^^^
Bark Fragment   12687
Brilliant Amber 12697
Luminescent Fungi   12689
Parasitic Plant 12688
Switch Item 12127
"""

noLrc = ("More reagents are needed for this spell")
noMana = ("Insufficient mana for this spell")
from System.Collections.Generic import List
tileinfo = List[Statics.TileInfo]
treeposx = []
treeposy = []
treeposz = []
treegfx = []
treenumber = 0
blockcount = 0
lastrune = 5
onloop = True
BankRunePosition=BankRunePosition * 6 - 1
lastSpot = 0

if MasterRuneBook:
    lastrune = 1
    

##################
dolog = 1
def dbg(s):
    if dolog:
        Misc.SendMessage(s, 2222)

def go(x1, y1):
    Coords = PathFinding.Route() 
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = 3
    PathFinding.Go(Coords)
    
def checkPositionChanged(posX, posY, noise=False):
    dbg("checkPositionChanged")
    recallStatus = "Life Sucks"
    unchanged = True
    if Player.Position.X == posX and Player.Position.Y == posY:
        dbg("checkPositionChanged: Position Unchanged")
        if Journal.Search("blocked"):
            Journal.Clear()
            if noise:
                Misc.SendMessage("Rune Blocked", 4095)
            recallStatus = "blocked"

        elif Journal.Search("mana"):
            Journal.Clear()
            if noise:
                Misc.SendMessage("out of mana", 4095)
            recallStatus = "mana"

        elif Journal.Search("More reagents are needed"):
            Journal.Clear()
            if noise:
                Misc.SendMessage("out of mana", 4095)
            recallStatus = "regs"

        elif Journal.Search("Thou art too encumbered"):
            Journal.Clear()
            if noise:
                Misc.SendMessage("Overweight", 4095)
            recallStatus = "weight"
            BankWood()

        elif unchanged:
            recallStatus = "unchanged"
        else:
            recallStatus = "good"
    else:
        recallStatus = "good"

    Journal.Clear()
    dbg("checkPositionChanged: return: " + recallStatus)
    return recallStatus
 
 ### Corys Adds
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
        Misc.SendMessage("Spell should be one of R, G or S, quitting", 2222)
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
##### End Corys Add
        

def recall(bookSerial, bookIndex):
    if MasterRuneBook:
        MasterBook(MRBSerial, MRBLogBook, bookIndex, "R")
    else:
        Items.UseItem(bookSerial)
        Gumps.WaitForGump(1431013363, 2000)
        Gumps.SendAction(1431013363, bookIndex)
        Misc.Pause(RecallPause)


def doRecall(bookSerial, bookIndex):
    currentX = Player.Position.X
    currentY = Player.Position.Y
    retry = 0
    rv = ""
    dbg("doRecall")
    dbg("doRecall rune: " + str(bookIndex))
    while retry < 2:
        dbg("doRecall, retry = " + str(retry))
        recall(bookSerial, bookIndex)
        rv = checkPositionChanged(currentX, currentY, True)
        if rv == "good":
            break
        else:
            retry += 1


# recall via runebook to the insula bank
def gotoBank():
    dbg("gotoBank")
    x = Player.Position.X
    y = Player.Position.Y
    rv = doRecall(RuneBookBanca, BankRunePosition)
    dbg("gotoBank, recall = " + str(rv))
    if rv == "good":
        dbg("gotoBank, we're good")
        Player.ChatSay(2222, "bank")
    else:
        dbg("gotoBank, recall failed: " + str(rv))
        Misc.Pause(2000)

def RecallNextSpot():
    global lastrune
    dbg("RecallNextSpot")
    Gumps.ResetGump()
    Misc.SendMessage("--> Recall to Spot", 2222) 
    doRecall(RuneBookTrees, lastrune)
    Misc.Pause(RecallPause)
    if MasterRuneBook:
        lastrune = lastrune + 1
        if lastrune >= MBRRuneSlots:
           Misc.SendMessage("--> Initialize New Cycle", 2222)      
           lastrune = 1
    else:
        lastrune = lastrune + 6
        if lastrune > 95:
            lastrune = 5 
        if lastrune < 6:
                Misc.SendMessage("--> Initialize New Cycle", 2222) 
                lastrune = 5       
    EquipAxe()
    
#################### 


def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:
            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list   

def BankWood():
    attempt = 0
    dbg("BankWood")
    if NoBank:
        Items.UseItem(BankStoneSerial)
        Misc.Pause(1000)
    else:
        gotoBank()
    Journal.Clear()
    CutLogsToBoards()
    
    
    lst = find(Player.Backpack.Serial, BankResourceID)
    for itm in lst:
        Misc.SendMessage(itm.Serial)
        Items.Move(itm, 0x413985E1, 0)
        Misc.SendMessage(itm.Name)
        Misc.Pause(2000)
    
    


####################

def CutLogsToBoards():
    dbg("CutLogsToBoards")
    EquipAxe()
    while Items.FindByID(LogID, -1, Player.Backpack.Serial) != None:
        log = Items.FindByID(LogID, -1, Player.Backpack.Serial)
        dbg("CutLogsToBoards: Log found")
        Items.UseItem(SerialAxe)
        Target.WaitForTarget(2000, False)
        Target.TargetExecute(log)
        Misc.Pause(2000)

            
#################### 

def EquipAxe():
    dbg("EquipAxe")
    if not Player.CheckLayer("RightHand"):
        Player.EquipItem(SerialAxe)
        Misc.Pause(EquipaxeDelay)      
   
####################  

def ScanStatic(): 
    global treenumber
    Misc.SendMessage("--> Init Tile Scan", 2222)
    minx = Player.Position.X - ScanRange
    maxx = Player.Position.X + ScanRange
    miny = Player.Position.Y - ScanRange
    maxy = Player.Position.Y + ScanRange

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
        minx = Player.Position.X - ScanRange            
        miny = miny + 1
    treenumber = treeposx.Count    
    Misc.SendMessage('--> Total Trees: %i' % (treenumber), 2222)

####################
       
def RangeTree(spotnumber):
    
    if (Player.Position.X - 1) == treeposx[spotnumber] and (Player.Position.Y + 1) == treeposy[spotnumber]:
        return True
    elif (Player.Position.X - 1) == treeposx[spotnumber] and (Player.Position.Y - 1) == treeposy[spotnumber]:
        return True
    elif (Player.Position.X + 1) == treeposx[spotnumber] and (Player.Position.Y + 1) == treeposy[spotnumber]:
        return True
    elif (Player.Position.X + 1) == treeposx[spotnumber] and (Player.Position.Y - 1) == treeposy[spotnumber]:
        return True
    elif Player.Position.X == treeposx[spotnumber] and (Player.Position.Y - 1) == treeposy[spotnumber]:
        return True    
    elif Player.Position.X == treeposx[spotnumber] and (Player.Position.Y + 1) == treeposy[spotnumber]:   
        return True     
    elif Player.Position.Y == treeposy[spotnumber] and (Player.Position.X - 1) == treeposx[spotnumber]:
        return True    
    elif Player.Position.Y == treeposy[spotnumber] and (Player.Position.X + 1) == treeposx[spotnumber]:   
        return True    
    else:
       # Misc.SendMessage("TreePos: {},{} PlayerPos: {},{}".format(treeposx[spotnumber],treeposy[spotnumber],Player.Position.X, Player.Position.Y))
        return False
        
def GetRangeOffset(spotnumber):

    if treeposx[spotnumber] != None:
        PX = Player.Position.X
        PY = Player.Position.Y
        PZ = Player.Position.Z
        
        OX = treeposx[spotnumber] - PX
        OY = treeposy[spotnumber] - PY
        OZ = treeposz[spotnumber] - PZ
        
        return (OX,OY,OZ)
    else:
        return None
       
####################
    
def MoveToTree(spotnumber):
    dbg("MoveToTree")
    if spotnumber > len(treeposx):
        dbg("MoveToTree: spotnumber bad")
        return
    pathlock = 0
    Misc.SendMessage('--> Moving to TreeSpot: {}'.format(spotnumber), 222)
    offset = GetRangeOffset(spotnumber)
    Player.PathFindTo(Player.Position.X + offset[0], Player.Position.Y + offset[1] + 1, Player.Position.Z + offset[2])
    Misc.Pause(1000)
    Misc.SendMessage("{} {} {}".format(offset[0], offset[1], offset[2]), 222)
    while not RangeTree(spotnumber):
        #Misc.SendMessage("Ranging Tree")
        CheckEnemy()  
        Misc.Pause(30)
        pathlock = pathlock + 1
        if pathlock > 350:
            Misc.SendMessage("Pathlocked Trying Again: {}".format(pathlock))
            Misc.SendMessage("{} {} {}".format(Player.Position.X + offset[0], Player.Position.Y + offset[1], Player.Position.Z + offset[2]), 222)
            #Player.PathFindTo(1187,561,-88) 
            offset = GetRangeOffset(spotnumber)
            newoffsety = offset[1] - 1
            newoffsetx = offset[0] + 1
            Player.PathFindTo(Player.Position.X + newoffsetx, Player.Position.Y + newoffsety + 1, Player.Position.Z + offset[2])
            #go(Player.Position.X + newoffsetx, Player.Position.Y + newoffsety + 1)
            Misc.Pause(30)
        if pathlock > 500:
            Misc.SendMessage("Disconecting....")
            Misc.Disconnect()
            pathlock = 0
        
    Misc.SendMessage('--> Reached TreeSpot: %i' % (spotnumber), 2222)

####################  
def overWeight():
    Misc.SendMessage("Overweight Check")
    global lastrune
    global lastSpot
    if (Player.Weight >= WeightLimit):
        CutLogsToBoards()
        Misc.Pause(1500)
        if (Player.Weight >= WeightLimit):
            BankWood()
            Misc.Pause(1500)
            if MasterRuneBook:
                lastrune = 0 
            else:
                lastrune = lastrune - 6
                if lastrune < 5:
                    lastrune = 5
            RecallNextSpot()
            MoveToTree(lastSpot)

def CutTree(spotnumber):
    dbg("CutTree")
    
    global lastSpot
    global blockcount
    global lastrune
    global cutcount
    cutcount = 0
    if (Player.Weight >= WeightLimit):
        Misc.SendMessage("Overweight While Cutting")
        CutLogsToBoards()
        BankWood()
    
    lastSpot = spotnumber

    if Target.HasTarget():
        Misc.SendMessage("--> Extraneous Target Cancelled", 2222)
        Target.Cancel()
        Misc.Pause(500)

    CheckEnemy()    
    Journal.Clear()
    axe = Items.FindBySerial(SerialAxe)
    Items.UseItem(axe)
    Target.WaitForTarget(TimeoutOnWaitAction)
    Target.TargetExecute(treeposx[spotnumber], treeposy[spotnumber], treeposz[spotnumber], treegfx[spotnumber])
    Misc.Pause(ChopDelay)
    if Journal.Search("There's not enough"):
        Misc.SendMessage("--> Go to next tree", 2222)
        cutcount = 0
    elif Journal.Search("cannot be seen"):
            Journal.Clear()
            dbg("Cant find tree moving to next one")
            cutcount = 0
    elif Journal.Search("That is too far away"):
        blockcount = blockcount + 1
        Journal.Clear()
        if (blockcount > 15):
            blockcount = 0
            Misc.SendMessage("--> Blocked", 2222)
        else:
            CutTree(spotnumber)
            cutcount = cutcount + 1
    else:
        CutTree(spotnumber)
        cutcount = cutcount + 1

####################
        
def CheckEnemy():
    if (Player.Hits < Player.HitsMax):
        Misc.SendMessage("--> WARNING: Enemy Around!",2222)
        Misc.Beep()
        
        fil = Mobiles.Filter()
        fil.Enabled = True
        fil.RangeMax = 2
        enemyfound = 0
        enemys = Mobiles.ApplyFilter(fil)
        
        for enemy in enemys:
            if enemy.Notoriety == 3:
                enemyfound = enemy.Serial
                
        if enemyfound != 0:
            enemymobile = Mobiles.FindBySerial(enemyfound)
            Misc.SendMessage("--> WARNING: Enemy Detected!", 2222) 
            Spells.CastMagery("Poison")
            Target.WaitForTarget(1000)
            Target.TargetExecute(enemymobile)
            Misc.Pause(900)
            while enemymobile:
                Spells.CastMagery("Harm")
                Target.WaitForTarget(1000)
                Target.TargetExecute(enemymobile)
                Misc.Pause(900)
                enemymobile = Mobiles.FindBySerial(enemyfound)
                
        while Player.Hits < Player.HitsMax:
            Spells.CastMagery("Heal")
            Target.WaitForTarget(1000)
            Target.Self()
            Misc.Pause(900)    

        EquipAxe()     
        
    else:
        return;
        
####################

Misc.SendMessage("--> Starting Lumberjack", 2222)
while onloop:
    overWeight()
    RecallNextSpot()
    ScanStatic()    
    i = 0
    while i < treenumber:
        MoveToTree(i)
        CutTree(i)
        overWeight()
        i = i + 1
    treeposx = []
    treeposy = []
    treeposz = []
    treegfx = []
    treenumber = 0
