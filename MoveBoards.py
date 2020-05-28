while Items.FindByID(0x1BD7, -1, Player.Backpack.Serial) != None:
    board = Items.FindByID(0x1BD7, -1, Player.Backpack.Serial)
    Misc.SendMessage(board)
    Items.Move(board, 0x413985E1, 0)
    Misc.Pause(2000)
    