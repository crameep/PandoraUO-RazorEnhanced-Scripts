import re
layers = (
"RightHand",
"LeftHand",
"Shoes",
"Pants",
"Shirt",
"Head",
"Gloves",
"Ring",
"Neck",
"Hair",
"Waist",
"InnerTorso",
"Bracelet",
"FacialHair",
"MiddleTorso",
"Earrings",
"Arms",
"Cloak",
"OuterTorso",
"OuterLegs",
"InnerLegs",
"Talisman")

myStats = {
  "luck" : 0,
  "defense chance" : 0,
  "lower reagent" : 0,
  "spell damage": 0,
  "strength bonus": 0,
  "dexterity bonus": 0,
  "intelligence bonus": 0,
  "stamina increase": 0,
  "swing speed": 0,
  "damage increase": 0,
  "hit point regeneration": 0,
  "hit point increase": 0,
  "mana regeneration": 0,
  "faster casting": 0,
  "faster cast recovery": 0,
  "lower mana": 0,
  "reflect physical": 0
  }
  
complexStats = {
  "tier XP increase": 0,
  "hit chance": 0,
  }
luck = 0
dci = 0

stripTags = re.compile("<[^>]+>")
stripLetters = re.compile("[^0-9]+") 

for layer in layers:
    item = Player.GetItemOnLayer(layer)
    if item != None:
        #Misc.SendMessage(item.Name,777)
        for prop in Items.GetPropStringList(item):
            clean = stripTags.sub("",prop)
            #Misc.SendMessage("Property: {}".format(clean),333)
            
            for stat in myStats.keys():
                if stat in clean:
                    valueStr = stripLetters.sub("", clean)
                    currentValue = myStats[stat]
                    newValue = currentValue + int(valueStr)
                    myStats.update({stat : newValue})


for x in myStats.keys():
    Misc.SendMessage("{}: {}".format(x,myStats[x]),600)