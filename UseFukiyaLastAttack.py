#Shoot with Fukiya
last = Mobiles.FindBySerial(Target.GetLastAttack())
Player.HeadMessage(222,"Fukiya: {}".format(last.Name))
Items.UseItem(0x406DBC21)
Target.WaitForTarget(1000, False)
Target.TargetExecute(last)

