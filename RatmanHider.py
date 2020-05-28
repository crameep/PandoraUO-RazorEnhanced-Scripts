while True:
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
            Misc.Pause(3000)
            Items.WaitForProps(closest, 8000)
            if closest.Properties != None:
                Misc.SendMessage(closest.Properties)
                for x in closest.Properties:
                    Misc.SendMessage(x)
                    if "baracoon" not in x:
                        Items.Hide(closest)
                        Misc.Pause(10)
