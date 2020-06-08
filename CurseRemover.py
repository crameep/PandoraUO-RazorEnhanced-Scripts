##Enchanted Apple

enchappleid = 0x2FD8

debuffs = [
    "Curse",
    "Mortal Strike" 
    "Feeblemind",
    "Strangle",
    "Mortal Wound",
    "Mind Rot",
    "Corpse Skin",
    "Bload Oath (curse)",
    "Clumsy",
    "Weaken"
]


while not Player.IsGhost:
    for debuff in debuffs:
        if Player.BuffsExist(debuff):
            if not(Timer.Check("enchantedapple")):
                Items.UseItemByID(enchappleid)
                Timer.Create("enchantedapple", 3000 )
                Misc.Pause(50)
            else:
                if not(Timer.Check("removeCurse")):
                    Spells.CastChivalry("Remove Curse")
                    Target.WaitForTarget(1000, True)
                    Target.Self()
                    Timer.Create("removeCurse", 3000 )
                    Misc.Pause(50)
            
    
                    