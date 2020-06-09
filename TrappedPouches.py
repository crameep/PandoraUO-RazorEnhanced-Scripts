##Use Traped Pouch to get out of Paralyze


def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:
            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list
    

    
        
        
pouchID = 0x0F0A
pouchContainer = 0x41002AA5

used = 0
numberOfPouches = 0
pouches = find(pouchContainer,[pouchID])    

Misc.SendMessage(numberOfPouches)
while not Player.IsGhost:
    if Player.Paralized:
        if not(Timer.Check("paralized")):
            Misc.Pause(100)
            Misc.SendMessage("Using Traped Pouch",222)
            Items.UseItemByID(pouchID)
            Target.WaitForTarget(3000, True)
            Target.Self()
            Timer.Create("paralized", 3000 )
            Misc.Pause(50)

            





