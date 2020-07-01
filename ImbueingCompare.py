import time
import re
filterList = {
    ":": -1,
    "Tier": -1,
    "Runes": -1,
    "Rating": -1,
    "Blessed": -1,
    "Talisman": -1,
    "crafted by": -1
}

brm = re.compile("<[^>]+>")
stripLetters = re.compile("[^0-9]+") 

def parseResist(s):
    import operator
    sp = s.split(" ", 2)
    sp[2] = sp[2].replace("%", "").replace("+", "")
    valsp = sp[2].split(" ")
    val = 0
    for v in valsp:
        val += int(v)
    sp[2] = str(val)
    return " ".join(sp)
    
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
                   
def getProperties(item):
    if item != None:
        Items.WaitForProps(item, 8000)
        return list(Items.GetPropStringList(item))
                   
item1 = Pick("Pick First Item to Compare",False)
item2 = Pick("PIck Second Item to Compare",False)
    
Props1 = getProperties(item1)
Props2 = getProperties(item2)
Misc.SendMessage("BOO")