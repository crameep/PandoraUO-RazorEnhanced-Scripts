from System.Collections.Generic import List
from System import Byte

usePets = True
move = False
targetingRange = 1
StartWep = Player.GetItemOnLayer("LeftHand")

def WeaponSetup():
    global targetingRange
    #Misc.SendMessage("Detecting Weapon Type")
    wep = Player.GetItemOnLayer("LeftHand")
    typeCount = len(wep.Properties)
    index = typeCount - 2
    if wep != None:
        if typeCount > 5 and wep.Properties[index]!= None:
            search = str(wep.Properties[index])
            if search.find("Ranged") != -1:
                #Misc.SendMessage("Setting Range to 7")
                targetingRange = 7
            elif search.find("Melee") != -1:
                targetingRange = 1
                #Misc.SendMessage("Setting Range to 1")
                
    else:
        #Misc.SendMessage("Defaulting Range to 1")
        targetingRange = 7
WeaponSetup()
                               
def SendPets(e):
    if not(Timer.Check("PetAttack")):
        Player.ChatSay(690, "All Kill")
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(e)
        Timer.Create("PetAttack", 2000 )
def MoveToEnnemy(e):
    Player.PathFindTo(e.Position.X, e.Position.Y, e.Position.Z)
    Misc.Pause(1000)
def Main():
    Misc.SendMessage(targetingRange)
    eNumber = 0
    fil = Mobiles.Filter()
    fil.Enabled = True
    fil.RangeMax = targetingRange
    fil.Notorieties = List[Byte](bytes([3,4,5,6]))
    while not Player.IsGhost:
        CurWep = Player.GetItemOnLayer("LeftHand")
        if CurWep != None:
            if StartWep.Name != CurWep.Name:
                Misc.SendMessage("Detected Weapon Change")
                break
        enemies = Mobiles.ApplyFilter(fil)
        Mobiles.Select(enemies,'Nearest')
        for enemy in enemies:
            eNumber += 1
        if eNumber > 0:
            if not(Timer.Check("Divine")):
                Spells.CastChivalry("Divine Fury")
                Misc.Pause(10)
                Timer.Create("Divine", 10000 )
            if not(Timer.Check("Consecrate")):
                Spells.CastChivalry("Consecrate Weapon")
                Misc.Pause(10)
                Timer.Create("Consecrate", 10000 )
            if not(Timer.Check("EOO")):
                Spells.CastChivalry("Enemy Of One")
                Misc.Pause(10)
                Timer.Create("EOO", 30000 )
    
        if eNumber == 1:
            eNumber = 0
            if not Player.HasSpecial:
                Player.WeaponPrimarySA()
            Player.Attack(enemy)
            #MoveToEnnemy(enemy)
            #SendPets(enemy)
        if eNumber == 2:
            eNumber = 0
            if not Player.SpellIsEnabled('Momentum Strike'):
                Spells.CastBushido('Momentum Strike')
            Player.Attack(enemy)
            #SendPets(enemy)
            #MoveToEnnemy(enemy)
        if eNumber > 2 :
            eNumber = 0
            if not Player.HasSpecial:
                Player.WeaponPrimarySA()
            Player.Attack(enemy)
            #SendPets(enemy)
            #MoveToEnnemy(enemy)
        Misc.Pause(250)
Main()