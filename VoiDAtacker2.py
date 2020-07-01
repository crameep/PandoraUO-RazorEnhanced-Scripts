from System.Collections.Generic import List
from System import Byte

targetingRange = 15
usePets = False
move = False
honor = True


StartWep = Player.GetItemOnLayer("LeftHand")
startX = Player.Position.X
startY = Player.Position.Y
startZ = Player.Position.Z

def returnToStart():
    if not(Timer.Check("ReturnToStart"))and move == True:
        Misc.SendMessage("Returning to Starting Position",222)
        Player.PathFindTo(startX, startY, startZ)
        Timer.Create("ReturnToStart", 30000 )

def MoveToEnemy(e):
    if move:
        Player.PathFindTo(e.Position.X, e.Position.Y, e.Position.Z)
        Misc.Pause(500)
        
def WeaponSetup():
    global targetingRange
    #Misc.SendMessage("Detecting Weapon Type")
    wep = Player.GetItemOnLayer("LeftHand")
    if wep != None:
        typeCount = len(wep.Properties)
        index = typeCount - 2
        if wep != None:
            if typeCount > 5 and wep.Properties[index]!= None:
                search = str(wep.Properties[index])
                if search.find("Ranged") != -1:
                #Misc.SendMessage("Setting Range to 7")
                    targetingRange = 12
                elif search.find("Melee") != -1:
                    targetingRange = 12
                    #Misc.SendMessage("Setting Range to 1")

        else:
            #Misc.SendMessage("Defaulting Range to 1")
            targetingRange = 7
            
def FindEnemies():
    fil = Mobiles.Filter()
    fil.Enabled = True
    fil.Notorieties = List[Byte](bytes([3,4,5,6]))
    fil.RangeMax = targetingRange
    fil.Friend = -1
    enemies = Mobiles.ApplyFilter(fil)
    return enemies  

def honor(e):
    if honor:
        if not(Timer.Check("honor")):
            Player.InvokeVirtue("Honor")
            Target.WaitForTarget(300, False)
            Target.TargetExecute(e)
            Timer.Create("honor", 5000 )
        
def SendPets(e):
    if usePets:
        if Player.Followers > 1:
            if not(Timer.Check("PetAttack")):
                Player.ChatSay(690, "All Kill")
                Target.WaitForTarget(300, False)
                Target.TargetExecute(e)
                Timer.Create("PetAttack", 4000 )            

def Main():
    while not Player.IsGhost:
        WeaponSetup()
        returnToStart()

        enemies = FindEnemies()
        enemy = Mobiles.Select(enemies,'Nearest')
        eNumber = len(enemies)
        if eNumber > 0:
            if not(Timer.Check("Divine")) and Player.Stam < (Player.StamMax * .80):
                if not Player.BuffsExist("Divine Fury"):
                    Spells.CastChivalry("Divine Fury")
                    Misc.Pause(10)
                    Timer.Create("Divine", 10000 )
            if not(Timer.Check("Consecrate")):
                Spells.CastChivalry("Consecrate Weapon")
                Misc.Pause(10)
                Timer.Create("Consecrate", 10000 )
            if not(Timer.Check("EOO")):
                if not Player.BuffsExist("Enemy Of One"):
                    Spells.CastChivalry("Enemy Of One")
                    Misc.Pause(10)
                    Timer.Create("EOO", 30000 )
            if not(Timer.Check("Bless")):
                if not Player.BuffsExist("Bless"):
                    Spells.CastMagery("Bless")
                    Target.WaitForTarget(2000, True)
                    Target.Self()
                    Misc.Pause(10)
                    Timer.Create("Bless", 2300 )
    
        if eNumber == 1:
            eNumber = 0
            if not Player.HasSpecial:
                if not(Timer.Check("Secondary")):
                    Player.WeaponSecondarySA()
                    Timer.Create("Secondary", 60000 )
                else:
                    Player.WeaponPrimarySA()
            honor(enemy)
            MoveToEnemy(enemy)
            SendPets(enemy)
            
            Player.Attack(enemy)
        if eNumber == 2:
            eNumber = 0
            if not Player.SpellIsEnabled('Momentum Strike'):
                Spells.CastBushido('Momentum Strike')
            honor(enemy)
            MoveToEnemy(enemy)
            SendPets(enemy)   
            Player.Attack(enemy) 
        if eNumber > 2 :
            eNumber = 0
            if not Player.HasSpecial:
                Player.WeaponPrimarySA()
            MoveToEnemy(enemy)    
            Player.Attack(enemy)
        Misc.Pause(250)
Main()
