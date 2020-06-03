def WeaponSetup():
    wep = Player.GetItemOnLayer("LeftHand")
    if wep != None:
        Misc.SendMessage(wep.Name)
        
WeaponSetup()