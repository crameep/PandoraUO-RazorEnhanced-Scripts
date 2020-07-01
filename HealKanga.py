import time
import sys
import math
#
if not Misc.CurrentScriptDirectory() in sys.path:
    sys.path.append(Misc.CurrentScriptDirectory())
#

import System
import common as common
import hoboconstants as hobo

for x in common.razorModules:
    x = str(x)
    exec(compile("common." + x + " = " + x, "<retards>", "exec"))
    
for pet in hobo.PetSerials:
    Misc.SendMessage(pet)
    
    
def findPets():
    petFilter = Mobiles.Filter()
    petFilter.RangeMin = 0
    petFilter.RangeMax = 7
    petFilter.IsHuman = 0
    petFilter.IsGhost = 0
    petFilter.Friend = 1
    
    pets = Mobiles.ApplyFilter( petFilter )
    
    return pets
    
while not Player.IsGhost:
    pets = findPets()
    weakest = Mobiles.Select(pets, "weakest")
    if weakest != None:
        weakestCurrentHP = (float(weakest.Hits) / float(weakest.HitsMax)) * 100
        for pet in pets:
            currentHP = (pet.Hits / pet.HitsMax) * 100
            if pet.Hits != pet.HitsMax:
                if currentHP < weakestCurrentHP:
                    Misc.SendMessage("Healing {}".format(pet.Name),222)
                    Items.UseItem(0x401BE8B4)
                    Target.WaitForTarget(10000, False)
                    Target.TargetExecute(pet)
                    Misc.Pause(11000)
    
    
