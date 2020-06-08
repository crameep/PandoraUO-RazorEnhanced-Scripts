containerSerial = 0x40C97091
grabBagSerial = 0x40C97091
OrgGrabBag = 0x40C97091
runeID = 0x1F14

def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:
            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list 
    
runes = find(Player.Backpack.Serial, [runeID])
unravels = find(Player.Backpack.Serial, [0x573C])

for rune in runes:
    Items.Move(rune, containerSerial, 0, 21, 13)
    Misc.Pause(700)
    
for unravel in unravels:
    Items.Move(unravel, OrgGrabBag, 0, 130, 13)
    Misc.Pause(700)
    


