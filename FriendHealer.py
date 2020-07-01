from System.Collections.Generic import List
from System import Byte

targetingRange = 3
startHealAt = 90 ## Start Healing at 90% Health.
castDelay = 500

petSerials = [0x001051A3,0x0000DE80]
petHealPot = 0x401BE8B4
petCurePot = 0x402AB22E

def FindFriends():
    fil = Mobiles.Filter()
    fil.Enabled = True
    #fil.Notorieties = List[Byte](bytes([1,2]))
    fil.RangeMax = targetingRange
    fil.Friend = 1
    friends = Mobiles.ApplyFilter(fil)
    return friends
    
def getHP(f):
    hp = float(f.Hits) / float(f.HitsMax)
    hp = hp * 100
    #Misc.SendMessage("{} HP is {}%".format(f.Name,hp))
    return hp
    
def needsCure(f):
    if not f.Poisoned or not f.YellowHits:
        return False
    else:
        return True

def CastGreaterHeal(f):
    global startHealAt
    if not needsCure:
        hp = getHP(f)
        if hp >= startHealAt - 5:
            Spells.CastMagery("Heal")
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(f)
        else:
            Spells.CastMagery("Greater Heal")
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(f)
        #END else
    else:
        Misc.SendMessage("You Need to Cure")
    #END else
    Misc.Pause(castDelay)
    
def castMiniHeal(f):
    hp = getHP(f)
    global castDelay
    global startHealAt
    if hp <= startHealAt - 5 and hp > 75:
        if not needsCure(f):
            if not(Timer.Check("miniHeal")):
                Spells.CastMagery("Heal")
                Target.WaitForTarget(1000, False)
                Target.TargetExecute(f)
                Timer.Create("miniHeal", castDelay)
def castgHeal(f):
    hp = getHP(f)
    global castDelay
    global startHealAt
    if hp <= 75:
        if not needsCure(f):
            if not(Timer.Check("gHeal")):
                Spells.CastMagery("Greater Heal")
                Target.WaitForTarget(1000, False)
                Target.TargetExecute(f)
                Timer.Create("gHeal", castDelay)
    
        
def PetHeal(f):
    global petHealPot
    if not(Timer.Check("PetHeal")):
        Misc.SendMessage("Healing {}".format(f.Name),555)
        Items.UseItem(petHealPot)
        Target.WaitForTarget(1000, False)
        Target.TargetExecute(f)
        Misc.Pause(300)
        if not Journal.Search("everlasting pet greater heal"):
            Misc.SendMessage("DETECTED")
            Journal.Clear()
            CastGreaterHeal(f)
        elif not Journal.Search("must wait"):
            Misc.SendMessage("DETECTED WAIT")
            Journal.Clear()
            castMiniHeal(f)
            CastGreaterHeal(f)
        else:
            Timer.Create("PetHeal", 11000)
    else:
        CastGreaterHeal(f)
        
def HealPlayer(f):
    Misc.SendMessage("HealPlayer")
    global startHealAt
    hp = getHP(f)
    castMiniHeal(f)
    castgHeal(f)
        
    
    
    
    
    
    
def healLoop(f):
    if f.Serial in petSerials:
        PetHeal(f)
    else:
        HealPlayer(f)
    
    
friends = FindFriends()

Misc.SendMessage(len(friends))

for friend in friends:
    Misc.SendMessage(friend.Name)
    
while not Player.IsGhost:
    friends = FindFriends()
    friend = Mobiles.Select(friends,'Weakest')
    if friend != None:
        hp = getHP(friend)
        if hp <= startHealAt:
            healLoop(friend)
    Misc.Pause(50)
            