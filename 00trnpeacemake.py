from System.Collections.Generic import List
from System import Byte
from itertools import chain


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

cowsbull = [
    0x000C7A49,
    0x000C7A4A,
    0x000C7A4B,
    0x000C7A4C,
    0x000C7A4D,
    0x000C7A4E,
    0x000C7A4F,
    0x000C7A2C,
    0x000C7A2D,
    0x000C7A2F,
    0x000C7A30,
    0x000C7A31,
    0x000C7A32,
    0x000C7A34
]

bearsnbugs = [
    0x000C7A1B,
    0x000C7A1C,
    0x000C7A1D,
    0x000C7A1E,
    0x000C7A1F,
    0x000C7A20,
    0x000C7A21,
    0x000C79FF,
    0x000C7A01,
    0x000C7A02,
    0x000C7A03,
    0x000C7A04,
    0x000C7A05,
    0x000C7A06
]

hiryuncu = [
    0x000C79E8,
    0x000C79EA,
    0x000C79EA,
    0x000C79EC,
    0x000C79ED,
    0x000C79EE,
    0x000C79EF,
    0x000C79D8,
    0x000C79D9,
    0x000C79DA,
    0x000C79DB,
    0x000C79DC,
    0x000C79DD,
    0x000C79DE
]


lute = 0x0EB3

def findInstrument(inst):
    for itm in Player.Backpack.Contains:
        if itm.ItemID == inst:
            Misc.Pause(1000)
            Misc.SendMessage("Found Instrument: " + str(hex(itm.Serial)), 4095)
            return itm.Serial
    return 0

def peacemake(target):
    rv = False
    Player.UseSkill("Peacemaking")
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
        rv = False
    
    elif Journal.Search("You attempt to calm your target"):
        rv = False

    elif Journal.Search("You play hypnotic music"):
        rv = True

    else:
        rv = False

    Journal.Clear()
    Misc.Pause(1000)
    return rv


def hide():
    Journal.Clear()
    Misc.Pause(250)
    Player.UseSkill("Hiding")
    Misc.Pause(1000)


    if Journal.Search("You fail to hide"):
        #Player.HeadMessage(4095, "Hide failed")
        return False
    
    elif Journal.Search("You have hidden yourself well"):
        #Player.HeadMessage(4095, "Hide success")
        return True
    else:
        #Player.HeadMessage(4095, "Hide failed")
        return False


while not Player.IsGhost:
    #for enemy in cowsbull: # til 58ish
    for enemy in chain(bearsnbugs, hiryuncu):
        while not peacemake(enemy):
            Misc.Pause(6000)

        Misc.Pause(11000)

    while hide() == False or Player.Visible:
        Misc.Pause(2000)
    Misc.Pause(16000)

"""
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
        if peacemake(enemy):
            fails = 40
            Misc.IgnoreObject(enemy.Serial)
            Misc.Pause(11000)
        else:
            fails -= 1
            if fails < 1:
                Misc.ClearIgnore()
                while hide() == False or Player.Visible:
                    Misc.Pause(2000)
                Misc.Pause(16000)
"""
