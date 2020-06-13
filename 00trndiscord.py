from System.Collections.Generic import List
from System import Byte


"""
"What instrument shall you play?"
"You play poorly, and there is no effect."
"You attempt to disrupt your target, but fail."
"You play jarring music, suppressing your target's strength."
"""

"""
"You have hidden yourself well"
"You fail to hide"
"
"""

lute = 0x0EB3

def findInstrument(inst):
    for itm in Player.Backpack.Contains:
        if itm.ItemID == inst:
            Misc.Pause(1000)
            Misc.SendMessage("Found Instrument: " + str(hex(itm.Serial)), 4095)
            return itm.Serial
    return 0

def discord(target):
    Player.UseSkill("Discordance")
    Misc.Pause(250)
    
    if Journal.Search("What instrument shall you play"):
        Journal.Clear()
        Player.HeadMessage(4095, "Gimme an instrument")
        ins = findInstrument(lute) # dirty
        if ins > 0:
            Items.WaitForContents(ins, 2000)
            Target.TargetExecute(ins)
        return False
        
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(target)
    Misc.Pause(1000)
    
    if Journal.Search("You play poorly, and"):
        Journal.Clear()
        return False
    
    elif Journal.Search("You attempt to disrupt your target"):
        Journal.Clear()
        return False

    elif Journal.Search("You play jarring music"):
        Journal.Clear()
        return True
    else:
        return False


def hide():
    Journal.Clear()
    Misc.Pause(250)
    Player.UseSkill("Hiding")
    Misc.Pause(1000)


    if Journal.Search("You fail to hide"):
        Player.HeadMessage(4095, "Hide failed")
        return False
    
    elif Journal.Search("You have hidden yourself well"):
        Player.HeadMessage(4095, "Hide success")
        return True
    else:
        Player.HeadMessage(4095, "Hide failed")
        return False



fil = Mobiles.Filter()
fil.Enabled = True
fil.RangeMax = 9
fil.Notorieties = List[Byte](bytes([3,4,5,6]))
fil.CheckIgnoreObject = True
fails = 40

while not Player.IsGhost:
    enemies = Mobiles.ApplyFilter(fil)
    Misc.SendMessage(str(len(enemies)) + " enemies", 4095)
    if len(enemies) < 4:
        Misc.ClearIgnore()
        while hide() == False or Player.Visible:
            Misc.Pause(2000)
        Misc.Pause(16000)
        fails= 40
        continue
    for enemy in enemies:
        Misc.Pause(100)
        if discord(enemy):
            fails = 40
            Misc.IgnoreObject(enemy.Serial)
        else:
            fails -= 1
            if fails < 1:
                Misc.ClearIgnore()
                while hide() == False or Player.Visible:
                    Misc.Pause(2000)
                Misc.Pause(16000)
