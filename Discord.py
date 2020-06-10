#Discord
def discord(enemy):
    #return
    global next_discord_time
    global discord_list
    instrumentID = 0xe9c
    drum = Items.FindByID(instrumentID, -1, Player.Backpack.Serial)
    if drum == None:
        return
    if enemy.Serial in discord_list:
        return
    now = time.time()
    if next_discord_time > time.time():
        return
    Journal.Clear()    
    Player.UseSkill('Discordance') 
    next_discord_time = time.time() + 12
    journal_msg = ""
    limit = time.time() + 1
    while time.time() < limit:
        if Journal.Search("Choose the target"):
            journal_msg = "Choose the target"
            limit = 0  # force out of loop
        if Journal.Search("shall you play"):
            journal_msg = "shall you play"
            limit = 0  # force out of loop
    if journal_msg == "":
        Target.Cancel()
        return # wtf ?
    if journal_msg == "shall you play":
        Target.WaitForTarget(500)
        Target.TargetExecute(drum)
        Misc.Pause(100)
    Target.WaitForTarget(500)
    Target.TargetExecute(enemy)
    Misc.Pause(500)
    Target.Cancel()
    if Journal.Search("play jarring music"):
        discord_list[enemy.Serial] = True
    if Journal.Search("no effect"):
        discord_list[enemy.Serial] = True
    if Journal.Search("already in discord"):
        discord_list[enemy.Serial] = True
    return