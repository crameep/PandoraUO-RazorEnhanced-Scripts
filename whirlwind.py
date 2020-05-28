from System.Collections.Generic import List
from System import Byte
def Main():
    eNumber = 0
    fil = Mobiles.Filter()
    fil.Enabled = True
    fil.RangeMax = 1
    fil.Notorieties = List[Byte](bytes([3,4,5,6]))
    while not Player.IsGhost:
        enemies = Mobiles.ApplyFilter(fil)
        Mobiles.Select(enemies,'Nearest')
        for enemy in enemies:
            eNumber += 1
        if eNumber == 1:
            eNumber = 0
            if not Player.HasSpecial:
                Player.WeaponPrimarySA()
            Player.Attack(enemy)
        if eNumber == 2:
            eNumber = 0
            if not Player.SpellIsEnabled('Momentum Strike'):
                Spells.CastBushido('Momentum Strike')
            Player.Attack(enemy) 
        if eNumber > 2 :
            eNumber = 0
            if not Player.HasSpecial:
                Player.WeaponSecondarySA()
            Player.Attack(enemy)
        Misc.Pause(250)
Main()
