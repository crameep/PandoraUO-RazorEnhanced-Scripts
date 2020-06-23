while True:

    last = Mobiles.FindBySerial(Target.GetLastAttack())
    Player.HeadMessage(222,"Cursing: {}".format(last.Name))
    Misc.SendMessage(last.Name)
    Spells.CastMagery("Curse")
    Target.WaitForTarget(1000, False)
    Target.TargetExecute(last)
    Misc.Pause(1600)