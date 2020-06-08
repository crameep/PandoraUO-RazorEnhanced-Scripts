-- ;==================================
-- ; Module Name: Tinkering
-- ; Author: Antipatiko
-- ;==================================
setfenv(1, TWMMB)
Tinkering = {
  isLoaded = function()
    return true
  end
}

-- ---------------------------
-- @ Extends: Types
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Type.TinkerTool = {7864, 7865, 7868}

-- ---------------------------
-- @ Extends: Char
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Char.TinkeringTool = nil

-- ---------------------------
-- $ Tinkering $ VARS
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tinkering.Gump = {}
Tinkering.Gump.contPos = {250, 150}
Tinkering.Gump.Menu_NextPage = {630, 420}
Tinkering.Gump.Menu_Shovel = {480, 220, Page = 2}
Tinkering.Gump.Menu_TinkersTools = {480, 280}
Tinkering.Gump.Menu_Tools = {275, 260}
Tinkering.Gump.Size = {530, 437}

local function MoveToolstoBank()
  local Amount = CountItem(Type.TinkerTool, UO.BackpackID) - Config.CraftingToolsInBackPack
  if Amount > 0 then
    IgnoreItem.Local:this(Char.TinkeringTool)
    MoveItems(Type.TinkerTool, UO.BackpackID, BankBox.ID, ItemType.ALL, Amount)
    IgnoreItem.Local:Reset()
  end
end

local function TinkeringTool()
  Char.TinkeringTool = FindTool(Char.TinkeringTool, Type.TinkerTool, false)
  return Char.TinkeringTool
end

local function CraftTinkeringTool()
  Bot.JournalIndex = Journal:EntryCount()
  UO.LObjectID = TinkeringTool()
  UOMacro:fn(true, UOMacro.LastObject)
  if CraftChecks(Tinkering.Gump.Size) then
    contPos(unpack(Tinkering.Gump.contPos))
    Mouse:LeftClick(unpack(Tinkering.Gump.Menu_Tools)) -- ::Tools
    FindGumpLoop({Size = Tinkering.Gump.Size})
    contPos(unpack(Tinkering.Gump.contPos))
    Mouse:LeftClick(unpack(Tinkering.Gump.Menu_TinkersTools)) -- ::tinker's tools
    -- The tool might have broken.
    PostCrafting(Tinkering.Gump.Size)
  end
end

local function CraftMiningTool()
  Bot.JournalIndex = Journal:EntryCount()
  UO.LObjectID = TinkeringTool()
  UOMacro:fn(true, UOMacro.LastObject)
  if CraftChecks(Tinkering.Gump.Size) then
    local CurrentPage = 1
    contPos(unpack(Tinkering.Gump.contPos))
    Mouse:LeftClick(unpack(Tinkering.Gump.Menu_Tools)) -- ::Tools
    while CurrentPage < Tinkering.Gump.Menu_Shovel.Page do
      FindGumpLoop({Size = Tinkering.Gump.Size})
      contPos(unpack(Tinkering.Gump.contPos))
      Mouse:LeftClick(unpack(Tinkering.Gump.Menu_NextPage)) -- ::NEXT PAGE
      CurrentPage = CurrentPage + 1
    end
    FindGumpLoop({Size = Tinkering.Gump.Size})
    contPos(unpack(Tinkering.Gump.contPos))
    Mouse:LeftClick(unpack(Tinkering.Gump.Menu_Shovel)) -- ::shovel
    -- The tool might have broken.
    PostCrafting(Tinkering.Gump.Size)
  end
end

local function GetIngotsFromResourcesBag(Amount)
  -- Open Resources Bag.
  nextCPos(0, 470)
  UO.LObjectID = GetIngotBag()
  UOMacro:fn(true, UOMacro.LastObject)
  if FindGumpLoop({ID = GetIngotBag()}) then
    sleep(ScaledMS(1000))
    local IngotsInBag = CountIronIngots(GetIngotBag())
    if IngotsInBag > 0 then
      local Amount = math.min(IngotsInBag, Amount)
      MoveItems(Type.Ingot, GetIngotBag(), UO.BackpackID, ItemType.IRON, Amount)
    end
  end
end

function GetRequiredIngots(Amount)
  local IngotsCount = CountIronIngots(UO.BackpackID)
  if IngotsCount < Amount then
    local Amount = (Amount - IngotsCount) * 5
    GetIngotsFromResourcesBag(Amount)
  end
  return CountIronIngots(UO.BackpackID) >= Amount
end

function Tinkering.LoadTools()
  if not Config.Tinkering then
    return false
  end
  local TinkeringTools = CountItem(Type.TinkerTool, UO.BackpackID)
  if TinkeringTools == 0 then
    if CountItem(Type.TinkerTool, BankBox.ID) > 0 then
      MoveItem(Type.TinkerTool, BankBox.ID, UO.BackpackID)
      TinkeringTool()
      return true
    end
  else
    if TinkeringTools < Config.CraftingToolsInBackPack then
      if GetRequiredIngots(2) then
        CraftTinkeringTool()
        return true
      end
    end
    if Mining:isLoaded() and UO.GetSkill("Tinkering") >= 500 then
      if CountItem(Type.MiningTools, UO.BackpackID) < Config.ToolsInBackPack then
        if GetRequiredIngots(4) then
          CraftMiningTool()
          return true
        end
      end
    end
    if CountItem(Type.TinkerTool, BankBox.ID) < 3 then
      if TinkeringTools > Config.CraftingToolsInBackPack then
        IgnoreItem.Local:this(Char.TinkeringTool)
        MoveItem(Type.TinkerTool, UO.BackpackID, BankBox.ID)
        IgnoreItem.Local:Reset()
        return true
      elseif GetRequiredIngots(2) then
        CraftTinkeringTool()
        return true
      end
    end
  end
  return false
end

function Tinkering.PostBank()
  MoveToolstoBank()
end

function Tinkering.CheckSkills()
  if not Config.Tinkering then
    return
  end
  if UO.GetSkill("Tinkering") < 300 then
    UO.SysMessage("Tinkering disabled due to low skill.", 5110)
    Config.Tinkering = false
  else
    Bot.Tools = table.join(Bot.Tools, Type.TinkerTool)
  end
end

function Tinkering.GetTask()
  if not Config.Tinkering then
    return
  end
  if CountItem(Type.TinkerTool, UO.BackpackID) == 0 then
    Bot.Task = {"Bank"}
  elseif CountItem(Type.TinkerTool, UO.BackpackID) < Config.CraftingToolsInBackPack and
      CountIronIngots(UO.BackpackID) >= 2 then
    Bot.Task = {"TinkerTinkeringTool", "StandStill"}
  elseif CountItem(Type.MiningTools, UO.BackpackID) == 0 and UO.GetSkill("Tinkering") >= 500 and
      CountIronIngots(UO.BackpackID) >= 4 and HarvestTask == "Mine" then
    Bot.Task = {"TinkerMiningTool", "StandStill"}
  end
end

function TinkerMiningTool()
  CraftMiningTool()
  Char:setTaskDone(true)
end

function TinkerTinkeringTool()
  CraftTinkeringTool()
  Char:setTaskDone(true)
end
