#Item Mover
#Chose Item
#Chose Source Container
#Chose Destination Container

startX = 0
startY = 0
increment = 0
endX = 0
endY = 0


def Pick(text): 
    Misc.SendMessage(text, 76)
    chosenid = Target.PromptTarget()
    if chosenid > -1:
        chosen = Items.FindBySerial(chosenid)
        Misc.Pause(500)
        Misc.SendMessage("Chose {}".format(chosen.Name))
        return chosen
        
def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:

            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list 
    
def getSize(container):
    global startX
    global startY
    global endX
    global endY
    global increment
    
    if "backpack" in container.Name:
        Misc.SendMessage("Setting size to Backpack or a Pouch")
        startX = 45
        startY = 75
        endX = 160
        endY = 150
        increment = 20
    elif "pouch" in container.Name:
        Misc.SendMessage("Setting size to Pouch")
        startX = 45
        startY = 75
        endX = 160
        endY = 150
        increment = 20
    elif "bag" in container.Name:
        Misc.SendMessage("Setting size to Bag")
        startX = 30
        startY = 40
        endX = 115
        endY = 120
        increment = 20
    elif "ornate" in container.Name:
        Misc.SendMessage("Setting size to Box")
        startX = 20
        startY = 40
        endX = 115
        endY = 120
        increment = 20
    elif "metal chest" in container.Name:
        Misc.SendMessage("Setting size to Metal Chest")
        startX = 20
        startY = 105
        endX = 135
        endY = 150
        increment = 10
    else:
        Misc.SendMessage("Setting size to Unknown")
        startX = 50
        startY = 50
        endX = 115
        endY = 120
        increment = 20


itemToMove = Pick("Select the Item you want to move")
sourceCont = Pick("Select the source container")
destCont = Pick("Select the destination container")


if sourceCont == None:
    sourceCont = Items.FindBySerial(itemToMove.Container)
    
items = find(sourceCont.Serial, [itemToMove.ItemID])

    
getSize(destCont)

x = startX
y = startY
Misc.SendMessage(items)
for item in items:
    Misc.SendMessage("{},{}".format(x,y))
    if x > endX:
        x = startX
        y = y + increment
    if y >= endY:
       break 
       
    Items.Move(item, destCont, 0, x, y)
    Misc.Pause(1200)
    x = x + 10
