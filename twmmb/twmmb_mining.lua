-- ;==================================
-- ; Module Name: Mining
-- ; Author: Antipatiko
-- ;==================================
setfenv(1, TWMMB)
Mining = {
  isLoaded = function()
    return true
  end
}

-- ---------------------------
-- @ Extends: CliLocs
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
CliLoc.BackpackFull = "Your backpack is full, so the ore you mined is lost."
CliLoc.FoundAGem = "You have found a .+"
CliLoc.NoMetalHereToMine = "There is no metal here to mine"
CliLoc.NoSandHereToMine = "There is no sand here to mine"
CliLoc.SelectAnotherPile = "Select another pile of ore with which to combine this."
CliLoc.SelectForge = "Select the forge on which to smelt the ore"
CliLoc.SomeoneBeforeYou = "Someone has gotten to the metal before you"
CliLoc.WhereToDig = "Where do you wish to dig?"
CliLoc.YouCarefullyDig = "You carefully dig up sand of sufficient quality for glassblowing"
CliLoc.YouCarefullyExtract = "You carefully extract some workable stone from the ore vein!"
CliLoc.YouDigForAWhile = "You dig for a while but fail to find any of sufficient quality for glassblowing"
CliLoc.YouDigSome = "You dig some .+ [Oo]re and put it in your backpack."
CliLoc.YouLoosenSomeRocks = "You loosen some rocks but fail to find any useable ore"
CliLoc.YouPutSomeOre = "You put some .+ ore in your backpack"
-- Specific strings for Sphere shards:
CliLoc.SphereNothingHereToMineFor = "There is nothing here to mine for."
CliLoc.SphereWhereShovel = "Where do you want to use the shovel?"
CliLoc.SphereYouDigDiamond = "You dig some flawless diamond and put it in your backpack."
CliLoc.SphereYouPutTheOre = "You put the .+ Ore in your pack."

-- ---------------------------
-- @ Extends: Types
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Type.Forge = {4017, 6522, 6526, 6530, 6534, 6538, 6546, 6550, 6554, 6558, 6562, 11736}
Type.Gems = {12690, 3861, 3862, 3856, 12696, 3859, 3865, 3877, 12693, 3878, 12692, 3873, 12695, 3885, 12691}
Type.Ingot = {7154, 7139, 7151, 7145, 7157}
Type.MiningTools = {3717, 3718, 3897, 3898}
Type.OreSmall = {6583}
Type.OreMedium = {6584, 6586}
Type.OreLarge = {6585}
Type.ProspectorsTool = {}
Type.Sand = {4586}
Type.Stone = {6009}
Type.OreCombinable = table.join(Type.OreSmall, Type.OreMedium)
Type.Ore = table.join(Type.OreSmall, Type.OreMedium, Type.OreLarge)
Type.SandAndStone = table.join(Type.Sand, Type.Stone)

-- ---------------------------
-- @ Extends: Char
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Char.MiningTool = nil

-- ---------------------------
-- $ Mining $ DEFINITIONS
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mining.ForgeSpots = false
Mining.IngotsReserve = 20
Mining.OreWeight = 12

local function MiningTool()
  Char.MiningTool = FindTool(Char.MiningTool, Type.MiningTools)
  return Char.MiningTool
end

local function MiningEntriesLoop()
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  repeat
    sleep()
    CheckContext()
    while (Bot.JournalIndex < Journal:EntryCount()) do
      Bot.JournalIndex = Bot.JournalIndex + 1
      local Entry = Journal:getEntry(Bot.JournalIndex)
      if Entry:match(CliLoc.YouDigSome) or Entry:match(CliLoc.YouPutSomeOre) or 
          Entry:match(CliLoc.SphereYouPutTheOre) then
        return true
      elseif Entry:match(CliLoc.NoMetalHereToMine) or Entry:match(CliLoc.NoSandHereToMine) or 
          Entry:match(CliLoc.SphereNothingHereToMineFor) then
        EightEight:SetDry()
        return false
      elseif Entry:match(CliLoc.BackpackFull) then
        ShardFeatures.Clear (ShardFeatures.HumanStrongBack)
        Char.CarryCapacity()
        return false
      elseif Entry:match(CliLoc.TooFarAway) then
        Rail:SetSkip()
        return false
      elseif Entry:match(CliLoc.YouLoosenSomeRocks) or Entry:match(CliLoc.YouCarefullyDig) or 
          Entry:match(CliLoc.YouCarefullyExtract) or Entry:match(CliLoc.YouDigForAWhile) or 
          Entry:match(CliLoc.SomeoneBeforeYou) or Entry:match(CliLoc.FoundAGem) or 
          Entry:match(CliLoc.SphereYouDigDiamond) then
        -- Default:
        return true
      end
    end
  until getticks() > Timeout
  -- If we timed out, skipping the current rail might help move the Task forward.
  Rail:SetSkip()
  return false
end

local function Mining_fn(x, y, z, k, t)
  setXYZKT(MiningTool(), x, y, z, k, t)
  UOMacro.__fn(false, UOMacro.LastObject)
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  repeat
    sleep()
    CheckContext()
    while (Bot.JournalIndex < Journal:EntryCount()) do
      Bot.JournalIndex = Bot.JournalIndex + 1
      local Entry = Journal:getEntry(Bot.JournalIndex)
      if Entry:match(CliLoc.WhereToDig) or Entry:match(CliLoc.SphereWhereShovel) then
        GetGumps()
        Target(Timeout - getticks())
        UOMacro.__fn(true, UOMacro.LastTarget)
        return
      elseif Entry:match(CliLoc.MustWaitFor) or Entry:match(CliLoc.IgnoringActionRequest) then
        sleep(ScaledMS(100))
        UOMacro:fn(false, UOMacro.LastObject)
      elseif Entry:match(CliLoc.YouCantRiding) then
        ErrorHandling("Please dismount and restart the script!")
      end
    end
  until getticks() > Timeout
  ErrorHandling("Fatal error. Unable to continue mining.")
end

function OreVeinsAvailable()
  -- We average the time it takes for ore veins to replenish (typically, 10-20 minutes)
  -- and use that number for our calculations.
  local OreRespawnDelay = average(RESOURCE_REPLENISH_MIN_MS, RESOURCE_REPLENISH_MAX_MS)
  local Ticks = getticks()
  local Available = 0
  for r = 1, RAIL:count() do
    if RAIL:A(r) == "Mine" and Rail:Available(r) then
      local LastDry = RAIL[r].LastDry or 0
      if (Ticks - LastDry) > OreRespawnDelay then
        Available = Available + 1
      end
    end
  end
  dbg_print(("OreVeinsAvailable() -> Total = %d"):format(Available))
  return Available
end

function MoveOre(Source, Dest, Remaining)
  FindItem:Cont(Source)
  FindItem:Type(Type.Ore)
  if FindItem.Count == 0 then
    return
  end
  for i = 1, FindItem.Count do
    local Item = FindItem:get(i)
    local Amount = math.min(Remaining, Item.Stack)
    DragItem(Item.ID, Amount)
    DropItem:Cont(Dest)
    Remaining = Remaining - Amount
    if Remaining == 0 then return end
  end
end

local function MoveOretoBank()
  MoveOre(UO.BackpackID, BankBox.ID, AMOUNT_MAX)
end

local function MoveOretoBackpack()
  if Mining.ForgeSpots then
    local Amount = (Char:BackpackCapacity() / Mining.OreWeight) - 1
    if Amount > 0 then
      MoveOre(BankBox.ID, UO.BackpackID, Amount)
    end
  end
end

local function MoveIngotstoBag()
  MoveItems(Type.Ingot, UO.BackpackID, GetIngotBag(), ItemType.COLORED)
  local Amount = CountIronIngots(UO.BackpackID)
  if Config.Tinkering then
    Amount = Amount - Mining.IngotsReserve
  end
  if Amount > 0 then
    MoveItems(Type.Ingot, UO.BackpackID, GetIngotBag(), ItemType.IRON, Amount)
  end
end

local function MoveToolstoBank()
  local Amount = CountItem(Type.MiningTools, UO.BackpackID) - Config.ToolsInBackPack
  if Amount > 0 then
    IgnoreItem.Local:this(Char.MiningTool)
    MoveItems(Type.MiningTools, UO.BackpackID, BankBox.ID, ItemType.ALL, Amount)
    IgnoreItem.Local:Reset()
  end
end

local function DropOreLoop()
  local Count = 0
  if UO.Weight > Char:maxWeight() then
    Count = CountStack(Type.OreSmall, UO.BackpackID, true)
    if Count > 0 then
      local Amount = math.min(Count, (math.abs(Char:BackpackCapacity()) / 2) + 1)
      DropItems(Type.OreSmall, Amount, true)
      return true
    end
    Count = CountStack(Type.OreMedium, UO.BackpackID, true)
    if Count > 0 then
      local Amount = math.min(Count, (math.abs(Char:BackpackCapacity()) / 7) + 1)
      DropItems(Type.OreMedium, Amount, true)
      return true
    end
    Count = CountStack(Type.OreLarge, UO.BackpackID, true)
    if Count > 0 then
      local Amount = math.min(Count, (math.abs(Char:BackpackCapacity()) / 12) + 1)
      DropItems(Type.OreLarge, Amount, true)
      return true
    end
    Count = CountStack(Type.OreSmall, UO.BackpackID)
    if Count > 0 then
      local Amount = math.min(Count, (math.abs(Char:BackpackCapacity()) / 2) + 1)
      DropItems(Type.OreSmall, Amount)
      return true
    end
    Count = CountStack(Type.OreMedium, UO.BackpackID)
    if Count > 0 then
      local Amount = math.min(Count, (math.abs(Char:BackpackCapacity()) / 7) + 1)
      DropItems(Type.OreMedium, Amount)
      return true
    end
    Count = CountStack(Type.OreLarge, UO.BackpackID)
    if Count > 0 then
      local Amount = math.min(Count, (math.abs(Char:BackpackCapacity()) / 12) + 1)
      DropItems(Type.OreLarge, Amount)
      return true
    end
  end
  return false
end

-- ---------------------------
-- ;;; Forging
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
local Forging = {}

function Forging:FindForge()
  FindItem:Ground()
  FindItem:Type(Type.Forge)
  if FindItem.Count > 0 then
    local Item = FindItem:get()
    dbg_print(("Forging:FindForge() -> Forge ID: %d"):format(Item.ID))
    return Item.ID
  else
    dbg_print("Forging:FindForge() -> Found no forge at this spot!")
    return
  end
end

function Forging:SetIDs(Forge_ID, Ore_ID)
  UO.LObjectID = Ore_ID
  if ShardFeatures:Get(ShardFeatures.SmeltDblClickOre) then
    dbg_print("Forging:SetIDs() -> Double click ore = true")
    UO.LTargetKind = RAIL[Char.rail].Tkind
    if UO.LTargetKind == 1 then
      dbg_print(("Forging:SetIDs() -> LTargetID: %d"):format(Forge_ID))
      UO.LTargetID = Forge_ID
    else
      UO.LTargetX = RAIL[Char.rail].Tx
      UO.LTargetY = RAIL[Char.rail].Ty
      UO.LTargetZ = RAIL[Char.rail].Tz
      UO.LTargetTile = RAIL[Char.rail].Ttile
    end
  elseif ShardFeatures:Get(ShardFeatures.SmeltDblClickForge) then
    dbg_print("Forging:SetIDs() -> Double click forge = true")
    UO.LObjectID = Forge_ID
    UO.LTargetID = Ore_ID
    UO.LTargetKind = 1
  end
end

function Forging:fn()
  UOMacro:fn(true, UOMacro.LastObject)
  if ShardFeatures:Get(ShardFeatures.SmeltOnDblClick) then
    dbg_print("Forging:fn() -> Smelt on double click = true")
    ActionDelay()
    return true
  end
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  repeat
    sleep()
    CheckContext()
    while (Bot.JournalIndex < Journal:EntryCount()) do
      Bot.JournalIndex = Bot.JournalIndex + 1
      local Entry = Journal:getEntry(Bot.JournalIndex)
      if Entry:match(CliLoc.SelectForge) or Entry:match(CliLoc.SelectAnotherPile) then
        GetGumps()
        Target(Timeout - getticks())
        UOMacro.__fn(true, UOMacro.LastTarget)
        ActionDelay()
        return
      elseif Entry:match(CliLoc.MustWaitFor) or Entry:match(CliLoc.IgnoringActionRequest) then
        sleep(ScaledMS(100))
        UOMacro:fn(true, UOMacro.LastObject)
      end
    end
  until getticks() > Timeout
  ErrorHandling("Unable to smelt ore... Stuck at forge!")
end

function Forging:SmeltOreLoop(Forge_ID, Container)
  CheckContext()
  FindItem:Cont(Container)
  FindItem:Type(Type.Ore)
  if FindItem.Count == 0 then
    dbg_print("SmeltOre() -> Found no ore to smelt!")
    return false
  end
  local Ore = FindItem:get()
  dbg_print(("SmeltOre() -> Found: %d ore pile(s) to smelt!"):format(FindItem.Count))
  dbg_print(("SmeltOre() -> Ore ID: %d; Type: %d; Amount: %d"):format(Ore.ID, Ore.Type, Ore.Stack))
  -- Might need to combine ore later.
  if table.match(Type.OreCombinable, Ore.Type) and Ore.Stack == 1 then
    dbg_print(("SmeltOre() -> Ignoring Ore: %d as it's combinable. (stack = 1)"):format(Ore.ID))
    IgnoreItem.Local:this(Ore.ID)
    return true
  end
  dbg_print(("SmeltOre() -> Will attempt to smelt Ore with ID: %d"):format(Ore.ID))
  Forging:SetIDs(Forge_ID, Ore.ID)
  Forging:fn()
  FindItem:Cont(Container)
  FindItem:ID({Ore.ID})
  if FindItem.Count > 0 and FindItem:get().Stack == Ore.Stack then
    dbg_print(("SmeltOre() -> Ignoring Ore: %d cause we couldn't smelt it!"):format(Ore.ID))
    IgnoreItem.Local:this(Ore.ID)
  end
  return true
end

function Forging:SmeltOre(Forge_ID, Cont)
  repeat until not Forging:SmeltOreLoop(Forge_ID, Cont)
  IgnoreItem.Local:Reset()
end

function Forging:SmeltPackAnimalOre(Forge_ID)
  if not PackAnimals:Check() then
    return
  end
  for key, ID in pairs(PackAnimals.List) do
    local Mobile = PackAnimal[ID]
    Mobile:OpenBackpack()
    if ShardFeatures:Get(ShardFeatures.SmeltDblClickForge) then
      Forging:SmeltOre(Forge_ID, Mobile.ContID)
    else
      while CountStack(Type.Ore, Mobile.ContID) > 0 do
        local Amount = (Char:BackpackCapacity() / Mining.OreWeight) - 1
        if Amount > 0 then
          MoveOre(Mobile.ContID, UO.BackpackID, Amount)
          Forging:SmeltOre (Forge_ID, UO.BackpackID)
        else
          dbg_print("PackAnimals:SmeltOre() -> Error: Ore amount is zero.")
        end
      end
    end
    Mobile:getStones()
    Mouse:RightClick(270, 70) -- Close gump.
  end
end

local function FindForgeSpots()
  Mining.ForgeSpots = false
  for r = 1, RAIL:count() do
    if RAIL:A(r) == "Forge" and (not RAIL:skip(r)) then
      Mining.ForgeSpots = true
      return
    end
  end
end

function CountIronIngots(Container)
  return CountStack(Type.Ingot, Container, true)
end

function CountIronOre(Container)
  return CountStack(Type.Ore, Container, true)
end

function Mining.Init()
  Mining.SpotsAvailable = OreVeinsAvailable()
  -- Bot.Tools is set here since Type.MiningTools can be modified at runtime (after shard detection).
  Bot.Tools = table.join(Bot.Tools, Type.MiningTools)
  FindForgeSpots()
end

function Mining.atBank()
  MoveOretoBank()
  MoveItems(Type.Gems, UO.BackpackID, BankBox.ID)
  MoveItems(Type.Sand, UO.BackpackID, BankBox.ID)
  MoveItems(Type.Stone, UO.BackpackID, BankBox.ID)
end

function Mining.LoadTools()
  if CountItem(Type.MiningTools, UO.BackpackID) < Config.ToolsInBackPack then
    if CountItem(Type.MiningTools, BankBox.ID) > 0 then
      MoveItem(Type.MiningTools, BankBox.ID, UO.BackpackID)
      return true
    end
  end
  return false
end

function Mining.PostLoadTools()
  if CountItem(Type.MiningTools, UO.BackpackID) == 0 then
    ErrorHandling("Low on Mining tools. Please restock.")
  end
end

function Mining.PostBank()
  MoveIngotstoBag()
  MoveToolstoBank()
  MoveOretoBackpack()
end

function Mining.GetTask_Overweight()
  if CountStack(Type.Ore, UO.BackpackID) == 0 then
    return
  end
  Bot.Task = Mining.ForgeSpots and {"Forge"} or {"Bank"}
end

function Mining.GetTask_Early()
  if #Bot.Task == 0 then
    if CountStack(Type.Ingot, UO.BackpackID) >= (Config.Coward + Mining.IngotsReserve) then
      dbg_print("Mining.GetTask_Early() -> Ingot count > Coward")
      Bot.Task = {"Bank"}
    end
  end
end

function Mining.GetTask()
  if OreVeinsAvailable() > 0 and CountItem(Type.MiningTools, UO.BackpackID) > 0 then
    Bot.Task = {"Mine"}
  else
    local SmeltableOreCnt = CountStack(Type.Ore, UO.BackpackID) - CountStack(Type.OreCombinable, UO.BackpackID)
    dbg_print(("Mining.GetTask() -> Smeltable ore count: %d"):format(SmeltableOreCnt))
    local Task = SmeltableOreCnt > 0 and {"Forge"} or {"Bank"}
    Bot.Task = RAIL:A(Char.rail) == "Bank" and {"Relax", "StandStill"} or Task
  end
end

function Mining.Harvest(x, y, z, k, t)
  if not (RAIL:A(Char.rail) == "Mine") then
    return
  end
  repeat
    Mining_fn(x, y, z, k, t)
    if not MiningEntriesLoop() or CountItem(Type.MiningTools, UO.BackpackID) == 0 or
        UO.Weight > (Char:maxWeight() - 25) or Char.UnderAttack then
      Char:setTaskDone(true)
    end
  until (Char:TaskDone())
end

function Mining.Relax()
  if OreVeinsAvailable() > 0 then
    dbg_print("Mining.Relax() -> Premature end of task.")
    return
  end
  repeat
    CheckContext()
    UO.SysMessage("All ore veins are exhausted. Waiting for respawn!", 5110)
    sleep(10 * SEC_TO_MSEC)
  until (OreVeinsAvailable() > 0)
end

function Mining.DropOre()
  repeat until (not DropOreLoop())
end

function Mine()
  repeat until (not Harvest())
end

function Forge()
  local r = Char.rail
  while (not (UO.CharPosX == RAIL[r].x and UO.CharPosY == RAIL[r].y)) do
    UO.Pathfind(RAIL[r].x, RAIL[r].y, RAIL[r].z)
    sleep(500)
  end
  local Forge = Forging:FindForge()
  if not Forge then
    Rail:SetSkip()
    return
  end
  Forging:SmeltOre(Forge, UO.BackpackID)
  Char:setTaskDone(true)
end
