# Keep up evasion Buff
Journal.Clear()
Spells.CastBushido("Evasion")
Timer.Create("evasion", 20000 )
while not Player.IsGhost:
    if Journal.Search("no longer feel"):
        if not(Timer.Check("evasion")):
            Misc.Pause(1000)
            Spells.CastBushido("Evasion")
            if not Journal.Search("You must wait before trying again"):
                Journal.Clear()
                Timer.Create("evasion", 21000 )
    Misc.Pause(500)

        
