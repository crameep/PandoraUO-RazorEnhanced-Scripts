containerSerial = 0x400732B1
grabBagSerial = 0x40F8CB7C
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

for rune in runes:
    Items.Move(rune, containerSerial, 0, 21, 13)
    Misc.Pause(700)


