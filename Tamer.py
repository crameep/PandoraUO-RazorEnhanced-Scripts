def Pick(text): 
    Misc.SendMessage(text, 76)
    chosenid = Target.PromptTarget()
    if chosenid > -1:
        
        chosen = Mobiles.FindBySerial(chosenid)
        Misc.Pause(500)
        return chosen
tame = Pick("Choose Creature to tame")
while True:
    Misc.WaitForContext(tame.Serial, 10000)
    Misc.ContextReply(tame.Serial, 0)
    Misc.Pause(1000)