#AutoTarget

from System.Collections.Generic import List
from System import Byte

enemyfilter = Mobiles.Filter()
enemyfilter.Enabled = True
enemyfilter.RangeMax = 8
enemyfilter.Notorieties = List[Byte](bytes([3,4,5,6]))
enemies = Mobiles.ApplyFilter(enemyfilter)
Misc.Pause(200)
enemy = Mobiles.Select(enemies,'Nearest')

if enemy:
    Player.InvokeVirtue("Honor")
    Target.WaitForTarget(1000, False)
    Target.TargetExecute(enemy.Serial)
    Target.TargetExecute(enemy)
    Player.Attack(enemy)
    while Mobiles.FindBySerial(enemy.Serial)!= None:
      Misc.Pause(1000)  
      