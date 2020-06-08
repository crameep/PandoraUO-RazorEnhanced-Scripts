##Use Traped Pouch to get out of Paralyze


def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:
            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list
    
def reTrapPouches():
    Misc.SendMessage("Re-Trapping Pouches", 222)
    pouches = find(pouchContainer,[pouchID])
    global numberOfPouches
    global used
    numberofPouches = len(pouches)
    for pouch in pouches:
        Spells.CastMagery("Magic Trap")
        Target.WaitForTarget(1000,True)
        Target.TargetExecute(pouch.Serial)
        Misc.Pause(1500)
        numberOfPouches = numberOfPouches + 1
    
        
        
pouchID = 0x0E79
pouchContainer = 0x40C97091

used = 0
numberOfPouches = 0
pouches = find(pouchContainer,[pouchID])    
reTrapPouches()
Misc.SendMessage(numberOfPouches)
while not Player.IsGhost:
    if Player.Paralized:
        if not(Timer.Check("paralized")):
            if used < numberOfPouches:
                    Misc.Pause(100)
                    Misc.SendMessage("Using Traped Pouch")
                    Items.UseItem(pouches[used])
                    used = used + 1
                    Timer.Create("paralized", 3000 )
                    Misc.Pause(50)
            else:
                ###Redo Traps.
                reTrapPouches()
                Misc.Pause(50)
            





