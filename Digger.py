startX = Player.Position.X
startY = Player.Position.Y
startZ = Player.Position.Z

digrange = 2
delay = 2000

Misc.SendMessage('Target a Treasure Map', 76)       
contid = Target.PromptTarget()
if contid > -1:
    map = Items.FindBySerial(contid)
    Misc.Pause(500)

    
def checkNorth():
    for x in range( 0, digrange):
            Misc.WaitForContext(map.Serial, 10000)
            Misc.ContextReply(map.Serial, 1)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Player.Position.X, Player.Position.Y - x ,Player.Position.Z)
            Misc.Pause(delay)
def checkSouth():
    for x in range( 0, digrange):
            Misc.WaitForContext(map.Serial, 10000)
            Misc.ContextReply(map.Serial, 1)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Player.Position.X, Player.Position.Y + x ,Player.Position.Z)
            Misc.Pause(delay)
def checkEast():
    for x in range( 0, digrange):
            Misc.WaitForContext(map.Serial, 10000)
            Misc.ContextReply(map.Serial, 1)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Player.Position.X + x, Player.Position.Y ,Player.Position.Z)
            Misc.Pause(delay)
def checkWest():
    for x in range( 0, digrange):
            Misc.WaitForContext(map.Serial, 10000)
            Misc.ContextReply(map.Serial, 1)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Player.Position.X - x, Player.Position.Y,Player.Position.Z)
            Misc.Pause(delay)
def checkNorthWest():
    for x in range( 0, digrange):
            Misc.WaitForContext(map.Serial, 10000)
            Misc.ContextReply(map.Serial, 1)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Player.Position.X - x, Player.Position.Y - x,Player.Position.Z)
            Misc.Pause(delay)
def checkNorthEast():
    for x in range( 0, digrange):
            Misc.WaitForContext(map.Serial, 10000)
            Misc.ContextReply(map.Serial, 1)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Player.Position.X + x, Player.Position.Y - x,Player.Position.Z)
            Misc.Pause(delay)
def checkSouthWest():
    for x in range( 0, digrange):
            Misc.WaitForContext(map.Serial, 10000)
            Misc.ContextReply(map.Serial, 1)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Player.Position.X - x, Player.Position.Y + x,Player.Position.Z)
            Misc.Pause(delay)
def checkSouthEast():
    for x in range( 0, digrange):
            Misc.WaitForContext(map.Serial, 10000)
            Misc.ContextReply(map.Serial, 1)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Player.Position.X + x, Player.Position.Y + x,Player.Position.Z)
            Misc.Pause(delay)
            
        
checkNorth()
checkSouth()
checkEast()
checkWest()
checkNorthEast()
checkNorthWest()
checkSouthEast()
checkSouthWest()
Misc.SendMessage("Done")
