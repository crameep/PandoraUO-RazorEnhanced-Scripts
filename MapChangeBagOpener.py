blessBag =  Items.FindBySerial(0x40F8B1AB)
grabBag = Items.FindBySerial(0x40F8CB7C)
weaponBag = Items.FindBySerial(0x400732B1)

currentMap = Player.Map
Misc.SendMessage(currentMap)
while True:
    if currentMap != Player.Map:
        Items.UseItem(blessBag)
        Misc.Pause(700)
        Items.UseItem(grabBag)
        Misc.Pause(700)
        Items.UseItem(weaponBag)
        Misc.Pause(700)
        currentMap = Player.Map
        Misc.Pause(1000)
    Misc.Pause(1000)