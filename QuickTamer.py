target = Target.PromptTarget()
while not Player.IsGhost:
    Misc.WaitForContext(target, 10000)
    Misc.ContextReply(target, 0)
    Misc.Pause(1000)

