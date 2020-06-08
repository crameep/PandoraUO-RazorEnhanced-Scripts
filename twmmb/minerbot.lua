-- ;==================================
-- ; Script Name: WalkingMumblingMinerBot
-- ; Author: Antipatiko
-- ; Version: 2.3 (Legacy) BETA
-- ; Client Tested with: 7.0.85.15
-- ; OEUO version tested with: 0.91
-- ; Shard OSI / FS: OSI & Free Shards
-- ; Revision Date: 5/14/2020
-- ; Public Release: 4/2/2014
-- ; Purpose: Fully autonomous miner, who appears to be intelligent in actions and answers.
-- ;==================================

-- ---------------------------
-- :: Init Package.
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
local P = {}
TWMMB = P
-- inheritance
setmetatable(P, {__index = _G})
setfenv(1, P)
_env = getfenv()
Bot = {}

OpenEUOLua = false

-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- !! !! DEBUG TOGGLE !! !! !!
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Debug = { Enabled = true }
Debug.Callbacks = false
Debug.CheckContext = false
Debug.FileConversion = false
Debug.FindItem = false
Debug.Gumps = false
Debug.IgnoreHits = false
Debug.Inventory = false
Debug.Journal = false
Debug.Modules = false
Debug.Mount = false
Debug.UOMacro = false
Debug.Pathfind = false
Debug.RailPicker = true
Debug.RailWriter = false
Debug.ShardGumps = false
Debug.Sleeps = false
Debug.Targets = false
Debug.Timers = false
-- Behavior alterning:
Debug.FakeMaxWeight = false
Debug.ForceHiding = false
Debug.IgnoreCliLogged = false

function dbg_print(s)
  if Debug.Enabled then
    print(s)
  end
end

function dbg_ifprint(condition, s)
  if Debug.Enabled and condition then
    print(s)
  end
end

-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- !! DON'T TOUCH ANYTHING !! !!
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SEC_TO_MSEC = 1000
MIN_TO_SEC = 60
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- !! DON'T TOUCH ANYTHING !! !!
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
RESOURCE_REPLENISH_MIN_MS = 10 * MIN_TO_SEC * SEC_TO_MSEC
RESOURCE_REPLENISH_MAX_MS = 20 * MIN_TO_SEC * SEC_TO_MSEC
WORLD_SAVE_TIMEOUT = 55 * SEC_TO_MSEC
CONTEXT_GRANULARITY = 150
DISTANCE_TO_CHARS = 4
AMOUNT_MAX = 65535
PATH_PRE = ""

-------------------------------------------------------------------------
-- :: Load Libraries.
-------------------------------------------------------------------------
dofile(getbasedir()..'include.lua')
dofile(getbasedir()..'libtwmmb.lua')

-- ---------------------------
-- # CFG variables
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Bot.FileName = IntToSys26(UO.CharID) .. string.sub(UO.Shard, 0, 2)
Bot.cfgName = Bot.FileName .. ".cfg"
Bot.cfgVer = 3

function Display(MSG)
  if OpenEUOLua then
    print(MSG)
  else
    local DisplayBox = Obj.Create("TMessageBox")
    DisplayBox.Button, DisplayBox.Icon = 0, 4
    DisplayBox.Show(MSG)
  end
end

-- ---------------------------
-- % ErrorHandling
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- Halt program and bring up an error message.
-- %1 = Word #1 of error message
-- %n = Word #n of error message
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function ErrorHandling(ErrorStatement)
  if not ErrorStatement then
    Display("Unknown error.\nPlease log out, log in and restart \n\nReport this error @ TWMMB thread.\nProgram execution stopped.")
    stop()
  else
    Display("The following error happened:\n\n" .. ErrorStatement .. "\n\nIf you consider this a bug, please report it.\nProgram execution stopped.")
    stop()
  end
end

-- -----------------------------------------
-- :: Check if user is logged on, else halt.
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~--------------
if not (UO.CliLogged or Debug.IgnoreCliLogged) then
  ErrorHandling("Please login to Ultima Online first!")
end

-- ---------------------------
-- # Localization Strings
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
CliLoc = {
  BandagesBarelyHelp = "You apply the bandages, but they barely help.",
  Bank = "Bank container has %d+ items, %d+ stones",
  BankSphere = "You have %d+ stones in your Bank Box",
  CannotBeSeen = "Target cannot be seen.",
  CannotBeInspected = "That cannot be inspected.",
  CanNotPickThat = "You can not pick that up",
  DestroyedItem = "You destroyed the item :",
  FinishApplyingBandages = "You finish applying the bandages.",
  GuardZone = "You are now under the protection of the town guards",
  IgnoringActionRequest = "Ignoring action request",
  IsAttackingYou = "is attacking you",
  MustWaitFor = "You must wait to perform another action",
  NoGuardZone = "You have left the protection of the town guards",
  Ping = "Min:.+Max:.+Avg:.+",
  StrengthChanged = "Your strength has changed",
  TooFarAway = "That is too far away",
  TooFatigued = "You are too fatigued to move",
  TryingToStealFrom = "trying to steal from",
  WornOutTool = "You have worn out your tool!",
  YouCantRiding = "You can't .+ while riding or flying."
}

-- ---------------------------
-- # Item Types
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Type = {
  Bandage = {3617},
  Corpse = {3791},
  ElfRace = {Male = 605, Female = 606},
  GargoyleRace = {Male = 666, Female = 667},
  HumanRace = {Male = 400, Female = 401}
}
Type.Races = table.join(table.getValues(Type.HumanRace), table.getValues(Type.ElfRace), table.getValues(Type.GargoyleRace))

ItemType = {
  ALL = 0,
  IRON = 1,
  COLORED = 2
}

-- ---------------------------
-- :: Show init message.
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
UO.ExMsg(UO.CharID, 3, 256, "System initializing. Please standby.")

Bot.ActionDelayDelta = -1
Bot.DelayBase = 1000
Bot.Guards = false
Bot.GuardYellCounter = 0
Bot.JournalEntry = nil
Bot.LastContextCheck = -1
Bot.MustWaitPenalty = 0
Bot.ScriptStarted = false
Bot.Task = {}
Bot.Tools = {}

function sleep(ms)
  local ms = ms or 15
  dbg_ifprint(Debug.Sleeps, ("sleep() -> %d ms."):format(ms))
  wait(ms)
end

function ScaledMS(ms)
  return ms + (Bot.MustWaitPenalty * 100)
end

-- ---------------------------
-- ;;; Timer functions
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Timer = {}

function Timer:Set(ms)
  return getticks() + ms
end

function Timer:Wait(ms)
  local ticks = getticks()
  if ticks < ms then
    local to_wait = ms - ticks
    dbg_ifprint(Debug.Timers, ("Timer:Wait() -> Delta: %d ms."):format(to_wait))
    wait(ScaledMS(to_wait))
  end
end

function Timer:CheckExpired(expires)
  if getticks() < expires then
    return false
  else
    return true
  end
end

function ActionDelaySet(delta)
  local delta = delta or Bot.DelayBase
  delta = Timer:Set(delta)
  if delta > Bot.ActionDelayDelta then
    Bot.ActionDelayDelta = delta
  end
end

function ActionDelay()
  Timer:Wait(Bot.ActionDelayDelta)
  -- Always perform this check after significant sleeps.
  CheckContext()
end

function contPos(x, y)
  while (UO.ContPosX ~= x or UO.ContPosY ~= y) do
    UO.ContPosX = x
    UO.ContPosY = y
    sleep()
  end
end

-- ---------------------------
-- ;;; IgnoreItem functions
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
IgnoreItem = {
  Ignored = {}
}

function IgnoreItem:this(item)
  dbg_print(("IgnoreItem:this() -> Adding item '%d' to global ignore list."):format(item))
  table.fast_insert(IgnoreItem.Ignored, item)
end

function IgnoreItem:Reset()
  IgnoreItem.Ignored = {}
end

function IgnoreItem:Ignoring(item)
  return table.match(IgnoreItem.Ignored, item)
end

IgnoreItem.Local = {
  Ignored = {}
}

function IgnoreItem.Local:this(entity)
  table.fast_insert(IgnoreItem.Local.Ignored, entity)
end

function IgnoreItem.Local:Reset()
  IgnoreItem.Local.Ignored = {}
end

function IgnoreItem.Local:Ignoring(entity)
  return table.match(IgnoreItem.Local.Ignored, entity)
end

-- ---------------------------
-- ;;; IDType
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
IDType = {
  isID = 0,
  isType = 1
}

function IDType:fn(object)
  if string.len(object) <= 5 then
    return IDType.isType
  else
    return IDType.isID
  end
end

function ApplyRules()
  if ShardFeatures:Get(ShardFeatures.OSIShard) then
    OSIShardQuirks()
  elseif ShardFeatures:Get(ShardFeatures.SphereEmu) then
    SphereServerQuirks()
  end
  Char:isHumanRace()
  Char:CarryCapacity()
end

-- ---------------------------
-- ;;; UOMacro
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
UOMacro = {
  Empty = 0,
  Say = 1,
  Open = 8,
  Close = 9,
  Minimize = 10,
  UseSkill = 13,
  LastSkill = 14,
  CastSpell = 15,
  LastObject = 17,
  LastTarget = 22,
  TargetSelf = 23,
  CloseGumps = 31
}

UOMacro.e8 = {
  Configuration = 0,
  Paperdoll = 1,
  Status = 2,
  Journal = 3,
  Skills = 4,
  Spellbook = 5,
  Chat = 6,
  Backpack = 7,
  Overview = 8,
  PartyManifest = 10,
  NecroSpellbook = 12,
  PaladinSpellbook = 13,
  CombatBook = 14,
  BushidoSpellbook = 15,
  NinjutsuSpellbook = 16,
  Guild = 17,
  SpellweavingSpellBook = 18,
  Questlog = 19
}

function UOMacro.__fn(SetDelay, Param1, Param2, Param3)
  local Param2 = Param2 or 0
  local Param3 = Param3 or 0
  dbg_ifprint(Debug.UOMacro, ("UOMacro() -> Param1 = %d, Param2 = %d, Param3 = %d"):format(Param1, Param2, Param3))
  if Param3 == 0 then
    UO.Macro(Param1, Param2)
  else
    UO.Macro(Param1, Param2, Param3)
  end
  if SetDelay then
    ActionDelaySet(1000)
  end
end

function UOMacro:fn(SetDelay, Param1, Param2, Param3)
  ActionDelay()
  UOMacro.__fn(SetDelay, Param1, Param2, Param3)
end

function SendMessage(MSG)
  UO.Msg(MSG .. string.char(13))
end

-- ---------------------------
-- ;;; Mouse functions
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mouse = {}

function Mouse:LeftClick(ScreenX, ScreenY)
  UO.Click(ScreenX, ScreenY, true, true, true, false)
end

function Mouse:RightClick(ScreenX, ScreenY)
  UO.Click(ScreenX, ScreenY, false, true, true, false)
end

function FindShardGump(ContName, ContSizeX, ContSizeY)
  if ContName == "generic gump" and ContSizeX == 480 and ContSizeY == 360 then
    contPos(250, 150)
    Mouse:LeftClick(275, 490)
    return true
  end
  local Shard = UO.Shard
  if "Ultima Forever" == Shard then
    if ContName == "generic gump" and ContSizeX == 328 and ContSizeY == 189 then
      contPos(250, 200)
      Mouse:LeftClick(525, 318)
      return true
    end
  elseif "UOGamers" == Shard then
    if ContName == "generic gump" and ContSizeX == 379 and ContSizeY == 178 then
      contPos(250, 150)
      Mouse:LeftClick(575, 252)
      return true
    elseif ContName == "generic gump" and ContSizeX == 370 and ContSizeY == 240 then
      contPos(15, 385)
      Mouse:RightClick(220, 555)
      return true
    end
  end
  -- Unhandled cont!
  return false
end

function KnownGump(ContName, ContSizeX, ContSizeY)
  if ContName == "container gump" and ContSizeX == 230 and ContSizeY == 204 then
    return true
  elseif ContName == "status gump" and ContSizeX == 584 and ContSizeY == 216 then
    return true
  elseif ContName == "status gump" and ContSizeX == 432 and ContSizeY == 184 then
    return true
  elseif ContName == "normal gump" and ContSizeX == 11 and ContSizeY == 21 then
    return true
  elseif ContName == "paperdoll gump" and ContSizeX == 262 and ContSizeY == 324 then
    return true
  elseif ContName == "text gump" and ContSizeX == 304 and ContSizeY == 300 then
    return true
  else
    return false
  end
end

function FindGump(data)
  local idx = 0
  repeat
    local ContName, ScreenX, ScreenY, ContSizeX, ContSizeY, ContKind, ContID, ContType = UO.GetCont(idx)
    if ContName then
      dbg_ifprint(Debug.Gumps, ("FindGump() -> ContName: %s (idx = %d)"):format(ContName, idx))
      dbg_ifprint(Debug.Gumps, ("FindGump() -> ContID: %d; ContType: %d; ContKind: %d"):format(ContID, ContType, ContKind))
      dbg_ifprint(Debug.Gumps, ("FindGump() -> ContSizeX: %d; ContSizeY: %d"):format(ContSizeX, ContSizeY))
      dbg_ifprint(Debug.Gumps, ("FindGump() -> ScreenX: %d; ScreenY: %d"):format(ScreenX, ScreenY))
      if (not data.Name or data.Name == ContName) and (not data.Pos or data.Pos[1] == ScreenX and data.Pos[2] == ScreenY) and 
          (not data.Size or data.Size[1] == ContSizeX and data.Size[2] == ContSizeY) and (not data.Kind or data.Kind == ContKind) and 
          (not data.ID or data.ID == ContID) and (not data.Type or data.Type == ContType) then
        UO.ContTop(idx)
        return true
      end
    end
    idx = idx + 1
  until (not ContName)
  return false
end

function FindGumpLoop(data)
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  repeat
    sleep()
    CheckContext()
    if FindGump(data) == true then
      return true
    end
  until getticks() > Timeout
  return false
end

function GetGumps()
  local idx = 0
  repeat
    local ContName, ScreenX, ScreenY, ContSizeX, ContSizeY, ContKind = UO.GetCont (idx)
    if ContName and not KnownGump(ContName, ContSizeX, ContSizeY) then
      UO.ContTop(idx)
      if Debug.ShardGumps and not FindShardGump(ContName, ContSizeX, ContSizeY) then
        dbg_print(("GetGumps() -> ContName: %s; ContSizeX: %d; ContSizeY: %d"):format(ContName, ContSizeX, ContSizeY))
        dbg_print(("GetGumps() -> ScreenX: %d; ScreenY: %d; ContKind: %d"):format(ScreenX, ScreenY, ContKind))
      end
    end
    idx = idx + 1
  until (not ContName)
end

function CheckContext()
  if not Bot.ScriptStarted then
    dbg_ifprint(Debug.CheckContext, "Skipping CheckContext() as script hasn't started!")
    return
  end
  if getticks() - Bot.LastContextCheck > CONTEXT_GRANULARITY then
    dbg_ifprint(Debug.CheckContext, ("Checking Context right now! Last check was %d ms. ago"):format((getticks() - Bot.LastContextCheck)))
    -- Disconnected:
    if not UO.CliLogged then
      stop()
    end
    local ContName = UO.ContName
    local ContSizeX = UO.ContSizeX
    local ContSizeY = UO.ContSizeY
    -- Resurrection gump:
    if (ContSizeX == 400) and (ContSizeY == 350) then
      contPos(250, 150)
      Mouse:LeftClick(333, 388) -- ::CONTINUE
    end
    -- Report Murderer gump:
    if (ContSizeX == 626) and (ContSizeY == 532) then
      contPos(50, 50)
      Mouse:LeftClick(325, 360) -- ::Yes
    end
    -- Connection lost gump:
    if (ContSizeX == 203) and (ContSizeY == 121) and (ContName == "waiting gump") then
      stop()
    end
    -- Main Menu gump:
    if (ContSizeX == 640) and (ContSizeY == 480) and (ContName == "MainMenu gump") then
      stop()
    end
    -- Shard gumps:
    FindShardGump(ContName, ContSizeX, ContSizeY)
    -- We're dead. :(
    if Char:Ghost() then
      ErrorHandling("Your character is DEAD. Unable to continue.")
    end
    while Bot.CheckContextJindex < Journal:EntryCount() do
      Bot.CheckContextJindex = Bot.CheckContextJindex + 1
      local Entry = Journal:getEntry(Bot.CheckContextJindex)
      if Entry:match(CliLoc.IsAttackingYou) then
        Char.UnderAttack = true
      elseif Entry:match(CliLoc.StrengthChanged) then
        Char:CarryCapacity()
      elseif Entry:match(CliLoc.TooFatigued) then
        ShardFeatures:Clear(ShardFeatures.HumanStrongBack)
        Char:CarryCapacity()
      elseif Entry:match(CliLoc.TryingToStealFrom) then
        Char.BeingStolen = true
      end
    end
    if Char.UnderAttack or Char.BeingStolen or Char:HasLowHP() then
      if Bot.Guards and (Bot.GuardYellCounter < 4) then
        SendMessage("Guards!")
        Bot.GuardYellCounter = Bot.GuardYellCounter + 1
      end
    end
    Bot.LastContextCheck = getticks()
  end
end

function nextCPos(x, y)
  UO.NextCPosX = x
  UO.NextCPosY = y
end

function GetIngotBag()
  if not Config.IngotBag then
    return BankBox.ID
  else
    return Config.IngotBag
  end
end

-- ---------------------------
-- ;;; BankBox
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
BankBox = {
  ID = nil,
  ItemsStored = 0
}

function BankBox:CountItems()
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  while getticks() < Timeout do
    sleep()
    CheckContext()
    if Journal:FindEntry(CliLoc.Bank) or Journal:FindEntry(CliLoc.BankSphere) then
      local Entry = Journal:getEntry(Bot.JournalIndex)
      local ItemsStored = tonumber(Entry:match("%d+"))
      if ItemsStored then
        BankBox.ItemsStored = ItemsStored
        dbg_print(("BankBox.CountItems() -> Bank has %d items stored."):format(BankBox.ItemsStored))
      end
      return
    end
  end
end

function BankBox:Open()
  CheckContext()
  if UO.ContID == BankBox.ID then
    return true
  end
  nextCPos(0, 228)
  if RAIL:TID(Char.rail) == 0 then
    Bot.JournalIndex = Journal:EntryCount()
    SendMessage("bank")
    BankBox.CountItems()
    Bot.Guards = true
  else
    FindItem:Ground()
    FindItem:ID({RAIL[Char.rail].TID})
    if FindItem.Count == 0 then
      ErrorHandling("Unable to find your Secure Box.")
    end
    UO.LObjectID = FindItem.Item[FindItem.Index].ID
    UOMacro:fn(true, UOMacro.LastObject)
  end
  if FindGumpLoop({Name = "container gump", Size = {180, 240}, Pos = {0, 228}}) then
    BankBox.ID = UO.ContID
    if not (Config.IngotBag and Bot.ScriptStarted) then
      return true
    end
    sleep(ScaledMS(1000))
    FindItem:Cont(BankBox.ID)
    FindItem:ID({IngotBag()})
    if FindItem.Count == 0 then
      ErrorHandling("Fatal error: unable to find your Ingot Bag!")
    else
      return true
    end
  end
  -- Could not open Bank Box.
  return false
end

function CountItem(Types, Container)
  FindItem:Cont(Container)
  FindItem:Type(Types)
  return FindItem.Count
end

function CountStack(Types, Container, IRON_only)
  local IRON_only = IRON_only or false
  local cnt = 0
  FindItem:Cont(Container)
  FindItem:Type(Types)
  if FindItem.Count > 0 then
    for i = 1, FindItem.Count do
      if not IRON_only or FindItem.Item[i].Col == 0 then
        cnt = cnt + FindItem.Item[i].Stack
      end
    end
  end
  return cnt
end

function DragItem(Item, Amount)
  local Amount = Amount or 1
  ActionDelay()
  UO.Drag(Item, Amount)
  ActionDelaySet()
  ActionDelay()
end

-- ---------------------------
-- ;;; DropItem
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
DropItem = {}

function DropItem:Cont(ContID)
  UO.DropC (ContID)
  ActionDelaySet()
  ActionDelay()
end

function DropItem:Ground(x, y, z)
  local z = z or UO.CharPosZ
  UO.DropG(x, y, z)
  ActionDelaySet()
  ActionDelay()
end

function DropItem:RandomGroundOnce()
  local Random = {}
  while (true) do
    -- First random coordinate.
    Random.x = math.random(0, 999) % 3
    if math.random(0, 999) % 100 >= 50 then
      Random.x = Random.x * -1
    end
    -- Second random coordinate.
    Random.y = math.random(0, 999) % 3
    if math.random(0, 999) % 100 >= 50 then
      Random.y = Random.y * -1
    end
    -- Both coords can't be zero.
    if Random.x ~= 0 or Random.y ~= 0 then
      break
    end
  end
  local Coord = {x = UO.CharPosX + Random.x, y = UO.CharPosY + Random.y}
  DropItem:Ground(Coord.x, Coord.y)
end


--[[
    DropItem:RandomGround()
    Drop an item on the ground near the character (never at its feet).
--]]
function DropItem:RandomGround()
  for i = 1, 3 do
    DropItem:RandomGroundOnce()
  end
end

function DropItem:Paperdoll()
  UO.DropPD()
  ActionDelaySet()
  ActionDelay()
end

function CraftChecks(GumpSize)
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  repeat
    sleep()
    if FindGump({Size = GumpSize}) then
      return true
    elseif Journal:FindEntry(CliLoc.MustWaitFor) then
      return false
    end
  until getticks() > Timeout
  return false
end

local function FindPostCraftingGump (GumpSize)
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  repeat
    sleep()
    CheckContext()
    if Journal:FindEntry(CliLoc.WornOutTool) then
      return true
    elseif FindGump({Size = GumpSize}) then
      contPos(250, 150)
      Mouse:RightClick(640, 320) -- Close gump.
      return true
    end
  until getticks() > Timeout
  return false
end

function PostCrafting(GumpSize)
  if FindPostCraftingGump (GumpSize) then
    ActionDelaySet()
    ActionDelay()
  end
end

function FindTool(Current, ToolType, Panic)
  local Panic = Panic or true
  FindItem:Cont(UO.BackpackID)
  FindItem:Type(ToolType)
  if FindItem.Count == 0 then
    if Panic then
      ErrorHandling("Unable to find tools type: " .. table.concat(ToolType, "; "))
    end
    return
  end
  local Tool = nil
  for i = 1, FindItem.Count do
    Tool = FindItem.Item[i].ID
    if not Current or Tool == Current then
      break
    end
  end
  return Tool
end

function UODistance(Point_A, Point_B)
  return math.max(math.abs(Point_A.x - Point_B.x), math.abs(Point_A.y - Point_B.y))
end

function RailDistance(rail_A, rail_B)
  dbg_ifprint(Debug.RailPicker, ("RailDistance() -> Starting rail: %d"):format(rail_A))
  dbg_ifprint(Debug.RailPicker, ("RailDistance() -> Ending rail: %d"):format(rail_B))
  dbg_ifprint(Debug.RailPicker, ("RailDistance() -> Raw distance: %d"):format(Rail:Distance(rail_A, rail_B)))
  if rail_A > rail_B then
    rail_A, rail_B = swap(rail_A, rail_B)
  end
  local Distance = 0
  while rail_A < rail_B do
    Distance = Distance + Rail:Distance(rail_A, rail_A + 1)
    rail_A = rail_A + 1
  end
  dbg_ifprint(Debug.RailPicker, ("RailDistance() -> Accumulated distance: %d"):format(Distance))
  dbg_ifprint(Debug.RailPicker, ("RailDistance() -> DONE"))
  return Distance
end

local function getDirection(r)
  local Direction = "+"
  if Char.rail > r then
    Direction = "-"
  end
  dbg_print(("getDirection() -> Current: %s; Suggested: %s; r_0=%d; r_1=%d"):format(Char.Direction, Direction, Char.rail, r))
  return Direction
end

function ClosestRail(Task)
  dbg_print(("ClosestRail() -> Trying to find a rail for '%s' task."):format(Task))
  local rail, LastDistance
  for r = 1, RAIL:count() do
    if RAIL:A(r) == Task and Rail:Available(r) then
      local Distance = RailDistance(Char.rail, r)
      if not LastDistance or Distance < LastDistance then
        LastDistance = Distance
        rail = r
      end
    end
  end
  if rail == nil then
    ErrorHandling(("Unable to find a rail for '%s' task."):format(Task))
  end
  local Direction = getDirection(rail)
  dbg_print(("ClosestRail() -> %d (Direction: %s)"):format(rail, Direction))
  return rail, Direction
end

function CheckStamina()
  while UO.Stamina == 0 do
    CheckContext()
    if math.random(0, 999) % 10 == 0 then
      Char:Print("Low stamina!", 16)
    end
    sleep(1000)
  end
end

-- --------------------------
-- ;;; Rail functions
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~
Rail = {
  A = {},
  x = {},
  y = {},
  z = {},
  Tx = {},
  Ty = {},
  Tz = {},
  Tkind = {},
  Ttile = {},
  TID = {},
  EndSpot = 0
}

RAIL = {}

function RAIL:InsertSpot(S)
  RAIL[S] = {}
  RAIL[S].A      =  Rail.A[S]
  RAIL[S].x      =  Rail.x[S]
  RAIL[S].y      =  Rail.y[S]
  RAIL[S].z      =  Rail.z[S]
  RAIL[S].Tx     =  Rail.Tx[S]
  RAIL[S].Ty     =  Rail.Ty[S]
  RAIL[S].Tz     =  Rail.Tz[S]
  RAIL[S].Tkind  =  Rail.Tkind[S]
  RAIL[S].Ttile  =  Rail.Ttile[S]
  RAIL[S].TID    =  Rail.TID[S]
  -- Runtime fields:
--RAIL[S].Pathfind  =  false
--RAIL[S].Skip      =  false
--RAIL[S].Ignore_timer = nil
--RAIL[S].LastDry      = nil
end

function RAIL:count()
  return #RAIL
end

function RAIL:skip(r)
  if RAIL[r].Skip == nil then
    return false
  else
    return true
  end
end

function RAIL:A(r)
  if r == 0 then
    return "StandStill"
  else
    return RAIL[r].A
  end
end

function RAIL:TID(r)
  if r == 0 then
    return 0
  else
    return RAIL[r].TID
  end
end

function Rail:Set(r)
  Char.rail = r
  Char.A = RAIL[r].A
  Char.x = RAIL[r].x
  Char.y = RAIL[r].y
  Char.z = RAIL[r].z
  dbg_print(("Rail:Set() -> %d"):format(r))
  Char:SetDirection()
end

function Rail:SetSkip()
  dbg_print(("Rail:SetSkip() -> Rail #%d will be skipped."):format(Char.rail))
  RAIL[Char.rail].Skip = true
end

function Rail:Ignore(r, t)
  dbg_print(("Rail:Ignore() -> Ignoring rail #%d for %d seconds."):format(r, (t / 1000)))
  RAIL[r].Ignore_timer = getticks() + t
end

function Rail:Available(r)
  local Ignore_timer = RAIL[r].Ignore_timer or 0
  return getticks() > Ignore_timer and (not RAIL:skip(r))
end

function Rail:Pos(r)
  return {x = RAIL[r].x, y = RAIL[r].y}
end

function Rail:getNext(r)
  if Char.Direction == "+" then
    return r + 1
  else
    return r - 1
  end
end

function Rail:inPath(a, b)
  return RAIL[a].x == RAIL[b].x or RAIL[a].y == RAIL[b].y
end

function Rail:Distance(a, b)
  return UODistance(Rail:Pos(a), Rail:Pos(b))
end

function Rail:SetPathfind(r)
  dbg_print(("Rail:SetPathfind() -> rail: %d"):format(r))
  RAIL[r].Pathfind = true
end

function Rail:ClearPathfind(r)
  dbg_print(("Rail:ClearPathfind() -> rail: %d"):format(r))
  RAIL[r].Pathfind = false
end

function Rail:save()
  local Railpath = PATH_PRE .. "Rails\\" .. string.lower(Config.Rail)
  print(("INFO: Saving Rail -> %s"):format(tostring(Railpath)))
  local OEUO_Rail, e = openfile(Railpath, "w")
  if not OEUO_Rail then
    ErrorHandling("Couldn't open a new file for writing!")
  end
  for r = 1, Rail.EndSpot do
    OEUO_Rail:write(("TWMMB.Rail.A[%d] = \"%s\"\n"):format(r, Rail.A[r]))
    OEUO_Rail:write(("TWMMB.Rail.x[%d] = %d\n"):format(r, Rail.x[r]))
    OEUO_Rail:write(("TWMMB.Rail.y[%d] = %d\n"):format(r, Rail.y[r]))
    OEUO_Rail:write(("TWMMB.Rail.z[%d] = %d\n"):format(r, Rail.z[r]))
    OEUO_Rail:write(("TWMMB.Rail.Tx[%d] = %d\n"):format(r, Rail.Tx[r]))
    OEUO_Rail:write(("TWMMB.Rail.Ty[%d] = %d\n"):format(r, Rail.Ty[r]))
    OEUO_Rail:write(("TWMMB.Rail.Tz[%d] = %d\n"):format(r, Rail.Tz[r]))
    OEUO_Rail:write(("TWMMB.Rail.Tkind[%d] = %d\n"):format(r, Rail.Tkind[r]))
    OEUO_Rail:write(("TWMMB.Rail.Ttile[%d] = %d\n"):format(r, Rail.Ttile[r]))
    OEUO_Rail:write(("TWMMB.Rail.TID[%d] = %d\n"):format(r, Rail.TID[r]))
  end
  OEUO_Rail:write(("TWMMB.Rail.EndSpot = %d"):format(Rail.EndSpot))
  OEUO_Rail:flush()
  OEUO_Rail:close()
end

Rail.convert_KeystoIgnore = {
  "endspot",
  "Guard",
  "TID",
  "TWMMBrailcfgVer"
}

function Rail:convert()
  local EUO_Railpath = PATH_PRE .. string.lower(Config.Rail)
  local EUO_rail, e = openfile(EUO_Railpath, "r")
  if not EUO_rail then
    ErrorHandling(("Couldn't open old format (EasyUO) rail: %s"):format(EUO_Railpath))
  end
  local line_number = 0
  for line in EUO_rail:lines() do
    line_number = line_number + 1
    dbg_ifprint(Debug.FileConversion, ("Rail:convert() -> Scanning line: %d"):format(line_number))
    local Key = line:match("%%(%a+)")
    if Key == nil then
      EUO_rail:close()
      ErrorHandling("Fatal error. Unable to continue with rail conversion!")
    end
    dbg_ifprint(Debug.FileConversion, ("Rail:convert() -> Key: %s"):format(Key))
    local Value = line:match("%p%w+%s(.+)")
    if Value == nil then
      EUO_rail:close()
      ErrorHandling("Fatal error. Unable to continue with rail conversion!")
    end
    dbg_ifprint(Debug.FileConversion, ("Rail.convert() -> Value: %s"):format(tostring(Value)))
    if not table.match(Rail.convert_KeystoIgnore, Key) then
      table.insert(Rail[Key], Value)
    end
  end
  Rail.EndSpot = #Rail.A
  EUO_rail:close()
  Rail:save()
  print("Congratulations! Your old rail from EasyUO version has been converted to the new format. Enjoy.")
end

function Rail:Load()
  local Railpath = PATH_PRE .. "Rails\\" .. string.lower(Config.Rail)
  print(("INFO: Loading Rail -> %s"):format(Railpath))
  local OEUO_rail, e = openfile(Railpath, "r")
  if OEUO_rail then
    local s = OEUO_rail:read()
    OEUO_rail:close()
    if s:match("TWMMB\.Rail\.A") then
      dofile(Railpath)
      Rail:newLayout()
      return true
    elseif s:match("%endspot") then
      ErrorHandling(("Rails that haven't been converted to new format must reside in: \"%s\""):format(getbasedir()))
    else
      ErrorHandling(("Couldn't open rail: %s\n\nUnknown file format!\n"):format(Config.Rail))
    end
  end
  local EUO_Railpath = PATH_PRE .. Config.Rail
  local EUO_rail, e = openfile(EUO_Railpath, "r")
  if EUO_rail then
    local s = EUO_rail:read()
    EUO_rail:close()
    if s:match("%endspot") then
      Rail:convert()
      dofile(Railpath)
      return true
    else
      ErrorHandling("Couldn't open rail: " .. Config.Rail .. "\n\nUnknown file format!\n")
    end
  end
  ErrorHandling(("Couldn't open rail: %s\n\nRails must reside in: \"%sRails\\\"" ..
    "\n\nRails that haven't been converted to new format must reside in: \"%s\""):format(Config.Rail, getbasedir(), getbasedir()))
end

function Rail:newLayout()
  for r = 1, Rail.EndSpot do
    RAIL:InsertSpot(r)
  end
  -- Free old tables:
  Rail.A = nil
  Rail.x = nil
  Rail.y = nil
  Rail.z = nil
  Rail.Tx = nil
  Rail.Ty = nil
  Rail.Tz = nil
  Rail.Tkind = nil
  Rail.Ttile = nil
  Rail.TID = nil
  Rail.EndSpot = nil
end

function DropItems(Type, Amount, IRON_only)
  local IRON_only = IRON_only or false
  FindItem:Cont(UO.BackpackID)
  FindItem:Type(Type)
  if FindItem.Count == 0 then
    return
  end
  for i = 1, FindItem.Count do
    if not IRON_only or FindItem.Item[i].Col == 0 then
      local Stack = FindItem.Item[i].Stack
      Stack = math.min(Amount, Stack)
      DragItem(FindItem.Item[i].ID, Stack)
      DropItem:RandomGround()
      Amount = Amount - Stack
      if Amount == 0 then return end
    end
  end
end

function Target(t)
  local Timeout = getticks() + t
  while getticks() < Timeout do
    CheckContext()
    if UO.TargCurs == true then
      return true
    else
      sleep()
    end
  end
  return false
end

-- ---------------------------
-- ;;; Char
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Char = {
  x = UO.CharPosX,
  y = UO.CharPosY,
  z = UO.CharPosZ,
  rail = 0,
  Direction = "+",
  BeingStolen = false,
  isHuman = false,
  Targets = {},
  Task = {},
  NextTask = {},
  UnderAttack = false,
  SkillsTimer = getticks(),
  _TaskDone = true
}

Char.Stats = {
  maxWeight = 0
}

function Char:TaskDone()
  return Char._TaskDone
end

function Char:setTaskDone(bool)
  Char._TaskDone = bool
end

function Char:maxWeight()
  return Char.Stats.maxWeight
end

function Char:BackpackCapacity()
  return Char:maxWeight() - UO.Weight
end

function Char:GetHP()
  return (UO.Hits / UO.MaxHits) * 100
end

function Char:GetPos()
  return {x = UO.CharPosX, y = UO.CharPosY, z = UO.CharPosZ}
end

function Char:GetNextRail()
  if Char.Direction == "+" then
    return Char.rail + 1
  else
    return Char.rail - 1
  end
end

function Char:isHumanRace()
  if UO.CharType == Type.HumanRace.Male or UO.CharType == Type.HumanRace.Female then
    dbg_print("Char:isHumanRace() -> Human race detected.")
    Char.isHuman = true
  else
    dbg_print("Char:isHumanRace() -> Non-human race detected.")
  end
end

function Char:CarryCapacity()
  Char:OpenStatusBar()
  Char.Stats.maxWeight = UO.MaxWeight
  if Char.Stats.maxWeight > 463 then
    Char.Stats.maxWeight = 463
  end
  if Debug.FakeMaxWeight then
    Char.Stats.maxWeight = 236
  elseif ShardFeatures:Get(ShardFeatures.AOSRules) then
    if Char.isHuman and ShardFeatures:Get(ShardFeatures.HumanStrongBack) then
      Char.Stats.maxWeight = Char.Stats.maxWeight + 60
    end
  end
  dbg_print(("Char:CarryCapacity() -> Current max weight: %d"):format(Char.Stats.maxWeight))
end

function Char:getTask()
  return Char.Task[1]
end

function Char:setTask(Task)
  Char.Task = Task
  Char.NextTask = {}
  dbg_print(("Char:setTask() -> %s"):format(table.concat(Char.Task, "; ")))
end

function Char:getNextTask()
  return Char.NextTask
end

function Char:setNextTask(T)
  Char.NextTask = T
end

function Char:clearNextTask()
  Char.NextTask = {}
end

function Char:StandStill()
  return table.match(Char.Task, "StandStill")
end

function Char:Ghost()
  local CharType = UO.CharType
  return CharType == 402 or CharType == 403 or CharType == 607 or CharType == 608 or CharType == 694 or CharType == 695
end

function Char:isHidden()
  return string.match(UO.CharStatus, "H")
end

function Char:Hide()
  if Config.Hiding and Timer:CheckExpired(Char.SkillsTimer) then
    Char:OpenStatusBar()
    if not Char:isHidden() or Debug.ForceHiding then
      Skills:UseHiding()
    end
  end
end

function Char:isPoisoned()
  return string.match(UO.CharStatus, "C")
end

function Char:HasLowHP()
  return (Char:GetHP() < 90 and not Debug.IgnoreHits)
end

function Char:OpenBackpack()
  nextCPos(0, 0)
  UOMacro.__fn(false, UOMacro.Close, UOMacro.e8.Backpack)
  UOMacro:fn(true, UOMacro.Open, UOMacro.e8.Backpack)
  if not FindGumpLoop({Size = {230, 204}}) then
    ErrorHandling("Could not open your backpack.")
  end
end

function Char:OpenStatusBar()
  if UO.Weight ~= 0 then
    return
  end
  UOMacro.__fn(true, UOMacro.Open, UOMacro.e8.Status)
  if not FindGumpLoop({Name = "status gump"}) then
    ErrorHandling("Could not open the status bar!")
  end
  UOMacro:fn(false, UOMacro.Minimize, UOMacro.e8.Status)
  contPos(430, 30)
end

function Char:OpenPaperdoll()
  UOMacro.__fn(false, UOMacro.Open, UOMacro.e8.Paperdoll)
  if not FindGumpLoop({Name = "paperdoll gump"}) then
    ErrorHandling("Could not open your Paperdoll.")
  end
  contPos(850, 20)
end

function Char:ClosePaperdoll()
  UOMacro.__fn(false, UOMacro.Close, UOMacro.e8.Paperdoll)
end

function Char:SetDirection()
  if Char.rail == 1 then
    Char.Direction = "+"
  elseif Char.rail == RAIL:count() then
    Char.Direction = "-"
  end
end

function Char:SwitchDirection()
  dbg_print(("Char:SwitchDirection() -> Switching direction!"))
  if Char.Direction == "+" then
    Char.Direction = "-"
  else
    Char.Direction = "+"
  end
end

function Char:Print(MSG, Color)
  local Color = Color or 256
  UO.ExMsg(UO.CharID, 3, Color, MSG)
end

function HealMe()
  Char.UnderAttack = false
  local Timer = getticks() - 1
  while Char:HasLowHP() do
    CheckContext()
    Char:Hide()
    sleep(1000)
    if getticks() > Timer then
      Char:Print("Low hits!", 16)
      Timer = getticks() + (15 * SEC_TO_MSEC)
    end
  end
  Bot.GuardYellCounter = 0
  Char:setTaskDone(true)
end

--[[
      This is our task engine, which decides what to do...
--]]
function GetTask()
  Bot.Task = {}
  CheckContext()
  Char:OpenStatusBar()
  if Char:Ghost() then
    ErrorHandling("Your character is DEAD. Unable to continue.")
  end
  if Char.UnderAttack or Char:HasLowHP() then
    if not RAIL:A(Char.rail) == "Bank" then
      Bot.Task = {"Bank"}
    else
      Bot.Task = {"HealMe", "StandStill"}
    end
  end
  if #Bot.Task == 0 and UO.Weight > (Char:maxWeight() - 25) then
    Bot.Task = {"Bank"}
    if UO.Weight > Char:maxWeight() then
      Mining.DropOre()
    end
    Mining.GetTask_Overweight()
  end
  if #Bot.Task == 0 then
    Mining.GetTask_Early()
  end
  if #Bot.Task == 0 then
    Bot.Task = {"Bank"}
    Mining.GetTask()
    Tinkering.GetTask()
  end
  dbg_print(("GetTask() -> %s"):format(table.concat(Bot.Task, "; ")))
  return Bot.Task
end

function MoveItems(Type, Source, Destination, ItemsType, Remaining)
  local ItemsType = ItemsType or ItemType.ALL
  local Remaining = Remaining or AMOUNT_MAX
  FindItem:Cont(Source)
  FindItem:Type(Type)
  if FindItem.Count == 0 then
    return
  end
  for i = 1, FindItem.Count do
    local Item = FindItem.Item[i]
    if ItemsType == ItemType.ALL or (ItemsType == ItemType.IRON and Item.Col == 0) or
        (ItemsType == ItemType.COLORED and Item.Col ~= 0) then
      local Amount = math.min(Remaining, Item.Stack)
      DragItem(Item.ID, Amount)
      DropItem:Cont(Destination)
      Remaining = Remaining - Amount
      if Remaining == 0 then break end
    end
  end
end

function MoveItem(Type, Container_from, Container_dest, ItemsType)
  local ItemsType = ItemsType or ItemType.ALL
  MoveItems(Type, Container_from, Container_dest, ItemsType, 1)
end

local function LoadToolsLoop()
  if not BankBox:Open() then
    dbg_print("LoadToolsLoop() -> couldn't open Bank Box!")
    return false
  end
  if Mining.LoadTools() or Tinkering.LoadTools() then
    return true
  else
    return false
  end
end

function LoadTools()
  repeat until not (LoadToolsLoop())
end

function Bank()
  Char.BeingStolen = false
  Char.UnderAttack = false
  Char:OpenBackpack()
  if not BankBox:Open() then
    Rail:SetSkip()
    return
  end
  Char:Hide()
  Mining.atBank()
  LoadTools()
  Mining.PostLoadTools()
  Mining.PostBank()
  Tinkering.PostBank()
  Char:setTaskDone(true)
end

Skills = {
  HIDING = 21
}
function Skills:UseHiding()
  if not Timer:CheckExpired(Char.SkillsTimer) then
    return
  end
  UOMacro:fn(false, UOMacro.UseSkill, Skills.HIDING)
  if ShardFeatures:Get(ShardFeatures.OSIShard) then
    ActionDelaySet(10000)
  end
  Char.SkillsTimer = Timer:Set(ScaledMS(10000))
end

function Relax()
  Mining.Relax()
  Char:setTaskDone(true)
end

function setXYZKT(id, x, y, z, k, t)
  UO.LObjectID = id
  UO.LTargetX = x
  UO.LTargetY = y
  UO.LTargetZ = z
  UO.LTargetKind = k
  UO.LTargetTile = t
end

function CheckGuardsRegion()
  local EntryCount = Journal:EntryCount()
  while (EntryCount > Bot.GuardsRegionJindex) do
    local Entry = Journal:getEntry(EntryCount)
    if Entry:match(CliLoc.GuardZone) then
      dbg_print("CheckGuardsRegion() -> Guards = YES")
      Bot.Guards = true
      break
    elseif Entry:match(CliLoc.NoGuardZone) then
      dbg_print("CheckGuardsRegion() -> Guards = NO")
      Bot.Guards = false
      break
    end
    EntryCount = EntryCount - 1
  end
  Bot.GuardsRegionJindex = Journal:EntryCount()
end

EightEight = {}

function EightEight:Pos(x, y)
  local _x = math.floor (x / 8)
  local _y = math.floor (y / 8)
  return {x = _x, y = _y}
end

function EightEight:CurrPos()
  local _x = math.floor (RAIL[Char.rail].Tx / 8)
  local _y = math.floor (RAIL[Char.rail].Ty / 8)
  return {x = _x, y = _y}
end

function EightEight:eq(A, B)
  return A.x == B.x and A.y == B.y
end

function EightEight:SetDry()
  local Ticks = getticks()
  local EightEight_curr = EightEight:CurrPos()
  dbg_print(("EightEight:SetDry() -> Marking 8x8: {%d, %d} as dry."):format(EightEight_curr.x, EightEight_curr.y))
  for r = 1, RAIL:count() do
    local EightEight_r = EightEight:Pos(RAIL[r].Tx, RAIL[r].Ty)
    if RAIL:A(r) == Char:getTask() and EightEight:eq(EightEight_curr, EightEight_r) then
      dbg_print(("EightEight:SetDry() -> Marking rail #%d as dry."):format(r))
      RAIL[r].LastDry = Ticks
    end
  end
end

local function HarvestRailFindNext()
  local Start = Char:GetNextRail()
  local End = Char.Direction == "+" and RAIL:count() or 1
  local Step = Start > End and -1 or 1
  local Ticks = getticks()
  for r = Start, End, Step do
    if RAIL:A(r) == Char:getTask() and Rail:Available(r) then
      local LastDry = RAIL[r].LastDry or 0
      if (Ticks - LastDry) > RESOURCE_REPLENISH_MIN_MS then
        dbg_print(("HarvestRailFindNext() -> %d"):format(r))
        return r
      end
    end
  end
  dbg_print("HarvestRailFindNext() -> Didn't find any candidate rail in this direction.")
  return
end

function HarvestRailGetNext()
  local Next = HarvestRailFindNext()
  if not (Next or Char.rail == 1 or Char.rail == RAIL:count()) then
    Char:SwitchDirection()
    Next = HarvestRailFindNext()
  end
  return Next
end

function HarvestLoop(x, y, z, k, t, Timeout)
  Bot.JournalIndex = Journal:EntryCount()
  Mining.Harvest(x, y, z, k, t)
  local Task = GetTask()
  local SkipRail = Char:TaskDone()
  Char:setTaskDone(Task[1] ~= Char:getTask())
  if Char:TaskDone() or SkipRail or getticks() > Timeout then
    return false, Task
  end
  if not ShardFeatures:Get(ShardFeatures.AOSRules) then
    Char:Hide()
  end
  -- Loop!!
  return true, Task
end

function Harvest()
  local r = Char.rail
  while (not (UO.CharPosX == RAIL[r].x and UO.CharPosY == RAIL[r].y)) do
    UO.Pathfind(RAIL[r].x, RAIL[r].y, RAIL[r].z)
    sleep(500)
  end
  Char:setTaskDone(false)
  local Tx = RAIL[Char.rail].Tx
  local Ty = RAIL[Char.rail].Ty
  local Tz = RAIL[Char.rail].Tz
  local Tk = RAIL[Char.rail].Tkind
  local Tt = RAIL[Char.rail].Ttile
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  local Task = {}
  local Loop = true
  repeat
    Loop, Task = HarvestLoop(Tx, Ty, Tz, Tk, Tt, Timeout)
  until (not Loop)
  if Char:TaskDone() then
    if not (Task[1] == "Mine") then
      Char.LastHarvestDirection = Char.Direction
      Char.LastHarvestRail = Char.rail
    end
    Char:setNextTask(Task)
    return false
  end
  repeat
    local HarvestRail = HarvestRailGetNext()
    if HarvestRail then
      PathfindLoop(HarvestRail)
    else
      Char:setTaskDone(true)
      Char.LastHarvestDirection = Char.Direction
      Char.LastHarvestRail = Char.rail
      return false
    end
  until RAIL:A(Char.rail) == Char:getTask()
  return true
end

function CloseGumps()
  UOMacro.__fn(false, UOMacro.CloseGumps)
  sleep(100)
end

--[[
    InitScreen()
    Show Welcome message and close all gumps.
--]]
function InitScreen()
  Char:Print("Setting up screen.", 16)
  CloseGumps()
  -- Drop any item on cursor.
  DropItem:Ground(UO.CharPosX, UO.CharPosY)
  Char:OpenBackpack()
  Char:OpenStatusBar()
end

ShardFeatures = {
  OSIShard = 0x1,
  SphereEmu = 0x2,
  AOSRules = 0x4,
  AOSTooltips = 0x8,
  HumanStrongBack = 0x10,
  SmeltOnDblClick = 0x20,
  SmeltDblClickOre = 0x40,
  SmeltDblClickForge = 0x80
}

function ShardFeatures:cfgDefault()
  return 0x50 -- HumanStrongBack, SmeltDblClickOre.
end

function ShardFeatures:AOSDefault()
  return 0xC -- AOSRules, AOSTooltips.
end

function ShardFeatures:SmeltFlags()
  return 0xE0 -- SmeltOnDblClick, SmeltDblClickOre, SmeltDblClickForge.
end

function ShardFeatures:Set(Flag)
  Config.ShardFeatures = Bit.Or (Config.ShardFeatures, Flag)
end

function ShardFeatures:Clear(Flag)
  Config.ShardFeatures = Config.ShardFeatures - Bit.And(Config.ShardFeatures, Flag)
end

function ShardFeatures:Get(Flag)
  return not (Bit.And(Config.ShardFeatures, Flag) == 0)
end

function isOSIShard()
  local OSIShards = {"Atlantic", "Baja", "Catskills", "Chesapeake", "Drachenfels", "Europa", "Great Lakes", "Lake Austin", "Lake Superior",
    "Legends", "Napa Valley", "Oceania", "Origin", "Pacific", "Siege Perilous", "Arirang", "Asuka", "Balhae", "Formosa", "Hokuto", "Izumo", "Mizuho",
    "Sakura", "Sonoma", "Wakoku", "Yamato"}
  return table.match(OSIShards, UO.Shard)
end

function ShardDetection()
  local Shard = UO.Shard
    if "ABC UO" == Shard then
    ShardFeatures:Set(ShardFeatures:AOSDefault())
    -- Has OSI gump size:
    if Tinkering:isLoaded() then
      Tinkering.Gump.Menu_Tools = {275, 280}
      Tinkering.Gump.Size = {530, 497}
    end
    return true
  elseif "DarkDeus" == Shard then
    ShardFeatures:Set(ShardFeatures.SphereEmu)
    ShardFeatures:Clear(ShardFeatures:SmeltFlags())
    ShardFeatures:Set(ShardFeatures.SmeltDblClickForge)
    return true
  elseif "Defiance" == Shard then
    return true
  elseif "Demise - AOS" == Shard then
    ShardFeatures:Set(ShardFeatures:AOSDefault())
    return true
  elseif "Divinity" == Shard then
    return true
  elseif "Forgotten Lands" == Shard then
    ShardFeatures:Set(ShardFeatures.SphereEmu)
    if Mining:isLoaded() then
      Type.MiningTools = {3897, 3898}
    end
    return true
  elseif "Lost Lands" == Shard then
    if Tinkering:isLoaded() then
      Tinkering.Gump.Menu_Tools = {275, 240}
    end
    return true
  elseif "PestilentUO AOS" == Shard then
    ShardFeatures:Set(ShardFeatures:AOSDefault())
    ShardFeatures:Clear(ShardFeatures.HumanStrongBack)
    return true
  elseif "Ultima Forever" == Shard then
    ShardFeatures:Clear(ShardFeatures:SmeltFlags())
    ShardFeatures:Set(ShardFeatures.SmeltOnDblClick)
    if Tinkering:isLoaded() then
      Tinkering.Gump.contPos = {155, 40}
      Tinkering.Gump.Menu_NextPage = {538, 473}
      Tinkering.Gump.Menu_Shovel = {390, 310, Page = 1}
      Tinkering.Gump.Menu_TinkersTools = {390, 170}
      Tinkering.Gump.Menu_Tools = {185, 150}
      Tinkering.Gump.Size = {530, 600}
    end
    return true
  elseif "UnrealUO" == Shard then
    return true
  elseif "UOGamers" == Shard then
    return true
  elseif "UOReckoning" == Shard then
    ShardFeatures:Set(ShardFeatures.SphereEmu)
    if Mining:isLoaded() then
      Mining.OreWeight = 1
    end
    return true
  elseif "UO Evolution" == Shard then
    ShardFeatures:Set(ShardFeatures:AOSDefault())
    -- Has OSI gump size:
    if Tinkering:isLoaded() then
      Tinkering.Gump.Menu_NextPage = {630, 440}
      Tinkering.Gump.Size = {530, 497}
    end
    return true
  elseif "Revelation" == Shard then
    return true
  elseif "SecondAge" == Shard then
    Config.Tinkering = false
    return true
  elseif "Vetus Mundus" == Shard then
    ShardFeatures:Set(ShardFeatures:AOSDefault())
    if Tinkering:isLoaded() then
      Tinkering.Gump.Menu_Shovel = {480, 240, Page = 2}
    end
    return true
  elseif "World of UO" == Shard then
    ShardFeatures:Set(ShardFeatures:AOSDefault())
    -- Has OSI gump size:
    if Tinkering:isLoaded() then
      Tinkering.Gump.Menu_Tools = {275, 280}
      Tinkering.Gump.Size = {530, 497}
    end
    return true
  elseif "In Por Ylem" == Shard then
    return true
  else
    return false
  end
end

function OSIShardQuirks()
  ShardFeatures:Set(ShardFeatures:AOSDefault())
  ShardFeatures:Set(ShardFeatures.HumanStrongBack)
  ShardFeatures:Clear(ShardFeatures:SmeltFlags())
  ShardFeatures:Set(ShardFeatures.SmeltDblClickOre)
  if Tinkering:isLoaded() then
    Tinkering.Gump.Menu_Tools = {275, 280}
    Tinkering.Gump.Size = {530, 497}
  end
end

function SphereServerQuirks()
  if not ShardFeatures:Get(ShardFeatures.SmeltDblClickOre) and
      not ShardFeatures:Get(ShardFeatures.SmeltDblClickForge) then
    ShardFeatures:Set(ShardFeatures.SmeltOnDblClick)
  end
  Config.Hiding = false
  Config.Tinkering = false
  Config.ToolsInBackPack = 1
  if Mining:isLoaded() then
    Type.MiningTools = {3897}
  end
end

--[[
    DetectShard()
    Rules:
    - Default is AOS.
    - OSI is always AOS.
    - SphereServer is never AOS.
    - RunUO vary but can be easily detected.
--]]
function DetectShard()
  -- OSI detection.
  if isOSIShard() then
    UO.SysMessage("INFO: OSI server detected.", 5110)
    ShardFeatures:Set(ShardFeatures.OSIShard)
  -- Free shard detection & quirks.
  elseif ShardDetection() then
    UO.SysMessage("Notice: Behaviour adjusted for this shard. If you experience any problem please fill in a bug report.", 5110)
  -- SphereServer detection.
  elseif UO.MaxHits == UO.Str and (UO.MaxStats == 235 or UO.MaxStats == 300) then
    UO.SysMessage("INFO: SphereServer emulator detected. If this is incorrect please fill in a bug report.", 5110)
    ShardFeatures:Set(ShardFeatures.SphereEmu)
    ShardFeatures:Clear(ShardFeatures:SmeltFlags())
  -- RunUO pre-AOS detection.
  elseif (getObjectName(UO.CharID) == nil) or (UO.MinDmg == 0 and UO.MaxDmg == 0) then
    UO.SysMessage("INFO: Age of Shadows (AOS) expansion WAS NOT detected on this shard. If this is incorrect please fill in a bug report.", 5110)
  else
    UO.SysMessage("INFO: Age of Shadows (AOS) expansion WAS detected on this shard. If this is incorrect please fill in a bug report.", 5110)
    ShardFeatures:Set(ShardFeatures:AOSDefault())
  end
end

function CheckSkills()
  -- Minimum Skill requirements.
  if Config.Hiding then
    local Skill = UO.GetSkill("Hiding")
    if Skill < 250 and not Debug.ForceHiding then
      UO.SysMessage("Hiding disabled due to low skill.", 5110)
      Config.Hiding = false
    end
  end
  Tinkering.CheckSkills()
end

function LateInit()
  local JEntryCount = Journal:EntryCount()
  Bot.CheckContextJindex = JEntryCount
  Bot.GuardsRegionJindex = JEntryCount
  Bot.JournalIndex = JEntryCount
end

function FindStartingRail()
  local _x, _y = UO.CharPosX, UO.CharPosY
  local closest_r, distance
  for r = 1, RAIL:count() do
    local dist_to_r = UODistance({x = _x, y = _y}, Rail:Pos(r))
    if r == 1 or dist_to_r < distance then
      distance = dist_to_r
      closest_r = r
    end
  end
  dbg_print(("FindStartingRail() -> Spot: %d (%d tile(s) away.)"):format(closest_r, distance))
  return closest_r, distance
end

function FindRail()
  if UO.Weight > Char:maxWeight() then
    Mining.DropOre()
  end
  Char:Print("Standby, calculating closest Rail...", 74)
  local closest_r, distance = FindStartingRail()
  if distance > 12 then
    ErrorHandling("You are too far away from your rails.")
  elseif distance ~= 0 then
    Char:Print("Moving to closest Rail.", 74)
    local x, y, z = RAIL[closest_r].x, RAIL[closest_r].y, RAIL[closest_r].z
    local Timeout = getticks() + WORLD_SAVE_TIMEOUT
    repeat
      UO.Pathfind(x, y, z)
      sleep(500)
      if getticks() > Timeout then
        ErrorHandling("Fatal error. Unable to Pathfind to closest rail!")
      end
    until (UO.CharPosX == x and UO.CharPosY == y)
  end
  Rail:Set(closest_r)
end

function CurrentTaskRail()
  if Char.LastHarvestRail and Char:getTask() == "Mine" then
    dbg_print(("CurrentTaskRail() -> Last rail we harvested = %d"):format(Char.LastHarvestRail))
    return Char.LastHarvestRail, getDirection(Char.LastHarvestRail)
  else
    return ClosestRail(Char:getTask())
  end
end

function Pathfind(x, y, z)
  local CharPos = Char:GetPos()
  dbg_ifprint(Debug.Pathfind, ("Pathfind() -> CharPos = %d, %d, %d"):format(CharPos.x, CharPos.y, CharPos.z))
  dbg_print(("Pathfind() -> x = %d, y = %d, z = %d"):format(x, y, z))
  -- Don't pathfind to the current position.
  if CharPos.x == x and CharPos.y == y then
    dbg_print("Pathfind() -> CharPos == x, y, z")
    return true
  end
  CheckContext()
  CheckStamina()
  if UO.Weight > Char:maxWeight() then
    Mining.DropOre()
  end
  -- Fix Z handling...
  if z == 0 then z = -1 end
  -- Call Pathfind()
  dbg_ifprint(Debug.Pathfind, "Pathfind() -> calling UO.Pathfind()")
  UO.Pathfind(x, y, z)
  sleep(ScaledMS(UODistance(CharPos, {x = x, y = y}) * 500))
  if UO.CharPosX == x and UO.CharPosY == y then
    dbg_ifprint(Debug.Pathfind, "Pathfind() succeeded!")
    return true
  else
    dbg_ifprint(Debug.Pathfind, "Pathfind() failed!")
    return false
  end
end

function Pathfind_rail(r)
  if Pathfind(RAIL[r].x, RAIL[r].y, RAIL[r].z) then
    return true
  else
    Rail:ClearPathfind(r)
    return false
  end
end

function MoveCoord(Curr, Dest, Thresh)
  local Delta = Dest - Curr
  if not (Delta == 0) then
    Delta = (Delta / math.abs(Delta)) * Thresh
  end
  Dest = Dest + Delta
  dbg_ifprint(Debug.Pathfind, ("MoveCoord() -> %d"):format(Dest))
  return Dest
end

function MoveTimeout(x, y, Thresh)
  local MoveTimeout = ScaledMS(500 * (UODistance(Char:GetPos(), {x = x, y = y}) - Thresh))
  dbg_ifprint(Debug.Pathfind, ("MoveTimeout() -> %d"):format(MoveTimeout))
  return MoveTimeout
end

function Move(x, y, Thresh)
  local CharPos = Char:GetPos()
  dbg_ifprint(Debug.Pathfind, ("Move() -> CharPos = %d, %d"):format(CharPos.x, CharPos.y))
  dbg_print(("Move() -> x = %d, y = %d"):format(x, y))
  dbg_ifprint(Debug.Pathfind, ("Move() -> Thresh = %d"):format(Thresh))
  -- Don't move to the current position.
  if CharPos.x == x and CharPos.y == y then
    dbg_print("Move() -> CharPos.x, CharPos.y == x, y")
    return true
  end
  CheckStamina()
  -- Call Move()
  dbg_ifprint(Debug.Pathfind, "Move() -> calling UO.Move()")
  local _x = Thresh == 0 and x or MoveCoord(CharPos.x, x, Thresh)
  local _y = Thresh == 0 and y or MoveCoord(CharPos.y, y, Thresh)
  UO.Move(_x, _y, Thresh, MoveTimeout(_x, _y, Thresh))
  -- Retrieve updated character position
  CharPos = Char:GetPos()
  if (CharPos.x == x or CharPos.x == _x) and (CharPos.y == y or CharPos.y == _y) then
    dbg_ifprint(Debug.Pathfind, "Move() succeeded!")
    return true
  else
    dbg_ifprint(Debug.Pathfind, "Move() failed!")
    return false
  end
end

local function PathfindMovedtoRail(NextRail, DestRail)
  local Step = DestRail > NextRail and 1 or -1
  for r = NextRail, DestRail, Step do
    if UO.CharPosX == RAIL[r].x and UO.CharPosY == RAIL[r].y then
      dbg_ifprint(Debug.Pathfind, ("PathfindMovedtoRail() -> jumped to rail: %d"):format(r))
      Rail:Set(r)
      return true
    end
  end
  return false
end

local function PathfindtoRail_fn(r, DestRail)
  if RAIL[r].Pathfind and Pathfind_rail(r) then
    return true
  elseif Move(RAIL[r].x, RAIL[r].y, r == DestRail and 0 or 1) then
    return true
  elseif PathfindMovedtoRail(r, DestRail) then
    return true
  else
    Rail:SetPathfind(r)
    return false
  end
end

local function PathfindtoRailLoop(r, DestRail)
  Bot.GuardsRegionJindex = Journal:EntryCount()
  local Timeout = getticks() + WORLD_SAVE_TIMEOUT
  repeat
    local CurrRail = Char.rail
    if PathfindtoRail_fn(r, DestRail) then
      if CurrRail == Char.rail then
        Rail:Set(r)
      end
      CheckGuardsRegion()
      return
    end
  until getticks() > Timeout
  ErrorHandling("Fatal error: unable to Pathfind!")
end

local function MergeRailsLoop(nR, dR)
  local Next = nR
  local Step = nR > dR and -1 or 1
  for r = Rail:getNext(nR), dR, Step do
    if not (Rail:inPath(r, nR) and Rail:inPath(r, Next)) then
      break
    end
    Next = r
  end
  dbg_ifprint(Debug.Pathfind and Next ~= nR, ("MergeRailsLoop() -> Next rail = %d (was: %d)"):format(Next, nR))
  return Next
end

local function PathfindMergeRails(dR)
  local nR = Char:GetNextRail()
  return nR == dR and nR or MergeRailsLoop(nR, dR)
end

function PathfindtoRail(DestRail)
  if UO.Weight > Char:maxWeight() then
    Mining.DropOre()
  end
  while (Char.rail ~= DestRail) do
    CheckContext()
    if Char.UnderAttack or Char:HasLowHP() then
      dbg_print("PathfindtoRail() -> Char is under attack!")
      if Char:getTask() ~= "Bank" then
        Char:setTaskDone(true)
        return false
      end
    end
    local NextRail = PathfindMergeRails(DestRail)
    PathfindtoRailLoop(NextRail, DestRail)
  end
end

function PathfindLoop(r)
  dbg_print(("PathfindLoop() -> Destination rail = %d"):format(r))
  PathfindtoRail(r)
  -- Preserve Harvest direction.
  if Char.A == "Mine" and Char.rail == Char.LastHarvestRail then
    dbg_print(("PathfindLoop() -> Preserving direction: %s"):format(Char.LastHarvestDirection))
    Char.Direction = Char.LastHarvestDirection
    Char.LastHarvestRail = nil
  end
end

function Call(func)
  _env[func]()
end

-- ---------------------------
-- # Config
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Config = {}
CFG = {}

-- ---------------------------
-- $ Config $ DEFAULT SETTINGS
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Config.Coward = 250
Config.CraftingToolsInBackPack = 1
Config.Hiding = true
Config.IngotBag = nil
Config.Tinkering = true
Config.ToolsInBackPack = 1
Config.ShardFeatures = ShardFeatures:cfgDefault()
Config.Rail = Bot.FileName .. ".ral"

-- ---------------------------
-- % Config:write
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Config:write()
  local cfg_path = PATH_PRE .. "CFG\\" .. string.lower(Bot.cfgName)
  print("INFO: Saving CFG -> " .. cfg_path)
  local cfg_fd, e = openfile(cfg_path, "w")
  if not cfg_fd then
    ErrorHandling("Couldn't open a new file for writing!")
  end
  cfg_fd:write("TWMMB.Config.Coward = " .. tostring(Config.Coward) .. "\n")
  cfg_fd:write("TWMMB.Config.CraftingToolsInBackPack = " .. tostring(Config.CraftingToolsInBackPack) .. "\n")
  cfg_fd:write("TWMMB.Config.Hiding = " .. tostring(Config.Hiding) .. "\n")
  cfg_fd:write("TWMMB.Config.IngotBag = " .. tostring(Config.IngotBag) .. "\n")
  cfg_fd:write("TWMMB.Config.Tinkering = " .. tostring(Config.Tinkering) .. "\n")
  cfg_fd:write("TWMMB.Config.ToolsInBackPack = " .. tostring(Config.ToolsInBackPack) .. "\n")
  cfg_fd:write("TWMMB.Config.ShardFeatures = " .. tostring(Config.ShardFeatures) .. "\n")
  cfg_fd:write("TWMMB.Config.Rail = \"" .. string.lower(tostring(Config.Rail)) .. "\"\n")
  cfg_fd:write("TWMMB.Config.cfgVer = " .. tostring(Bot.cfgVer) .. "\n")
  cfg_fd:flush()
  cfg_fd:close()
end

function Config:update()
  if CFG.cfgVer then
    if CFG.cfgVer < 2 then
      CFG.CraftingToolsInBackPack = 1
      CFG.ShardFeatures = ShardFeatures:cfgDefault()
    end
    if CFG.cfgVer < 3 then
      Config.Coward = CFG.Coward
      Config.CraftingToolsInBackPack = CFG.CraftingToolsInBackPack
      Config.Hiding = CFG.Hiding
      Config.IngotBag = CFG.IngotBag
      Config.Tinkering = CFG.Tinkering
      Config.ToolsInBackPack = CFG.ToolsInBackPack
      Config.ShardFeatures = CFG.ShardFeatures
      Config.Rail = CFG.RailFile
    end
    Config.cfgVer = Bot.cfgVer
    print("INFO: Updating CFG to latest version.")
    Config:write()
    CFG = {}
  end
end

function Config:convert()
  local EUO_cfg_path = PATH_PRE .. string.lower(Bot.cfgName)
  local EUO_cfg_fd, e = openfile(EUO_cfg_path, "r")
  if not EUO_cfg_fd then
    ErrorHandling("Couldn't open old format (EasyUO) cfg: " .. EUO_cfg_path)
  end
  for line in EUO_cfg_fd:lines() do
    local Key = line:match("%%(%a+)")
    if Key == nil then
      EUO_cfg_fd:close()
      ErrorHandling("Fatal error. Unable to continue with cfg conversion!")
    elseif Key == "Coward" or Key == "MiningToolsInBackPack" or Key == "ToolsInBackPack" or Key == "TWMMBRailFile" then
      if Key == "MiningToolsInBackPack" then Key = "ToolsInBackPack" end
      if Key == "TWMMBRailFile" then Key = "Rail" end
      Config[Key] = line:match("%p%w+%s(.+)")
    elseif Key == "GrabToolsAndOre" or Key == "Healing" or Key == "Hiding" or Key == "Tinkering" then
      Config[Key] = false
      if tonumber(line:match("%p%w+%s(.+)")) == -1 then
        Config[Key] = true
      end
    elseif Key == "IngotBag" then
      local ID = line:match("%p%w+%s(.+)")
      if ID ~= "N/A" then
        Config[Key] = Sys26ToInt(ID)
      end
    end
  end
  EUO_cfg_fd:close()
  Config:write()
  print("Congratulations! Your old settings from EasyUO version have been converted to the new format. Enjoy.")
end

function Config:Load()
  local cfg_path = PATH_PRE .. "CFG\\" .. string.lower(Bot.cfgName)
  print("INFO: Loading CFG -> " .. cfg_path)
  local cfg_fd, e = openfile(cfg_path, "r")
  if cfg_fd then
    local s = cfg_fd:read()
    cfg_fd:close()
    if s:match("TWMMB.CFG = {") or s:match("(TWMMB%.CFG%.).+%s=%s.+") == "TWMMB.CFG." or
        s:match("(TWMMB%.Config%.).+%s=%s.+") == "TWMMB.Config." then
      dofile(cfg_path)
      Config:update()
    elseif s:match("set %%") then
      ErrorHandling(("CFGs that haven't been converted to the new format must reside in: \"%s\""):format(getbasedir()))
    else
      ErrorHandling(("Couldn't open cfg: %s\n\nUnknown file format!\n"):format(Bot.cfgName))
    end
  else
    local EUO_cfg_path = PATH_PRE .. string.lower(Bot.cfgName)
    local EUO_cfg_fd, e = openfile(EUO_cfg_path, "r")
    if EUO_cfg_fd then
      local s = EUO_cfg_fd:read()
      EUO_cfg_fd:close()
      if s:match("set %%") then
        Config:convert()
        dofile(cfg_path)
      else
        ErrorHandling(("Couldn't open cfg: %s\n\nUnknown file format!\n"):format(Bot.cfgName))
      end
    else
      dbg_print(("Config:Load() -> Couldn't open configuration file: %s"):format(Bot.cfgName))
      dbg_print(("Config:Load() -> CFGs must reside in: \"%sCFG\\\""):format(getbasedir()))
      dbg_print(("Config:Load() -> CFGs that haven't been converted to the new format must reside in: \"%s\""):format(getbasedir()))
      print("WARNING: configuration file not found. Using default settings!")
    end
  end
end

----------------------------------------------------
-- :: Print banner.
----------------------------------------------------
print("### Welcome to the Walking Mumbling Miner Bot!")

----------------------------------------------------
-- :: Load modules.
----------------------------------------------------
dofile(getbasedir()..'twmmb_tinkering.lua')
dofile(getbasedir()..'twmmb_mining.lua')

----------------------------------------------------
-- :: Load Config.
----------------------------------------------------
Config:Load()

----------------------------------------------------
-- :: Show GUI.
----------------------------------------------------
if not OpenEUOLua then
  dofile(getbasedir()..'twmmb_gui.lua')
  GUI.Show()
end
GUI = {}

----------------------------------------------------
-- :: Load Rail.
----------------------------------------------------
Rail:Load()

-- ---------------------------
-- :: Start the script!
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
LateInit()
InitScreen()
DetectShard()
ApplyRules()
CheckSkills()
Mining.Init()
Char:Print("The Walking Mumbling Miner Bot")
Char:Print("now working.")
Bot.ScriptStarted = true
Bot.DelayBase = 800
FindRail()
Char:Print("I am your Walking Mumbling Miner Bot!")

-- ---------------------------
-- %%% MAIN LOOP
-- This is the core loop.
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
while (1) do
  if Char:TaskDone() then
    Char:setTaskDone(false)
    Bot.LastTask = Char:getTask()
    local NextTask = Char:getNextTask()
    if table.empty(NextTask) then
      NextTask = GetTask()
    end
    Char:setTask(NextTask)
  end
  local CurrentTask = Char:getTask()
  -- GetTask() above can never set %TaskDone to true
  if not (CurrentTask == Bot.LastTask or Char:StandStill()) and
      (CurrentTask ~= RAIL:A(Char.rail) or RAIL:skip(Char.rail)) then
    local TaskRail, Direction = CurrentTaskRail()
    Char.Direction = Direction
    PathfindLoop(TaskRail)
  end
  if CurrentTask == RAIL:A(Char.rail) or Char:StandStill() then
    Call(CurrentTask)
  end
end
