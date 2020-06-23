Target.AttackTargetFromList("tab")
lastTargetID = Target.GetLastAttack()
Misc.SendMessage(hex(lastTargetID))
#lastTarget = Mobiles.FindBySerial(lastTargetID)
Misc.SendMessage(lastTarget)
while Mobiles.FindBySerial(lastTargetID) != None:
    Misc.SendMessage("Current target is: {}".format(lastTarget.Name))
    Misc.Pause(1000)