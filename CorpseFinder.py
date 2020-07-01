startPos = Player.Position
while True:
    
    if not(Timer.Check("ReturnToStart")):
        Timer.Create("ReturnToStart", 10000 )
        Player.PathFindTo(startPos.X, startPos.Y, startPos.Z )
    corpse = Items.Filter()
    corpses = Items.Filter.Serials
    corpse.Enabled = True
    corpse.OnGround = True
    corpse.IsCorpse = 1
    corpse.RangeMax = 10
    corpse.CheckIgnoreObject = True

    corpses = Items.ApplyFilter(corpse)
    closest = Items.Select(corpses, 'Nearest')
    if closest != None:
        Misc.IgnoreObject(closest.Serial)
        Misc.SendMessage(closest.Serial)
        Player.PathFindTo(closest.Position.X, closest.Position.Y, closest.Position.Z )
        Misc.Pause(5000)
        Items.Hide(closest)
        Misc.Pause(1000)
