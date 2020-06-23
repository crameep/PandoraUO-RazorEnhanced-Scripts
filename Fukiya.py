#Shoot with Fukiya
if not(Timer.Check("fukiya")):
    last = Mobiles.FindBySerial(Target.GetLastAttack())
    Player.HeadMessage(222,"Fukiya: {}".format(last.Name))
    Items.UseItem(0x406DBC21)
    Target.WaitForTarget(1000, False)
    Target.TargetExecute(last)
    Timer.Create("fukiya", 15000 )
else:
    Player.HeadMessage(222,"Fukiya not ready")

