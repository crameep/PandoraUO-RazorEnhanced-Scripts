while not Player.IsGhost:
    if not(Timer.Check("grab")):
        Player.ChatSay( 52, '[grab' )
        Misc.Pause(1000)
        Timer.Create("grab", 6000 )
        

