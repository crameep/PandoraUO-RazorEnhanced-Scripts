from System.Collections.Generic import List

#rail mining script by Mourn 8182 discord contact
#have a fire beetle and walk by mineable cliffs or caves , if necessary add ids on lines 4-5

mineableTiles = [0x0246, 0x0245,0x0248,0x0247, 0x0249, 0x023B, 0x0233, 0x023A,0x022C,0x023C,0x022D,0x022E,0x022F,0x00E4,0x00E6,0x00E5,0x00DC,0x00DE,0x00DD]#map art
mineableStatics = [0x053E,0x053B,0x0540,0x0541,0x0542,0x0543,0x0544,0x0555,0x0546,0x0547,0x0548,0x0549]#statics like cave tiles

# rune one in atlas bank, rune 2 in atlas near pathcoords first coordinate
# must have tinker tool and ingots at start
global pathCoords
global count
count = 1

global runenumber
runenumber = 0

miningCoords = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1],[-2,-2],[-2,2],[2,-2],[2,2]]
global stoCont
bankList =[0x1BF2]
oreIDs = [0x19B7,0x19B8,0x19B9,0x19BA]
beetleID = List[int]((0x00A9,0x00A9))
toolID = 0x0E86
fil = Mobiles.Filter()
fil.Enabled = True
fil.RangeMax = 25
fil.Bodies = beetleID
stoCont = 0x42F664B5

def go(x1, y1):
    Coords = PathFinding.Route()
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = 10
    PathFinding.Go(Coords)
    Misc.Pause(400)

def recall(runenumber):
    if Player.BuffsExist("Animal Form"):
        Spells.CastNinjitsu("Animal Form")
        Misc.Pause(3000)
    Misc.Pause(1000)
    newrunenumber = 49999 + runenumber
    Items.UseItemByID(0x9C16)
    Misc.Pause(1000)
    Gumps.WaitForGump(498, 3000)
    Gumps.SendAction(498, newrunenumber)
    Gumps.WaitForGump(498, 3000)
    Gumps.SendAction(498, 4000)
    newrunenumber = 0
    Misc.Pause(3000)
    if Journal.Search('fizzles.') == True or Journal.Search('reagents') == True:
        Journal.Clear()
        Misc.Pause(1000)
        recall(runenumber)

def checkTinkerTool():
    while Items.BackpackCount(0x1EB9, -1) < 2:
        Player.HeadMessage(45,"Making Tinker Tools")
        Items.UseItemByID(0x1EB9, -1)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 11)
        Misc.Pause(2000)

def checkPickaxe():
    if Items.BackpackCount(0x0E86, -1) == 0:
        x = 0
    if Items.BackpackCount(0x0E86, -1) > 0:
        x = Items.BackpackCount(0x0E86,-1)/58
    while x < 2:
        Player.HeadMessage(45,"Making Pickaxe")
        Items.UseItemByID(0x1EB9, -1)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 24)
        Misc.Pause(2000)
        if Items.BackpackCount(0x0E86, -1) > 0:
            x = Items.BackpackCount(0x0E86,-1)/58

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
                Misc.SendMessage('in a cave')
                id = static.StaticID
                mineTile(x1,y1,Player.Position.Z)
    if not statics:
        if tile in mineableTiles:
            mineTile(x1,y1,z1)

def mineTile(x,y,z):
    while Items.BackpackCount(toolID) > 0:
        if Journal.Search('metal') or Journal.Search('see'):
            Journal.Clear()
            break
        Items.UseItemByID(toolID)
        Target.WaitForTarget(1000,False)
        Target.TargetExecute(x,y,z)
        Misc.Pause(1000)
        if Player.Weight > Player.MaxWeight -45:
            smelt()

def niter():
    nfil = Items.Filter()
    nfil.RangeMax = 3
    nfil.OnGround = True
    nfil.Enabled = True
    nfil.Movable = True
    nlist = List[int]((0x1362, 0x1363, 0x1364, 0x1367, 0x1369))
    nfil.Graphics = nlist
    niters = Items.ApplyFilter(nfil)
    Misc.Pause(500)
    while niters:
        checkTinkerTool()
        checkPickaxe()
        niter = Items.Select(niters,'Nearest')
        Items.UseItemByID(toolID)
        Target.WaitForTarget(1000,False)
        Target.TargetExecute(niter)
        Misc.Pause(500)
        niters = Items.ApplyFilter(nfil)
        Misc.Pause(500)

def smelt():
    beetles = Mobiles.ApplyFilter(fil)
    beetle = Mobiles.Select(beetles,'Nearest')
    if Player.InRangeMobile(beetle,2):
        for item in Player.Backpack.Contains:
            if item.ItemID in oreIDs:
                Items.UseItem(item)
                Target.WaitForTarget(1000,False)
                Target.TargetExecute(beetle)
                Misc.Pause(1000)
def dump():
    beetles = Mobiles.ApplyFilter(fil)
    beetle = Mobiles.Select(beetles,'Nearest')
    Player.ChatSay(30,'all follow me')
    while Player.InRangeMobile(beetle,2) == False:
        Misc.Pause(2000)

    while Player.Mount == None:
        Mobiles.UseMobile(beetle)
        Misc.Pause(1500)
    recall(1)
    Player.ChatSay(30,'bank')
    for item in Player.Backpack.Contains:
        if item.ItemID in bankList:
           Items.Move(item,Player.Bank,0)
           Misc.Pause(1500)
           restock = Items.FindByID(0x1BF2,0x0000,Player.Bank.Serial)
    Items.Move(restock,Player.Backpack,50)
    Misc.Pause(1100)

def unload():
    Misc.Pause(1100)
    Organizer.ChangeList("ore")
    Misc.Pause(300)
    Organizer.FStart()
    Misc.Pause(5000)

def getingot():
   # while Items.BackpackCount(0x1BD7,0x0000) > 0:
    ingot = Items.FindByID(0x1BF2,0x0000,stoCont)
    Misc.Pause(500)
    Items.WaitForContents(stoCont,2000)
    Misc.Pause(1100)
    Items.Move(ingot, Player.Backpack.Serial, 50)
    Misc.Pause(500)

def mineLocation(rune):
    getingot()
    Misc.Pause(300)
    
    if rune > 4:  #set to num of last rune rail
        rune = 3  # resets
        
    if rune == 3:
        path = [[2334, 827], [2335, 822], [2330, 822], [2324, 826], [2319, 827], [2316, 816], [2321, 814], [2328, 816], [2330, 820], [2332, 824]]
    if rune == 4 :
        path = [[2347, 807], [2351, 799], [2354, 802], [2359, 803], [2362, 806], [2362, 811], [2363, 816], [2369, 816], [2372, 819], [2370, 825], [2364, 827], [2360, 825], [2359, 820], [2358, 814], [2358, 810], [2352, 807]]
    
    recall(rune)
   
    if Player.Mount:
        Mobiles.UseMobile(Player.Serial)
        for pcoords in path:
            go(pcoords[0],pcoords[1])
            checkTinkerTool()
            checkPickaxe()
            if Items.BackpackCount(0x1BF2,-1) > 1500:
                #dump()
                recall(1)
                unload()
                Main()
            for mcoords in miningCoords:
                checkTile(mcoords[0],mcoords[1])
            niter()
            Misc.Pause(200)
        beetles = Mobiles.ApplyFilter(fil)
        beetle = Mobiles.Select(beetles,'Nearest')
        Player.ChatSay(30,'all follow me')
        while Player.InRangeMobile(beetle,2) == False:
            Misc.Pause(2000)

        while Player.Mount == None:
            Mobiles.UseMobile(beetle)
            Misc.Pause(1500)
        recall(1)
        Misc.Pause(400)
        unload()
        if Player.Mount:
           Mobiles.UseMobile(Player.Serial)
           smelt()
        rune +=1
        mineLocation(rune)

mineLocation(3)