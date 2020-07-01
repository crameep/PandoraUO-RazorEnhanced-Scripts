
keepIDs = [
0x0F7D, # Daemon Blood
0x0F8A, # Pig Iron
0x0EED,
0x0F86,
0x0F8E,
0x0F84,
0x0F25,
0x0F16,
0x0F15,
0x0F26,
0x0F10,
0x0F13,
0x0F19,
0x0F21,
0x0F2D,
0x0F7A,
0x0F7B,
0x0F84,
0x0F85,
0x0F86,
0x0F88,
0x0F8D,
0x0F8C,
0x14EC, # TMaps
0x14F8, # Rope
0x099F, # SOS
0x0F8E, # Crystal of Energy
0x2DB3, # Relic Fragment
0x1726, # Rough Stone
0x3186, # Putrifaction
0x3187, # Taint
0x3187, # Blight
0x3185, # Scourge
0x3184, # Corruption
0x3196, # White Pearl
0x14EF, # Scroll of Transcendence
0x0DCA, # Special Net
0x0F78, # Bat Wing
0x0F8F, # Grave Dust
0x571C, # Essence of Persistance
0x5720, #Spider Carapace
0x3195, # Ecu Citrine 
]



def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:

            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list 




Misc.SendMessage('Target a container to loot.', 76)       
contid = Target.PromptTarget()
if contid > -1:
    cont = Items.FindBySerial(contid)
    Items.WaitForContents(cont, 8000)
    Misc.Pause(500)

    
Misc.Pause(1000)        
items = find(cont.Serial, keepIDs)
for item in items:
    Misc.SendMessage("Keeping: {}".format(item),222)
    Items.Move(item, 0x40F8CB7C, 0)
    Misc.Pause(1200)
for i in cont.Contains:
    Misc.SendMessage("Trashing: {}".format(i),333)
    Items.Move(i, 0x4032FF5A, 0, 0, 0)
    Misc.Pause(1200)