##Mortal Stopper
enchappleid = 0x2FD8

while not Player.IsGhost:
    if Player.YellowHits:
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
            
    
                    