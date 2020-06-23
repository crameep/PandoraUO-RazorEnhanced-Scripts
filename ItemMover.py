#Item Mover
#Chose Item
#Chose Source Container
#Chose Destination Container


from System.Collections.Generic import List


startX = 0
startY = 0
verticalIncrement = 0
horizontalIncrement = 10
endX = 0
endY = 0
moveDelay = 1200
ignoreItems = [0x100E]


def Pick(text, multiple=True):
   itemList = []
   if multiple: 
       while multiple:
           Misc.SendMessage(text, 76)
           chosenid = Target.PromptTarget()
           if chosenid > -1:
               chosen = Items.FindBySerial(chosenid)
               Misc.Pause(500)
               Misc.SendMessage("Chose {}".format(chosen.Name))
               itemList.append(chosen.ItemID)
           else:
               multiple = False
               if len(itemList) == 1:
                   Misc.SendMessage("Returning {}".format(chosen.Name))
                   return chosen
               else:
                   return itemList
   else:
       Misc.SendMessage(text, 76)
       chosenid = Target.PromptTarget()
       if chosenid > -1:
           chosen = Items.FindBySerial(chosenid)
           Misc.Pause(500)
           Misc.SendMessage("Chose {}".format(chosen.Name))
           return chosen
       
        
def find(containerSerial, typeArray):
    if type(typeArray) is not list:
       item = typeArray
       typeArray = [item.ItemID]
       
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
    global verticalIncrement
    global horizontalIncrement
    
    if "backpack" in container.Name:
        Misc.SendMessage("Setting size to Backpack or a Pouch")
        startX = 45
        startY = 75
        endX = 160
        endY = 150
        verticalIncrement = 20
    elif "pouch" in container.Name:
        Misc.SendMessage("Setting size to Pouch")
        startX = 45
        startY = 75
        endX = 160
        endY = 150
        verticalIncrement = 20
    elif "bag" in container.Name:
        Misc.SendMessage("Setting size to Bag")
        startX = 30
        startY = 40
        endX = 115
        endY = 120
        verticalIncrement = 20
    elif "ornate" in container.Name:
        Misc.SendMessage("Setting size to Box")
        startX = 15
        startY = 50
        endX = 155
        endY = 120
        verticalIncrement = 20
    elif "wooden box" in container.Name:
        Misc.SendMessage("Setting size to Box")
        startX = 15
        startY = 50
        endX = 155
        endY = 120
        verticalIncrement = 20
    elif "metal chest" in container.Name:
        Misc.SendMessage("Setting size to Metal Chest")
        startX = 20
        startY = 105
        endX = 135
        endY = 150
        verticalIncrement = 10
    else:
        Misc.SendMessage("Setting size to Unknown")
        startX = 50
        startY = 50
        endX = 115
        endY = 120
        verticalIncrement = 20


itemsToMove = Pick("Select the Item you want to move")
sourceCont = Pick("Select the source container", False)
destCont = Pick("Select the destination container", False)


if sourceCont == None:
    sourceCont = Items.FindBySerial(itemsToMove.Container) 
        
if not itemsToMove:
    Misc.SendMessage("You didn't Pick an Item to move so I will move all items in the source.", 222)
    items = itemsToMove = sourceCont.Contains
    items = list(dict.fromkeys(items))
    horizontalIncrement = 15
else:
    items = find(sourceCont.Serial, itemsToMove)

    
getSize(destCont)

x = startX
y = startY
Misc.SendMessage(len(items))
for item in items:
    if item.ItemID not in ignoreItems:
        #Misc.SendMessage("{},{}".format(x,y))
        if x > endX:
            x = startX
            y = y + verticalIncrement
        if y >= endY:
           break 
           
        Items.Move(item, destCont, 0, x, y)
        Misc.Pause(moveDelay)
        x = x + horizontalIncrement
