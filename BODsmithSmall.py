from System.Collections.Generic import List 

Misc.SendMessage('Target Resource Container',78)
resourceCont = Target.PromptTarget(' ')
Misc.SendMessage('Target Book of Empty Deeds',78)
toEmpty = Target.PromptTarget(' ')
Misc.SendMessage('Target Book to put Full Deeds',78)
toFill = Target.PromptTarget(' ')
tinkerTool = Items.FindByID(0x1EB9,-1,Player.Backpack.Serial)
Items.UseItem(resourceCont)
Misc.Pause(1100)

def checkIngots(type):
    if Items.BackpackCount(0x1BF2,0x0000) < 50:
        Items.WaitForContents(resourceCont,2000)
        Misc.Pause(1500)
        ironIngots = Items.FindByID(0x1BF2,0x0000,resourceCont)
        Items.Move(ironIngots,Player.Backpack,250)
    if str(type) == 'dull':
        if Items.BackpackCount(0x1BF2,0x0973) < 50:
            Items.WaitForContents(resourceCont,2000)
            Misc.Pause(1500)
            dullIngots = Items.FindByID(0x1BF2,0x0973,resourceCont)
            Items.Move(dullIngots,Player.Backpack,250)        
    if str(type) == 'shadow':
        if Items.BackpackCount(0x1BF2,0x0966) < 50:
            Items.WaitForContents(resourceCont,2000)
            Misc.Pause(1500)
            shadowIngots = Items.FindByID(0x1BF2,0x0966,resourceCont)
            Items.Move(shadowIngots,Player.Backpack,250)   
    if str(type) == 'copper':
        if Items.BackpackCount(0x1BF2,0x096D) < 50:
            Items.WaitForContents(resourceCont,2000)
            Misc.Pause(1500)
            copperIngots = Items.FindByID(0x1BF2,0x096D,resourceCont)
            Items.Move(copperIngots,Player.Backpack,250)   
    if str(type) == 'bronze':
        if Items.BackpackCount(0x1BF2,0x0972) < 50:
            Items.WaitForContents(resourceCont,2000)
            Misc.Pause(1500)
            bronzeIngots = Items.FindByID(0x1BF2,0x0972,resourceCont)
            Items.Move(bronzeIngots,Player.Backpack,250)   
    if str(type) == 'gold':
        if Items.BackpackCount(0x1BF2,0x08A5) < 50:
            Items.WaitForContents(resourceCont,2000)
            Misc.Pause(1500)
            goldIngots = Items.FindByID(0x1BF2,0x08A5,resourceCont)
            Items.Move(goldIngots,Player.Backpack,250)   
    if str(type) == 'agapite':
        if Items.BackpackCount(0x1BF2,0x0979) < 50:
            Items.WaitForContents(resourceCont,2000)
            Misc.Pause(1500)
            agapiteIngots = Items.FindByID(0x1BF2,0x0979,resourceCont)
            Items.Move(agapiteIngots,Player.Backpack,250)   
    if str(type) == 'verite':
        if Items.BackpackCount(0x1BF2,0x089F) < 50:
            Items.WaitForContents(resourceCont,2000)
            Misc.Pause(1500)
            veriteIngots = Items.FindByID(0x1BF2,0x089F,resourceCont)
            Items.Move(veriteIngots,Player.Backpack,250)   
    if str(type) == 'valorite':
        if Items.BackpackCount(0x1BF2,0x08AB) < 50:
            Items.WaitForContents(resourceCont,2000)
            Misc.Pause(1500)
            valoriteIngots = Items.FindByID(0x1BF2,0x08AB,resourceCont)
            Items.Move(valoriteIngots,Player.Backpack,250)   
    Misc.Pause(1000)
    
def checkTongs():
    b = Items.BackpackCount(0x1EB9,-1)
    while b < 3:
        Items.UseItem(tinkerTool)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 5000)        
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 11)
        Misc.Pause(2000)
        b = Items.BackpackCount(0x1EB9,-1)
    a = Items.BackpackCount(0x0FBC,-1)
    while a < 3:
        Items.UseItem(tinkerTool)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 5000)        
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 20)
        Misc.Pause(2000)
        a = Items.BackpackCount(0x0FBC,-1)
        
def evalBod():
    global bod
    Items.UseItem(toEmpty)
    Gumps.WaitForGump(668, 10000)
    Gumps.SendAction(668, 4)
    Misc.Pause(1000)
    bod = Items.FindByID(0x2258,0x044E,Player.Backpack.Serial)
    Misc.Pause(400)
    bodList = Items.GetPropStringList(bod)
    Misc.Pause(400)

    metalTypes = bodList[4].split(' ')
    metalType = metalTypes[0]
    
    itemMakesss = bodList[7].split(':')
    itemMakess = itemMakesss[0]
    itemMakes = itemMakess.split(' ')
    itemMake = itemMakes[0]
    Misc.SendMessage(itemMake)
    if len(itemMakes) > 1:
        itemMake2 = itemMakes[1]
        Misc.SendMessage(itemMake2)        
    amountMakess = bodList[6].split(':')
    amountMakes = amountMakess[1].split(' ')
    amountMake = amountMakes[1]   
    Misc.SendMessage(amountMake)
    if str(metalType) == 'All':
        metalType = metalTypes[6]
    if str(metalType) == 'iron':
        ingotType = 5000
    Misc.SendMessage(metalType)
    
    if str(metalType) == 'dull':
        ingotType = 5001
    if str(metalType) == 'shadow':
        ingotType = 5002 
    if str(metalType) == 'copper':
        ingotType = 5003
    if str(metalType) == 'bronze':
        ingotType = 5004
    if str(metalType) == 'gold':
        ingotType = 5005    
    if str(metalType) == 'agapite':
        ingotType = 5006
    if str(metalType) == 'verite':
        ingotType = 5007
    if str(metalType) == 'valorite':
        ingotType = 5008 
        
    if str(itemMake) == 'tear':  # tear kite shield
        itemID = 0x1B78
        gumpNum = 38 
    if str(itemMake) == 'metal':
        if str(itemMake2) == 'kite':  # metal kite shield
            itemID = 0x1B74
            gumpNum = 37
        elif str(itemMake2) == 'shield':  # metal shield
            itemID = 0x1B7B
            gumpNum = 36
    if str(itemMake) == 'bronze':  
        itemID = 0x1B72
        gumpNum = 34    
    if str(itemMake) == 'heater':  
        itemID = 0x1B76
        gumpNum = 35    
    if str(itemMake) == 'buckler':  
        itemID = 0x1B73
        gumpNum = 33    
    if str(itemMake) == 'norse':  
        itemID = 0x140E
        gumpNum = 23    
    if str(itemMake) == 'helmet':  
        itemID = 0x140A
        gumpNum = 22    
    if str(itemMake) == 'close':  
        itemID = 0x1408
        gumpNum = 21    
    if str(itemMake) == 'bascinet':  
        itemID = 0x140C
        gumpNum = 20    
    if str(itemMake) == 'female':  
        itemID = 0x1C04
        gumpNum = 13   
    if str(itemMake) == 'halberd':  
        itemID = 0x143F
        gumpNum = 69    
    if str(itemMake) == 'bardiche':  
        itemID = 0x0F4D
        gumpNum = 66    
    if str(itemMake) == 'two':  
        itemID = 0x1443
        gumpNum = 64    
    if str(itemMake) == "executioner's":  # '
        itemID = 0x0F45
        gumpNum = 62    
    if str(itemMake) == 'large':  
        itemID = 0x13FB
        gumpNum = 63    
    if str(itemMake) == 'double':  
        itemID = 0x0F4B
        gumpNum = 61    
    if str(itemMake) == 'battle':  
        itemID = 0x0F47
        gumpNum = 60    
    if str(itemMake) == 'axe':  
        itemID = 0x0F49
        gumpNum = 59    
    if str(itemMake) == 'hammer':  
        itemID = 0x143D
        gumpNum = 76    
    if str(itemMake) == 'mace':  
        itemID = 0x0F5C
        gumpNum = 77    
    if str(itemMake) == 'maul':  
        itemID = 0x143B
        gumpNum = 78    
    if str(itemMake) == 'war':
        if str(itemMake2) == 'mace': 
            itemID = 0x1407
            gumpNum = 80 
        elif str(itemMake2) == 'hammer': 
            itemID = 0x1439
            gumpNum = 81 
        elif str(itemMake2) == 'axe': 
            itemID = 0x13B0
            gumpNum = 65 
        elif str(itemMake2) == 'fork': 
            itemID = 0x1405
            gumpNum = 75     
    if str(itemMake) == 'spear':  
        itemID = 0x0F62
        gumpNum = 74    
    if str(itemMake) == 'short':  
        itemID = 0x1403
        gumpNum = 72   
    if str(itemMake) == 'kryss':  
        itemID = 0x1401
        gumpNum = 47    
    if str(itemMake) == 'dagger':  
        itemID = 0x0F51
        gumpNum = 45    
    if str(itemMake) == 'viking':  
        itemID = 0x13B9
        gumpNum = 50    
    if str(itemMake) == 'scimitar':  
        itemID = 0x13B6
        gumpNum = 49    
    if str(itemMake) == 'longsword':  
        itemID = 0x0F61
        gumpNum = 48
    if str(itemMake) == 'katana':  
        itemID = 0x13FF
        gumpNum = 46 
    if str(itemMake) == 'cutlass':  
        itemID = 0x1441
        gumpNum = 44
    if str(itemMake) == 'broadsword':  
        itemID = 0x0F5E
        gumpNum = 42
    if str(itemMake) == 'plate':  
        itemID = 0x1412
        gumpNum = 24
    if str(itemMake) == 'platemail':  
        if str(itemMake2) == 'tunic':  
            itemID = 0x1415
            gumpNum = 12
        elif str(itemMake2) == 'legs':  
            itemID = 0x1411 
            gumpNum = 11
        elif str(itemMake2) == 'gorget':  
            itemID = 0x1413
            gumpNum = 10
        elif str(itemMake2) == 'gloves':  
            itemID = 0x1414
            gumpNum = 9
        elif str(itemMake2) == 'arms':  
            itemID = 0x1410
            gumpNum = 8
    if str(itemMake) == 'chainmail':  
        if str(itemMake2) == 'coif':  
            itemID = 0x13BB
            gumpNum = 5 
        elif str(itemMake2) == 'leggings':  
            itemID = 0x13BE
            gumpNum = 6
        elif str(itemMake2) == 'tunic':  
            itemID = 0x13BF
            gumpNum = 7 
    if str(itemMake) == 'ringmail':  
        if str(itemMake2) == 'gloves':  
            itemID = 0x13EB
            gumpNum = 1
        elif str(itemMake2) == 'leggings':  
            itemID = 0x13F0
            gumpNum = 2
        elif str(itemMake2) == 'sleeves':  
            itemID = 0x13EF
            gumpNum = 3    
        elif str(itemMake2) == 'tunic':  
            itemID = 0x13EC
            gumpNum = 4
    fillBOD(itemID, ingotType, metalType, gumpNum, amountMake)   
            
def fillBOD(itemID, ingotType, metalType, gumpNum, amountMake):
    counter = 0
    for itemCount in Player.Backpack.Contains:
        if itemCount.ItemID == itemID:
            counter += 1
    Misc.SendMessage(counter,54)
    Misc.SendMessage('/',54)    
    Misc.SendMessage(amountMake,54)
    while int(counter) < int(amountMake):
        counter = 0
        checkIngots(metalType)
        checkTongs()
        tongs = Items.FindByID(0x0FBC,-1,Player.Backpack.Serial)
        Items.UseItem(tongs)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, ingotType)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, gumpNum)
        Misc.Pause(1500)
        for itemCount in Player.Backpack.Contains:
            if itemCount.ItemID == itemID:
                counter += 1
        Misc.SendMessage(counter,54)
        Misc.SendMessage('/',54)    
        Misc.SendMessage(amountMake,54)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 0) 
    Misc.Pause(1000)
    Items.UseItem(bod)
    Gumps.WaitForGump(456, 10000)
    Gumps.SendAction(456, 11)
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(Player.Backpack)
    for items in Player.Backpack.Contains:
        if items.ItemID == 0x1BF2 and items.Hue != 0x0000:
            Items.Move(items,resourceCont,-1)
            Misc.Pause(1500)
    Misc.Pause(1500)
    Items.Move(bod.Serial,toFill,-1)
    Gumps.WaitForGump(668, 10000)
    Gumps.SendAction(668, 0)
    
while True:    
    evalBod()
    Misc.Pause(1000)