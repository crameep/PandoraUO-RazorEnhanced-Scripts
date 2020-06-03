#Item Mover
#Chose Item
#Chose Source Container
#Chose Destination Container




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

itemToMove = Pick("Select the Item you want to move")
sourceCont = Pick("Select the source container")
destCont = Pick("Select the destination container")
items = find(sourceCont.Serial, [itemToMove.ItemID])

x = 25
y = 40
Misc.SendMessage(items)
for item in items:
    Misc.SendMessage("{},{}".format(x,y))
    if x > 120:
        x = 25
        y = y + 10
    if y >= 120:
       break 
       
    Items.Move(item, destCont, 0, x, y)
    Misc.Pause(1200)
    x = x + 10
