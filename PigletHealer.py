#Piglet Healer
while True:
    Target.WaitForTarget(1000, True)
    Target.TargetExecute(0x401BE8B4)
    Items.UseItem(0x401BE8B4)
    Target.WaitForTarget(1000, True)
    Target.TargetExecute(0x1051A3)
    Misc.Pause(10200)