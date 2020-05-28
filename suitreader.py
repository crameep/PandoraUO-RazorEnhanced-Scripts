import time
import re
filterList = {
    ":": -1,
    "Tier": -1,
    "Runes": -1,
    "Rating": -1,
    "Blessed": -1,
    "Talisman": -1,
    "crafted by": -1
}

layers = [
    "RightHand", "LeftHand", "Shoes",
    "Pants", "Shirt", "Head", "Gloves",
    "Ring", "Neck", "Hair", "Waist",
    "InnerTorso", "Bracelet", "FacialHair",
    "MiddleTorso", "Earrings", "Arms",
    "Cloak", "OuterTorso", "OuterLegs",
    "InnerLegs", "Talisman"
]

myStats = {
  "luck" : 0,
  "defense chance" : 0,
  "lower reagent" : 0,
  "SDI": 0,
  "strength bonus": 0,
  "dexterity bonus": 0,
  "intelligence bonus": 0,
  "stamina increase": 0,
  "swing speed": 0,
  "DamageIncrease": 0,
  "hit point regeneration": 0,
  "hit point increase": 0,
  "mana regeneration": 0,
  "faster casting": 0,
  "faster cast recovery": 0,
  "lower mana": 0,
  "reflect physical": 0,
  "tier XP increase": 0,
  "hit chance" : 0,
  "critical hit chance": 0 ,
  "evasion": 0,
  "accuracy": 0,
  "healing increase": 0,
  "faster ethereal casting": 0,
  "perception": 0,
  "combat threat": 0,
  "physical resist": 0,
  "fire resist": 0,
  "cold resist": 0,
  "poison resist": 0,
  "energy resist": 0,
  "resilience": 0,
  "Fire Resonance": 0,
  "Soul Charger Poison": 0,
  "Soul Charge": 0,
  "Kinetic Resonance": 0,
  "Calmful Mind": 0,
  "Damage Eater": 0,
  "Kinetic Eater": 0,
  }

brm = re.compile("<[^>]+>")
stripLetters = re.compile("[^0-9]+") 

def filterFunc(s, flist=filterList):
    for k, v in filterList.iteritems():
        if s.find(k) != v:
            return True
    return False

def parseResist(s):
    import operator
    sp = s.split(" ", 2)
    sp[2] = sp[2].replace("%", "").replace("+", "")
    valsp = sp[2].split(" ")
    val = 0
    for v in valsp:
        val += int(v)
    sp[2] = str(val)
    return " ".join(sp)


filename = 'suit_{0}.txt'.format(time.strftime('%y%m%d%H%M%S'))
f = open(filename, "w")

color = 222
for layer in layers:
    item = Player.GetItemOnLayer(layer)
    if item != None:
        Items.WaitForProps(item, 8000)
        plist = list(Items.GetPropStringList(item))

        for p in plist:
            color = color + 100
            for pp in p.split("\n"):
                pp = brm.sub("", pp.strip())
                if not filterFunc(pp):
                    pp = pp.strip()
                    f.write(pp.strip() + "\n")
                    ###Cory ADDED JUNK ####
                    if "damage increase" in pp and "spell" not in pp:
                        Misc.SendMessage("Found Damage Increase")
                        valueStr = stripLetters.sub("", pp)
                        pp = "DamageIncrease" + valueStr
                    if "spell damage" in pp:
                        Misc.SendMessage("Found Spell Damage Increase")
                        valueStr = stripLetters.sub("", pp)
                        pp = "SDI" + valueStr
                    for stat in myStats.keys():
                        if stat in pp:
                            valueStr = stripLetters.sub("", pp)
                            currentValue = myStats[stat]
                            newValue = currentValue + int(valueStr)
                            myStats.update({stat : newValue})


                        ###End Cory ADDED JUNK ###
        f.write("\n")
        
f.write("TOTAL STATS\n\n")

for x in sorted(myStats.keys()):
    Misc.SendMessage("{}: {}".format(x,myStats[x]),600)
    f.write("{}: {}\n".format(x,myStats[x]))

f.close()

###Cory ADDED JUNK ####
for x in myStats.keys():
    Misc.SendMessage("{}: {}".format(x,myStats[x]),600)
###Cory ADDED JUNK ####




