#autolooter by Mourn#8182 discord contact

import sys
import math
from System.Collections.Generic import List

backpack = 0x0E75
corpse = 0x2006

pvpWeapons = "Bone Harvester|Bardiche|Broadsword|Butcher Knife|Cleaver|Katana|Longsword|Scimitar|Cutlass|Pickaxe|Hatchet|Club|Gnarled Staff|Hammer Pick|Mace|Maul|War Axe|Assasin Spike|Dagger|Kryss|Lance|Pitchfork|Leafblade|War Fork"
bokuWaki = "Bokuto|Wakizashi|No-dachi"

class AutoFarmer(object):

    lastTarget = None
    insured = []
    ignore = []
    templates = [
       [[pvpWeapons], ["Splintering Weapon", 25], ["!Antique"], ["!Brittle"]],
       [[pvpWeapons], ["Splintering Weapon", 20], ["!Antique"], ["!Brittle"], ["Hit Lower Defense", 30], ["Spell Channeling"]],
       [[pvpWeapons], ["Splintering Weapon", 30], ["!Antique"]],
       [[pvpWeapons], ["Splintering Weapon", 20], ["!Antique"], ["Hit Fireball|Hit Harm|Hit Lightning", 50]],
       [[pvpWeapons], ["Splintering Weapon", 25], ["!Antique"], ["Hit Fireball|Hit Harm|Hit Lightning", 30]],
       [[pvpWeapons], ["Splintering Weapon", 25], ["!Antique"], ["Hit Magic arrow", 50]],
       
       [["Major Artifact"], ["Strength Bonus", 4], ["Hit Point Increase", 8]],
       [["Major Artifact"], ["Dexterity Bonus", 4], ["Stamina Increase", 8]],
       [["Major Artifact"], ["Damage Eater|Kinetic Eater|Fire Eater", 12], ["Mana Regeneration", 1], ["Lower Mana Cost", 4]],
       
       [[bokuWaki], ["Hit Fireball|Hit Harm|Hit Lightning", 50], ["!Antique"], ["Splintering Weapon", 20]],
       [[bokuWaki], ["Hit Fireball|Hit Harm|Hit Lightning", 30], ["!Antique"], ["Splintering Weapon", 25]],
       [[bokuWaki], ["Spell Channeling"], ["!Antique"], ["!Brittle"], ["Splintering Weapon", 15]],
       
       [["Major Artifact"], ["Ring|Bracelet"]],
       [["Major Artifact"], ['Luck', 150]],
       [["Luck", 150], ["$countProps", { "max": 3 }]],
       
       [["Legendary Artifact"]],             #['!Bow'],['!Weapon']],
       
       [["Ring|Bracelet"], ["!Antique"], ["Swing Speed Increase", 10], ["$countProps", { "max": 3 }]],
       [["Ring|Bracelet"], ["!Antique"], ["Spell Damage Increase", 18], ["$countProps", { "max": 3 }]],
       
       [[pvpWeapons + "|" + bokuWaki], ["Splintering Weapon", 20], ["!Antique"], ["!Brittle"], ["$countProps", { "max": 3 }]]
    ]
    
    stopWords = [
        "Cursed",
    ]
    
    notInsure = "gold coin"
    
    lootingBag = None

    def __init__(self):
        self.filter = Items.Filter()
        self.filter.Enabled = True
        self.filter.IsCorpse = True
        self.filter.Graphics = List[int]((corpse))
    
    def getPropertiesAsString(self, item):
        Items.WaitForProps(item, 1000)
        lines = Items.GetPropStringList(item)
        result = []
        
        for line in lines:
            if (line[0] == "*") or (line.find("<b>") >= 0):
                continue
            
            result.append(line)    
        
        return "\n".join(result)
    
    def countProps(self, item, args):
        Items.WaitForProps(item, 1000)
        count = 0
        
        stopWords = [
            "require",
            "insured",
            "weapon speed",
            "physical damage",
            "fire damage",
            "poison damage",
            "cold damage",
            "energy damage",
            "chaos damage",
            "physical resist",
            "fire resist",
            "poison resist",
            "cold resist",
            "energy resist",
            "handed weapon",
            "magic item",
            "artifact",
            "durability",
            "weight",
            "resist",
            "prized",
            "brittle",
            "antique",
            "weapon damage"
        ]
        
        for prop in Items.GetPropStringList(item)[1:]:
            prop = prop.lower()
            validProp = True
            
            for word in stopWords:
                if prop.find(word) >= 0:
                    validProp = False
                    break
                    
            if validProp:
                count = count + 1      
        
        return count > 0 and count < args["max"]
      
    def isSuitableItem(self, item):
        Items.WaitForProps(item, 1000)
        
        for prop in self.stopWords:
            if Items.GetPropValue(item, prop):
                return False     
                
        for props in self.templates: 
            pairCount = len(props)
            suitableCount = 0
            suitableProps = []
            
            for pair in props:
                parts = []  
                
                if pair[0].find("|") > 0:
                    for subPart in pair[0].split("|"):
                        parts.append(subPart.strip())
                else:
                    parts.append(pair[0])
                    
                for subPart in parts:   
                    if (len(pair) == 1):
                        notCond = False
                        strPart = subPart
                        
                        if strPart[0] == "!":
                            notCond = True
                            strPart = strPart[1:]      
                                
                        if notCond:
                            suitableCount = suitableCount + 1
                            
                            for prop in Items.GetPropStringList(item):
                                if prop.lower().find(strPart.lower()) >= 0:
                                    suitableCount = suitableCount - 1
                                    break
                                
                        else:     
                            for prop in Items.GetPropStringList(item):
                                if prop.lower().find("required") >= 0:
                                    continue
                                
                                if strPart.find(" ") > 0 and prop.lower().find(strPart.lower()) >= 0:
                                    suitableCount = suitableCount + 1
                                    suitableProps.append(strPart.lower())
                                    break
                                elif strPart.find(" ") < 0:
                                    words = prop.lower().split(" ")
                                    needle = strPart.lower()
                                    isContains = False
                                    
                                    for word in words:
                                        if word.find(needle) == 0:
                                            isContains = True
                                            break
                                            
                                    if isContains:
                                        suitableCount = suitableCount + 1
                                        suitableProps.append(needle)
                                        break
                  
                                         
                    elif (len(pair) == 2):
                        if (subPart[0] != "$") and (int(Items.GetPropValue(item, subPart.lower())) >= int(pair[1])):
                            suitableCount = suitableCount + 1
                            suitableProps.append(subPart.lower())
                            break
                        elif (subPart[0] == "$"):
                            method = subPart[1:]
                                
                            if getattr(self, method)(item, pair[1]):
                                suitableCount = suitableCount + 1
                                suitableProps.append(method)
                            
                            break
                                
            if suitableCount == pairCount:
                Misc.SendMessage(",".join(suitableProps))
                return True
                      
        return False
          
    def isItemInsured(self, item):
        Items.WaitForProps(item, 1000)
        
        for prop in Items.GetPropStringList(item):
            if prop.find("Insured") >= 0:
                return True
                
        return False

    def autoInsureAll(self):
        container = self.lootingBag if self.lootingBag else Player.Backpack
        Misc.Pause(100)
        
        for item in container.Contains:
            Items.WaitForProps(item, 1000)
            
            if (not Items.GetPropValue(item, 'durability')) or (self.isItemInsured(item)):
                continue
            
            self.insureItem(item)    

    def calcDistance(self, item):
        corpse = Items.FindBySerial(item.Container)
        
        if not corpse:
            return 999
        
        cords = corpse.Position
        return math.ceil(math.sqrt(math.pow(Player.Position.X - cords.X, 2) + math.pow(Player.Position.Y - cords.Y, 2)))
        
    def insureItem(self, item):
        if self.notInsure.find(item.Name.lower()) >= 0:
            return;
        
        Target.Cancel()
        
        Misc.WaitForContext(Player.Serial, 3000)
        Misc.ContextReply(Player.Serial, "Toggle Item Insurance")
        Target.WaitForTarget(2000, True)
        Target.TargetExecute(item)
        Misc.Pause(600)
        
        Target.Cancel()      
 
    def lootCorpses(self, container):
        corpses = Items.ApplyFilter(self.filter)
        corpsesToLoot = []
        
        for corpse in corpses:        
            if (corpse.Serial in self.ignore) or (self.calcDistance(corpse) > 2):
                continue
                
            corpsesToLoot.append(corpse)
            self.ignore.append(corpse.Serial)
            
        if not corpsesToLoot:
            return
        
        Misc.SendMessage("Corpses found: " + str(len(corpsesToLoot)))
        
        for corpse in corpsesToLoot:
            Misc.Pause(100)
            Items.UseItem(corpse)
            Misc.Pause(1400)
            if not corpse.Contains:
                continue
                
            itemsToLoot = []
        
            for item in corpse.Contains:
                Items.WaitForProps(item.Serial, 1000)
                
                if not self.isSuitableItem(item):
                    continue    
                    
                itemsToLoot.append(item)
            
            if not itemsToLoot:
                continue
            
            Misc.SendMessage("Items found: " + str(len(itemsToLoot)),30)
        
            for item in itemsToLoot:
                Misc.Pause(2000)
                Items.Move(item.Serial, container.Serial, 0)
                
                Misc.SendMessage(self.getPropertiesAsString(item),30)
                
            for item in itemsToLoot:
                if item.Serial in self.insured:
                    continue
                    
                    Misc.Pause(1600)    
                    
                self.insureItem(item)    
                self.insured.append(item.Serial)
                                                          
    def Main(self):
                 
        for item in Player.Backpack.Contains:
            if item.ItemID == 0x0E75:
                self.lootingBag = item               
                Items.UseItem(item)
                Misc.Pause(600)
                   
        if not self.lootingBag:
            target = Target.PromptTarget("Select a bag for loot")            
            if target > 0:         
                self.lootingBag = Items.FindBySerial(target)               
                Items.UseItem(self.lootingBag)
                Misc.Pause(600)
                        
        while True:
            Misc.Pause(300)            
            if not Timer.Check("insure"):
                self.autoInsureAll()
                Timer.Create("insure", 10000)
            if not Timer.Check("looting"):
                self.lootCorpses(self.lootingBag)
                Timer.Create("looting", 3500)
            
                
farmer = AutoFarmer()
farmer.Main()    