# Parametri
LogBag = 0x408605E4 # Serial of log bag
OtherResourceBag = 0x401F5898 # Serial of other resource bag
SerialAccetta = 0x408605ED # Serial Axe
ScanRange = 15
RuneBookBanca = 0x404C8545 # Runebook for casa
PosizioneRunaCasa = 14
RuneBookAlberi = 0x402ABA35 # Runebook for tree spots
###########

# Variabili Sistema
WeightLimit = Player.MaxWeight - 80
TreeStaticID = [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274, 3275, 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3365, 3367, 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486, 3488, 3490, 3492, 3496]
EquipAccettaDelay = 2000
TimeoutOnWaitAction = 4000
ChopDelay = 1000
RecallPause = 4000 
DragDelay = 1200
LogID = 0x1BDD
BoardsID = 0x1BD7
OtherResourceID = [12687, 12697, 12127, 12688, 12689]

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
PosizioneRunaCasa=PosizioneRunaCasa * 6 - 1
lastSpot = 0
    

##################
dolog = 1
def dbg(s):
    if dolog:
        Misc.SendMessage(s, 4095)

def go(x1, y1):
    Coords = PathFinding.Route() 
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = 3
    PathFinding.Go(Coords)


def checkPositionChanged(posX, posY, noise=False):
    dbg("checkPositionChanged")
    recallStatus = "Life Sucks"
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

        else:
            recallStatus = "good"
    else:
        recallStatus = "good"

    Journal.Clear()
    dbg("checkPositionChanged: return: " + recallStatus)
    return recallStatus
        

def recall(bookSerial, bookIndex):
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
    while retry < 5:
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
    rv = doRecall(RuneBookBanca, PosizioneRunaCasa)
    dbg("gotoBank, recall = " + str(rv))
    if rv == "good":
        dbg("gotoBank, we're good")
        Player.ChatSay(4095, "bank")
    else:
        dbg("gotoBank, recall failed: " + str(rv))
        Misc.Pause(2000)

def RecallNextSpot():
    global lastrune
    dbg("RecallNextSpot")
    Gumps.ResetGump()
    Misc.SendMessage("--> Recall to Spot", 4095) 
    doRecall(RuneBookAlberi, lastrune)
    Misc.Pause(RecallPause)
    lastrune = lastrune + 6
    if lastrune > 95:
        lastrune = 5 
    if lastrune < 6:
            Misc.SendMessage("--> Initialize New Cycle", 4095) 
            lastrune = 5       
    EquipAxe()
    
####################    

def BankWood():
    dbg("BankWood")
    gotoBank()
    Journal.Clear()
    for item in Player.Backpack.Contains:
        dbg("BankWood: Backpack Loop")
        Misc.Pause(1500)
        if item.ItemID == LogID:
            dbg("BankWood: Logs")
            CutLogsToBoards()
            Misc.Pause(2000)
        elif item.ItemID == BoardsID:
            dbg("BankWood: Boards")
            Items.Move(item, LogBag, 0)
            Misc.Pause(DragDelay)
        elif item.ItemID in OtherResourceID:
            dbg("BankWood: other resources")
            Items.Move(item, LogBag, 0)
            Misc.Pause(DragDelay)


####################

def CutLogsToBoards():
    dbg("CutLogsToBoards")
    EquipAxe()
    for item in Player.Backpack.Contains:
        if item.ItemID == LogID:
            dbg("CutLogsToBoards: Log found")
            Items.UseItem(SerialAccetta)
            Target.WaitForTarget(2000, False)
            Target.TargetExecute(item)
            Misc.Pause(2000)
    Misc.Pause(2000)
            
#################### 

def EquipAxe():
    dbg("EquipAxe")
    if not Player.CheckLayer("RightHand"):
        Player.EquipItem(SerialAccetta)
        Misc.Pause(EquipAccettaDelay)      
   
####################  

def ScanStatic(): 
    global treenumber
    Misc.SendMessage("--> Init Tile Scan", 4095)
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
    Misc.SendMessage('--> Total Trees: %i' % (treenumber), 4095)

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
        return False
       
####################
    
def MoveToTree(spotnumber):
    dbg("MoveToTree")
    if spotnumber > len(treeposx):
        dbg("MoveToTree: spotnumber bad")
        return
    pathlock = 0
    Misc.SendMessage('--> Moving to TreeSpot: %i' % (spotnumber), 4095)
    Player.PathFindTo(treeposx[spotnumber], treeposy[spotnumber], treeposz[spotnumber])
    while not RangeTree(spotnumber):
        CheckEnemy()  
        Misc.Pause(30)
        pathlock = pathlock + 1
        if pathlock > 350:
            Player.PathFindTo(treeposx[spotnumber], treeposy[spotnumber], treeposz[spotnumber])  
            pathlock = 0
        
    Misc.SendMessage('--> Reached TreeSpot: %i' % (spotnumber), 4095)

####################  
def overWeight():
    global lastrune
    global lastSpot
    if (Player.Weight >= WeightLimit):
        CutLogsToBoards()
        Misc.Pause(1500)
        if (Player.Weight >= WeightLimit):
            BankWood()
            Misc.Pause(1500)
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
    lastSpot = spotnumber
    if Target.HasTarget():
        Misc.SendMessage("--> Extraneous Target Cancelled", 4095)
        Target.Cancel()
        Misc.Pause(500)
    
    CheckEnemy()    
    Journal.Clear()
    accetta = Items.FindBySerial(SerialAccetta)
    Items.UseItem(accetta)
    Target.WaitForTarget(TimeoutOnWaitAction)
    Target.TargetExecute(treeposx[spotnumber], treeposy[spotnumber], treeposz[spotnumber], treegfx[spotnumber])
    Misc.Pause(ChopDelay)
    if Journal.Search("There's not enough"):
        Misc.SendMessage("--> Go to next tree", 4095)
    elif Journal.Search("That is too far away"):
        blockcount = blockcount + 1
        Journal.Clear()
        if (blockcount > 15):
            blockcount = 0
            Misc.SendMessage("--> Blocked", 4095)
        else:
            CutTree(spotnumber)
    else:
        CutTree(spotnumber)

####################
        
def CheckEnemy():
    if (Player.Hits < Player.HitsMax):
        Misc.SendMessage("--> WARNING: Enemy Around!",4095)
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
            Misc.SendMessage("--> WARNING: Enemy Detected!", 4095) 
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

Misc.SendMessage("--> Starting Lumberjack", 4095)
while onloop:
    overWeight()
    RecallNextSpot()
    ScanStatic()
    i = 0
    while i < treenumber:
        MoveToTree(i)
        CutTree(i)
        i = i + 1
    treeposx = []
    treeposy = []
    treeposz = []
    treegfx = []
    treenumber = 0
