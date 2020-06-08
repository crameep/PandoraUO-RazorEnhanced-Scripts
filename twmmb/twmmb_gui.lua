-- ;==================================
-- ; TWMMB GUI
-- ; Author: Antipatiko
-- ;==================================
local P = {}
TWMMB.GUI = P
setmetatable(P, {__index = TWMMB})
setfenv(1, P)
local _env = getfenv()

-------------------------------------------------------------------------
-- # -> Library
-------------------------------------------------------------------------

function TAGtoHandle (TAG)
  if not TAG then
    return
  elseif TAG == 1 then
    return "OnClick"
  elseif TAG == 3 then
    return "OnClose"
  end
end

function FreeObject(__Object)
  local Handle = TAGtoHandle (__Object.Tag)
  if Handle then
    __Object[Handle] = nil
  end
  Obj.Free(__Object)
end

-- ---------------------------
-- ###    ActiveObjects    ###
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ActiveObjects = {
  Alive = {},
  PendingDelete = {}
}

-- ---------------------------
-- # ActiveObjects:new()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function _ActiveObjects:new()
  obj = {}
  setmetatable(obj, self)
  self.__index = self
  return obj
end

-- ---------------------------
-- # ActiveObjects:Add()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function _ActiveObjects:Add (_Object)
  table.insert (self.Alive, _Object)
end

-- ---------------------------
-- # ActiveObjects:getTable()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function _ActiveObjects:getTable (_Object)
  return _Object:match("^[%w_]+")
end

-- ---------------------------
-- # ActiveObjects:getValue()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function _ActiveObjects:getValue (_Object)
  return _Object:match("%.(%w+)$")
end

-- ---------------------------
-- # ActiveObjects:toGC()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function _ActiveObjects:toGC()
  self.PendingDelete = self.Alive
  self.Alive = {}

  for i = 1, #self.PendingDelete do
    local _this = self.PendingDelete[i]
    local Object = _env[self:getTable(_this)][self:getValue(_this)]
    Object.Hide()
  end
end

-- ---------------------------
-- # ActiveObjects:Purge()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function _ActiveObjects:Purge()
  for i = 1, #self.PendingDelete do
    local _this = self.PendingDelete[i]
    local Table = self:getTable(_this)
    local Value = self:getValue(_this)
    FreeObject(_env[Table][Value])
    _env[Table][Value] = nil
  end

  self.PendingDelete = {}
end

--- ActiveObjects() Singleton.
ActiveObjects = _ActiveObjects:new()

-- ---------------------------
-- # FreeTimer()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function FreeTimer (tTimer)
  tTimer.Enabled = false
  tTimer.OnTimer = nil
  Obj.Free(tTimer)
end

-- ---------------------------
-- # Popup()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Popup (__String)
  MainForm.Hide()
  Display(__String)
  MainForm.Show()
end

-- ---------------------------
-- # -> VARS
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
CharLastPos = Char:GetPos()
ExistingRailCheck = false
ForgeSpotsCheck = false
LastMenu = nil
RailWriterJIndex = nil
SmeltFeatureSet = false
StopScript = false

-- ---------------------------
-- # -> Localization Strings
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- Must be kept in sync with twmmb_mining.lua
local CliLoc = {}
CliLoc.BackpackFull = "Your backpack is full, so the ore you mined is lost."
CliLoc.NoMetalHereToMine = "There is no metal here to mine"
CliLoc.NoSandHereToMine = "There is no sand here to mine"
CliLoc.SelectForge = "Select the forge on which to smelt the ore"
CliLoc.SmeltOre = "You smelt the ore removing the impurities"
CliLoc.YouBurnAway = "You burn away the impurities but are left with less useable metal."
CliLoc.YouCarefullyDig = "You carefully dig up sand of sufficient quality for glassblowing"
CliLoc.YouCarefullyExtract = "You carefully extract some workable stone from the ore vein!"
CliLoc.YouDigForAWhile = "You dig for a while but fail to find any of sufficient quality for glassblowing"
CliLoc.YouDigSomeOre = "You dig some .+ [Oo]re and put it in your backpack."
CliLoc.YouLoosenSomeRocks = "You loosen some rocks but fail to find any useable ore"
CliLoc.YouPutSomeOre = "You put some .+ ore in your backpack"
-- Specific strings for Sphere shards:
CliLoc.SphereNothingHereToMineFor = "There is nothing here to mine for."
CliLoc.SphereYouPutTheOre = "You put the .+ Ore"
CliLoc.SphereYouSmeltOre = "*You smelt .+ Ore*"

-- ---------------------------
-- # -> Types
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
ForgeType = {4017, 6522, 6526, 6530, 6534, 6538, 6546, 6550, 6554, 6558, 6562, 11736}
MiningToolsType = {3718, 3897, 3898}
OreType = {6583, 6584, 6585, 6586}

function SetTimeout(timeout)
  WORLD_SAVE_TIMEOUT = timeout
end

-- ---------------------------
-- # GetTarget
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
GetTarget = {}

function GetTarget:cursor()
  UO.TargCurs = true
  while UO.TargCurs == true do
    wait(100)
  end
end

function GetTarget:Type()
  FindItem.All()
  FindItem:ID({UO.LTargetID})
  return FindItem:get().Type
end

function SetSmeltShardFeature()
  if SmeltFeatureSet then
    return
  end
  FindItem:All()
  FindItem:ID({UO.LObjectID})
  if FindItem.Count == 0 then
    if UO.LTargetID == 0 then
      ShardFeatures:Clear(ShardFeatures:SmeltFlags())
      ShardFeatures:Set(ShardFeatures.SmeltOnDblClick)
      SmeltFeatureSet = true
    elseif table.match(ForgeType, GetTarget:Type()) then
      SmeltFeatureSet = true
    end
  elseif table.match(ForgeType, FindItem:get().Type) then
    ShardFeatures:Clear(ShardFeatures:SmeltFlags())
    ShardFeatures:Set(ShardFeatures.SmeltDblClickForge)
    SmeltFeatureSet = true
  end
end

function ClearRail()
  Rail.A = {}
  Rail.x = {}
  Rail.y = {}
  Rail.z = {}
  Rail.Tx = {}
  Rail.Ty = {}
  Rail.Tz = {}
  Rail.Tkind = {}
  Rail.Ttile = {}
  Rail.TID = {}
  Rail.EndSpot = 0
end

function ClearLTarget()
  UO.LTargetX = 0
  UO.LTargetY = 0
  UO.LTargetZ = 0
  UO.LTargetKind = 0
  UO.LTargetTile = 0
  UO.LTargetID = 0
end

function __MarkSpot(SpotType)
  CharLastPos = Char:GetPos()
  Rail.EndSpot = Rail.EndSpot + 1
  Rail.A[Rail.EndSpot] = SpotType
  Rail.x[Rail.EndSpot] = UO.CharPosX
  Rail.y[Rail.EndSpot] = UO.CharPosY
  Rail.z[Rail.EndSpot] = UO.CharPosZ
  Rail.Tx[Rail.EndSpot] = UO.LTargetX
  Rail.Ty[Rail.EndSpot] = UO.LTargetY
  Rail.Tz[Rail.EndSpot] = UO.LTargetZ
  Rail.Tkind[Rail.EndSpot] = UO.LTargetKind
  Rail.Ttile[Rail.EndSpot] = UO.LTargetTile
  Rail.TID[Rail.EndSpot] = UO.LTargetID
  dbg_ifprint(Debug.RailWriter,
    ("__MarkSpot() -> A = %s, x = %d, y = %d, z = %d, Tx = %d, Ty = %d, Tz = %d, Tkind = %d, Ttile = %d, TID = %d"):format(
    SpotType, UO.CharPosX, UO.CharPosY, UO.CharPosZ, UO.LTargetX, UO.LTargetY, UO.LTargetZ, UO.LTargetKind, UO.LTargetTile, UO.LTargetID))
  ClearLTarget()
end

-- ---------------------------
-- # MarkSpot()
-- @1 = type of spot
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function MarkSpot(SpotType)
  __MarkSpot(SpotType)
  UO.ExMsg(UO.CharID, 3, 74, "Marking \"" .. SpotType .. "\" spot")
end

function getSpot(data)
  if Rail.EndSpot > 0 then
    for r = 1, Rail.EndSpot do
      if (not data.A or data.A == Rail.A[r]) and (not data.x or data.x == Rail.x[r]) and
          (not data.y or data.y == Rail.y[r]) and(not data.Tx or data.Tx == Rail.Tx[r]) and
          (not data.Ty or data.Ty == Rail.Ty[r]) then
        return true
      end
    end
  end
  return false
end

function SpotsLoop()
  local Jidx = RailWriterJIndex
  while (Jidx < Journal:EntryCount()) do
    Jidx = Jidx + 1
    local Entry = Journal:getEntry(Jidx)
    if Entry:match(CliLoc.YouDigSomeOre) or Entry:match(CliLoc.YouPutSomeOre) or
        Entry:match(CliLoc.NoMetalHereToMine) or Entry:match(CliLoc.YouLoosenSomeRocks) or
        Entry:match(CliLoc.YouCarefullyDig) or Entry:match(CliLoc.YouCarefullyExtract) or
        Entry:match(CliLoc.NoSandHereToMine) or Entry:match(CliLoc.YouDigForAWhile) or
        Entry:match(CliLoc.BackpackFull) or Entry:match(CliLoc.SphereNothingHereToMineFor) or
        Entry:match(CliLoc.SphereYouPutTheOre) then
      if getSpot({A = "Mine", Tx = UO.LTargetX, Ty = UO.LTargetY}) then
        UO.ExMsg(UO.CharID, 3, 1264, "Spot already marked!")
      else
        MarkSpot("Mine")
      end
    end
  end
  while (RailWriterJIndex < Journal:EntryCount()) do
    RailWriterJIndex = RailWriterJIndex + 1
    local Entry = Journal:getEntry(RailWriterJIndex)
    if Entry:match(CliLoc.SmeltOre) or Entry:match(CliLoc.YouBurnAway) or Entry:match(CliLoc.SphereYouSmeltOre) then
      if getSpot({A = "Forge", x = UO.CharPosX, y = UO.CharPosY}) then
        UO.ExMsg(UO.CharID, 3, 1264, "Spot already marked!")
      else
        SetSmeltShardFeature()
        MarkSpot("Forge")
      end
    end
  end
  local CharPos = { x = UO.CharPosX, y = UO.CharPosY }
  if not (CharPos.x == CharLastPos.x or CharPos.y == CharLastPos.y) or UODistance(CharPos, CharLastPos) > 12 then
    __MarkSpot("Walk")
  end
end

function CheckSpots()
  local MarkedBankSpot = false
  local MarkedForgeSpot = false
  local MarkedHarvestSpots = false
  if Rail.EndSpot == 0 then
    Popup ("You haven't marked any spot. Please do so!")
    return false
  elseif Debug.RailWriter then
    return true
  else
    for r = 1, Rail.EndSpot do
      if Rail.A[r] == "Bank" then
        MarkedBankSpot = true
      elseif Rail.A[r] == "Forge" then
        MarkedForgeSpot = true
      elseif Rail.A[r] == "Mine" or Rail.A[r] == "Chop" then
        MarkedHarvestSpots = true
      end
    end
  end
  if not MarkedBankSpot then
    Popup ("You haven't marked a Bank spot. Please do so!")
    return false
  elseif not MarkedHarvestSpots then
    Popup ("You haven't marked any Mining spots. Please do so!")
    return false
  elseif not (MarkedForgeSpot or ForgeSpotsCheck) then
    Popup ("Forge spots are automatically marked when you smelt ore.\nNot doing so can be detrimental to your miner's performance!\n\n" ..
      "Proceed (SAVE) only if you understand the consequences.")
    ForgeSpotsCheck = true
    return false
  else
    return true
  end
end

function ExistingRail()
  local Railpath = PATH_PRE .. "Rails\\" .. string.lower (Config.Rail)
  local _ExistingRail, e = openfile (Railpath, "r")
  if _ExistingRail == nil then
    return false
  else
    _ExistingRail:close()
    return true
  end
end

-- ---------------------------
-- # Base Window
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
BaseWindow = {}

function BaseWindow:getLeft()
  return UO.CliLogged and (UO.CliLeft + (UO.CliXRes - MainForm.Width) / 2) or 200
end

function BaseWindow:getTop()
  return UO.CliLogged and (UO.CliTop + (UO.CliYRes - MainForm.Height) / 2) or 200
end

function BaseWindow:Show(Width, Height)
  MainForm = Obj.Create("TForm")
  MainForm.Width = Width
  MainForm.Height = Height
  MainForm.Left = BaseWindow:getLeft()
  MainForm.Top = BaseWindow:getTop()
  MainForm.Font.Name = "Arial"
  MainForm.Font.Size = 9
  MainForm.Caption = "TWMMB - Main Menu"
  MainForm.OnClose = MainForm_Handler
  MainForm.Tag = 3

  BaseWindow.Intro = Obj.Create("TLabel")
  BaseWindow.Intro.Parent = MainForm
  BaseWindow.Intro.Left = 15
  BaseWindow.Intro.Top = 10
  BaseWindow.Intro.Font.Name = "Garamond"
  BaseWindow.Intro.Font.Size = 19
  BaseWindow.Intro.Caption = "The Walking Mumbling Miner Bot"

  BaseWindow.Copyright1 = Obj.Create("TLabel")
  BaseWindow.Copyright1.Parent = MainForm
  BaseWindow.Copyright1.Left = 13
  BaseWindow.Copyright1.Top = 370
  BaseWindow.Copyright1.Caption = "(C) 2016 Antipatiko"

  BaseWindow.Copyright2 = Obj.Create("TLabel")
  BaseWindow.Copyright2.Parent = MainForm
  BaseWindow.Copyright2.Left = 13
  BaseWindow.Copyright2.Top = 385
  BaseWindow.Copyright2.Caption = "Please submit your suggestions or bug reports on EasyUO forum."
end

-- ---------------------------
-- # BaseWindow:Free()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function BaseWindow:Free()
  Obj.Free(BaseWindow.Copyright2)
  Obj.Free(BaseWindow.Copyright1)
  Obj.Free(BaseWindow.Intro)
  FreeObject(MainForm)
end

-- ---------------------------
-- # BaseWindow:Close()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function BaseWindow.Close()
  MainForm.Hide()
  Obj.Exit()
  ActiveObjects:toGC()
  ActiveObjects:Purge()
  BaseWindow:Free()
end

-- ---------------------------
-- # MainForm_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function MainForm_Handler()
  if MainMenu.Symbol1 == nil then
    MainMenu.Show()
  else
    BaseWindow.Close()
    StopScript = true
  end
end

-- ---------------------------
-- # Main Menu
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
MainMenu = {}

-- ---------------------------
-- # MainMenu.Show()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function MainMenu.Show()
  ActiveObjects:toGC()

  MainMenu.Symbol1 = Obj.Create("TLabel")
  MainMenu.Symbol1.Parent = MainForm
  MainMenu.Symbol1.Left = 11
  MainMenu.Symbol1.Top = 125
  MainMenu.Symbol1.Font.Name = "Wingdings"
  MainMenu.Symbol1.Font.Size = 100
  MainMenu.Symbol1.Font.Style = 1
  MainMenu.Symbol1.Font.Color = tonumber("00007090", 16)
  MainMenu.Symbol1.Caption = "6"
  ActiveObjects:Add("MainMenu.Symbol1")

  MainMenu.Symbol2 = Obj.Create("TLabel")
  MainMenu.Symbol2.Parent = MainForm
  MainMenu.Symbol2.Left = 11
  MainMenu.Symbol2.Top = 125
  MainMenu.Symbol2.Font.Name = "Wingdings"
  MainMenu.Symbol2.Font.Size = 100
  MainMenu.Symbol2.Font.Color = tonumber("0000C0F0", 16)
  MainMenu.Symbol2.Caption = "6"
  ActiveObjects:Add("MainMenu.Symbol2")

  MainMenu.Title = Obj.Create("TLabel")
  MainMenu.Title.Parent = MainForm
  MainMenu.Title.Left = 190
  MainMenu.Title.Top = 70
  MainMenu.Title.Font.Size = 15
  MainMenu.Title.Caption = "MAIN MENU"
  ActiveObjects:Add("MainMenu.Title")

  MainMenu.RailWizardTWMMB = Obj.Create("TButton")
  MainMenu.RailWizardTWMMB.Parent = MainForm
  MainMenu.RailWizardTWMMB.Left = 120
  MainMenu.RailWizardTWMMB.Top = 135
  MainMenu.RailWizardTWMMB.Width = 260
  MainMenu.RailWizardTWMMB.Height = 30
  MainMenu.RailWizardTWMMB.Caption = "::   Rail Wizard   ::"
  MainMenu.RailWizardTWMMB.OnClick = RailWizard.Show
  MainMenu.RailWizardTWMMB.Tag = 1
  ActiveObjects:Add("MainMenu.RailWizardTWMMB")

  MainMenu.SettingsTWMMB = Obj.Create("TButton")
  MainMenu.SettingsTWMMB.Parent = MainForm
  MainMenu.SettingsTWMMB.Left = 120
  MainMenu.SettingsTWMMB.Top = 170
  MainMenu.SettingsTWMMB.Width = 260
  MainMenu.SettingsTWMMB.Height = 30
  MainMenu.SettingsTWMMB.Caption = "::   Settings   ::"
  MainMenu.SettingsTWMMB.OnClick = SettingsWizard.Show
  MainMenu.SettingsTWMMB.Tag = 1
  ActiveObjects:Add("MainMenu.SettingsTWMMB")

  MainMenu.StartTWMMB = Obj.Create("TButton")
  MainMenu.StartTWMMB.Parent = MainForm
  MainMenu.StartTWMMB.Left = 120
  MainMenu.StartTWMMB.Top = 230
  MainMenu.StartTWMMB.Width = 260
  MainMenu.StartTWMMB.Height = 35
  MainMenu.StartTWMMB.Caption = ">>   Start Script   <<"
  MainMenu.StartTWMMB.OnClick = MainMenu.StartTWMMB_Handler
  MainMenu.StartTWMMB.Tag = 1
  ActiveObjects:Add("MainMenu.StartTWMMB")

  MainMenu.TTimer1 = Obj.Create("TTimer")
  MainMenu.TTimer1.OnTimer = MainMenu.TTimer1_Handler
  MainMenu.TTimer1.Interval = 5
  MainMenu.TTimer1.Enabled = true
  --ActiveObjects:Add("MainMenu.TTimer1")

  MainForm.ActiveControl = MainMenu.StartTWMMB
end

-- ------------------------------
-- # MainMenu.TTimer1_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function MainMenu.TTimer1_Handler()
  MainMenu.TTimer1.Enabled = false
  ActiveObjects:Purge()
end

-- ------------------------------
-- # MainMenu.StartTWMMB_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MainMenu.StartTWMMB_Handler = function()
  if ExistingRail() then
    BaseWindow.Close()
  else
  MainForm.Hide()
    Popup ("Please create a rail using the wizard and then start the script.")
    MainForm.Show()
  end
end

-- ---------------------------
-- # Rail Wizard
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
RailWizard = {}

-- ---------------------------
-- # RailWizard.Show()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function RailWizard.Show()
  ActiveObjects:toGC()
  MainForm.Caption = "Rail Wizard"

  RailWizard.TLabel1 = Obj.Create("TLabel")
  RailWizard.TLabel1.Parent = MainForm
  RailWizard.TLabel1.Left = 60
  RailWizard.TLabel1.Top = 40
  RailWizard.TLabel1.Font.Name = "Garamond"
  RailWizard.TLabel1.Font.Size = 15
  RailWizard.TLabel1.Caption = "The 'Uncolored Bikeshed' edition"
  ActiveObjects:Add("RailWizard.TLabel1")

  RailWizard.TLabel2 = Obj.Create("TLabel")
  RailWizard.TLabel2.Parent = MainForm
  RailWizard.TLabel2.Left = 25
  RailWizard.TLabel2.Top = 80
  RailWizard.TLabel2.Font.Style = 1
  RailWizard.TLabel2.Caption = "Welcome to The Walking Mumbling Miner Bot."
  ActiveObjects:Add("RailWizard.TLabel2")

  RailWizard.TLabel3 = Obj.Create("TLabel")
  RailWizard.TLabel3.Parent = MainForm
  RailWizard.TLabel3.Left = 25
  RailWizard.TLabel3.Top = 110
  RailWizard.TLabel3.Caption = "This wizard will guide you through the rail making process."
  ActiveObjects:Add("RailWizard.TLabel3")

  RailWizard.TLabel4 = Obj.Create("TLabel")
  RailWizard.TLabel4.Parent = MainForm
  RailWizard.TLabel4.Left = 25
  RailWizard.TLabel4.Top = 130
  RailWizard.TLabel4.Caption = "Please read carefully all instructions."
  ActiveObjects:Add("RailWizard.TLabel4")

  RailWizard.TLabel5 = Obj.Create("TLabel")
  RailWizard.TLabel5.Parent = MainForm
  RailWizard.TLabel5.Left = 25
  RailWizard.TLabel5.Top = 170
  RailWizard.TLabel5.Caption = "When you are ready to proceed, click CONTINUE."
  ActiveObjects:Add("RailWizard.TLabel5")

  RailWizard.TButton1 = Obj.Create("TButton")
  RailWizard.TButton1.Parent = MainForm
  RailWizard.TButton1.Left = 70
  RailWizard.TButton1.Top = 210
  RailWizard.TButton1.Width = 260
  RailWizard.TButton1.Height = 30
  RailWizard.TButton1.Font.Style = 1
  RailWizard.TButton1.Caption = "CONTINUE"
  RailWizard.TButton1.OnClick = RailWizard_Step1.Show
  RailWizard.TButton1.Tag = 1
  ActiveObjects:Add("RailWizard.TButton1")

  RailWizard.TTimer1 = Obj.Create("TTimer")
  RailWizard.TTimer1.OnTimer = RailWizard.TTimer1_Handler
  RailWizard.TTimer1.Interval = 5
  RailWizard.TTimer1.Enabled = true
  --ActiveObjects:Add("RailWizard.TTimer1")
end

-- ------------------------------
-- # RailWizard.TTimer1_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function RailWizard.TTimer1_Handler()
  RailWizard.TTimer1.Enabled = false
  ActiveObjects:Purge()
end

-- ---------------------------
-- # Rail Wizard - Step 1
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
RailWizard_Step1 = {}

-- ---------------------------
-- # RailWizard_Step1.Show()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function RailWizard_Step1.Show()
  ActiveObjects:toGC()

  RailWizard_Step1.TLabel1 = Obj.Create("TLabel")
  RailWizard_Step1.TLabel1.Parent = MainForm
  RailWizard_Step1.TLabel1.Left = 25
  RailWizard_Step1.TLabel1.Top = 60
  RailWizard_Step1.TLabel1.Font.Style = 1
  RailWizard_Step1.TLabel1.Caption = ":: Record the rail."
  ActiveObjects:Add("RailWizard_Step1.TLabel1")

  RailWizard_Step1.TLabel2 = Obj.Create("TLabel")
  RailWizard_Step1.TLabel2.Parent = MainForm
  RailWizard_Step1.TLabel2.Left = 25
  RailWizard_Step1.TLabel2.Top = 90
  RailWizard_Step1.TLabel2.Caption = "Mining spots are marked when you use a shovel or pickaxe to"
  ActiveObjects:Add("RailWizard_Step1.TLabel2")

  RailWizard_Step1.TLabel3 = Obj.Create("TLabel")
  RailWizard_Step1.TLabel3.Parent = MainForm
  RailWizard_Step1.TLabel3.Left = 25
  RailWizard_Step1.TLabel3.Top = 110
  RailWizard_Step1.TLabel3.Caption = "harvest ore from ground. Do it once for each spot."
  ActiveObjects:Add("RailWizard_Step1.TLabel3")

  RailWizard_Step1.TLabel4 = Obj.Create("TLabel")
  RailWizard_Step1.TLabel4.Parent = MainForm
  RailWizard_Step1.TLabel4.Left = 25
  RailWizard_Step1.TLabel4.Top = 140
  RailWizard_Step1.TLabel4.Caption = "Be sure to use a forge if there's any on your way."
  ActiveObjects:Add("RailWizard_Step1.TLabel4")

  RailWizard_Step1.TLabel5 = Obj.Create("TLabel")
  RailWizard_Step1.TLabel5.Parent = MainForm
  RailWizard_Step1.TLabel5.Left = 25
  RailWizard_Step1.TLabel5.Top = 170
  RailWizard_Step1.TLabel5.Caption = "You can mark multiple bank spots or secure containers."
  ActiveObjects:Add("RailWizard_Step1.TLabel5")

  RailWizard_Step1.TButton1 = Obj.Create("TButton")
  RailWizard_Step1.TButton1.Parent = MainForm
  RailWizard_Step1.TButton1.Left = 100
  RailWizard_Step1.TButton1.Top = 205
  RailWizard_Step1.TButton1.Width = 200
  RailWizard_Step1.TButton1.Height = 20
  RailWizard_Step1.TButton1.Caption = "Save Bank Spot"
  RailWizard_Step1.TButton1.OnClick = RailWizard_Step1.TButton1_Handler
  RailWizard_Step1.TButton1.Tag = 1
  ActiveObjects:Add("RailWizard_Step1.TButton1")

  RailWizard_Step1.TButton2 = Obj.Create("TButton")
  RailWizard_Step1.TButton2.Parent = MainForm
  RailWizard_Step1.TButton2.Left = 100
  RailWizard_Step1.TButton2.Top = 235
  RailWizard_Step1.TButton2.Width = 200
  RailWizard_Step1.TButton2.Height = 20
  RailWizard_Step1.TButton2.Caption = "Save Secure Box"
  RailWizard_Step1.TButton2.OnClick = RailWizard_Step1.TButton2_Handler
  RailWizard_Step1.TButton2.Tag = 1
  ActiveObjects:Add("RailWizard_Step1.TButton2")

  RailWizard_Step1.TButton3 = Obj.Create("TButton")
  RailWizard_Step1.TButton3.Parent = MainForm
  RailWizard_Step1.TButton3.Left = 12
  RailWizard_Step1.TButton3.Top = 320
  RailWizard_Step1.TButton3.Width = 130
  RailWizard_Step1.TButton3.Height = 30
  RailWizard_Step1.TButton3.Font.Style = 1
  RailWizard_Step1.TButton3.Caption = ":: RESTART RAIL"
  RailWizard_Step1.TButton3.OnClick = RailWizard_Step1.TButton3_Handler
  RailWizard_Step1.TButton3.Tag = 1
  ActiveObjects:Add("RailWizard_Step1.TButton3")

  RailWizard_Step1.TButton4 = Obj.Create("TButton")
  RailWizard_Step1.TButton4.Parent = MainForm
  RailWizard_Step1.TButton4.Left = 260
  RailWizard_Step1.TButton4.Top = 320
  RailWizard_Step1.TButton4.Width = 130
  RailWizard_Step1.TButton4.Height = 30
  RailWizard_Step1.TButton4.Font.Style = 1
  RailWizard_Step1.TButton4.Caption = "SAVE RAIL"
  RailWizard_Step1.TButton4.OnClick = RailWizard_Step1.TButton4_Handler
  RailWizard_Step1.TButton4.Tag = 1
  ActiveObjects:Add("RailWizard_Step1.TButton4")

  RailWizard_Step1.TTimer1 = Obj.Create("TTimer")
  RailWizard_Step1.TTimer1.OnTimer = RailWizard_Step1.TTimer1_Handler
  RailWizard_Step1.TTimer1.Interval = 5
  RailWizard_Step1.TTimer1.Enabled = true
  --ActiveObjects:Add("RailWizard_Step1.TTimer1")

  RailWizard_Step1.TTimer2 = Obj.Create("TTimer")
  RailWizard_Step1.TTimer2.OnTimer = SpotsLoop
  RailWizard_Step1.TTimer2.Interval = 100
  --ActiveObjects:Add("RailWizard_Step1.TTimer2")

  MainForm.ActiveControl = RailWizard_Step1.TButton4
end

-- ---------------------------
-- # RailWizard_Step1.TTimer1_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function RailWizard_Step1.TTimer1_Handler()
  RailWizard_Step1.TTimer1.Enabled = false
  ActiveObjects:Purge()
  CharLastPos = Char:GetPos()
  ClearRail()
  ClearLTarget()
  RailWriterJIndex = Journal:EntryCount()
  RailWizard_Step1.TTimer2.Enabled = true
end

-- ---------------------------
-- # RailWizard_Step1.TButton1_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function RailWizard_Step1.TButton1_Handler()
  local Orig_Timeout = WORLD_SAVE_TIMEOUT
  SetTimeout(1000)
  if not BankBox:Open() then
    MainForm.Hide()
    Popup("Unable to open Bank Box! Please retry.")
    MainForm.Show()
  elseif not getSpot({A = "Bank", x = UO.CharPosX, y = UO.CharPosY}) then
    ClearLTarget() -- We might be carrying a stale value that could break the Bank routine.
    MarkSpot("Bank")
  end
  SetTimeout(Orig_Timeout)
end

-- ---------------------------
-- # OpenSecureBox()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function OpenSecureBox(_SecureID)
  UO.LObjectID = _SecureID
  UO.Macro(17, 0) -- LastObject
  local Timeout = getticks() + 5000
  repeat
    wait(100)
    local ContName, ContSizeX, ContSizeY = UO.ContName, UO.ContSizeX, UO.ContSizeY
    if ContName == "container gump" then
      if ContSizeX == 180 and ContSizeY == 240 then
        return true -- Chest
      elseif ContSizeX == 176 and ContSizeY == 194 then
        return true -- Bag
      elseif ContSizeX == 206 and ContSizeY == 166 then
        return true -- Box
      elseif ContSizeX == 202 and ContSizeY == 162 then
        return true -- Basket
      elseif ContSizeX == 190 and ContSizeY == 140 then
        return true -- Crate
      elseif ContSizeX == 174 and ContSizeY == 210 then
        return true -- Bucket/Barrel
      end
    end
  until getticks() > Timeout
  return false
end

-- ---------------------------
-- # RailWizard_Step1.TButton2_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function RailWizard_Step1.TButton2_Handler()
  UO.LTargetID = 0
  MainForm.Hide()
  GetTarget:cursor()
  if not (UO.LTargetID == 0) and UO.LTargetKind == 1 then
    if OpenSecureBox(UO.LTargetID) then
      if not getSpot({A = "Bank", x = UO.CharPosX, y = UO.CharPosY}) then
        MarkSpot("Bank")
      end
    else
      Popup("Unable to open Secure Box! Please retry.")
    end
  end
  MainForm.Show()
end

-- ---------------------------
-- # RailWizard_Step1.TButton3_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function RailWizard_Step1.TButton3_Handler()
  RailWizard.Show()
  ClearRail()
  UO.ExMsg (UO.CharID, 3, 38, "Marked spots successfully erased.")
end

-- ---------------------------
-- # NonexistentRail()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function NonexistentRail()
  if ExistingRailCheck then
    return true
  end
  ExistingRailCheck = true
  if ExistingRail() then
    MainForm.Hide()
    Popup ("If you proceed, your existing rail will be overwritten.\nBe careful, this is your first and last warning!")
    MainForm.Show()
    return false
  else
    return true
  end
end

-- ---------------------------
-- # RailWizard_Step1.TButton4_Handler()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function RailWizard_Step1.TButton4_Handler()
  if CheckSpots() and NonexistentRail() then
    RailWizard_Step1.TTimer2.Enabled = false
    RailWizard_Step2.Show()
  end
end

-- ---------------------------
-- # Rail Wizard - Step 2
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
RailWizard_Step2 = {}

function RailWizard_Step2.Show()
  ActiveObjects:toGC()

  RailWizard_Step2.TLabel1 = Obj.Create("TLabel")
  RailWizard_Step2.TLabel1.Parent = MainForm
  RailWizard_Step2.TLabel1.Left = 110
  RailWizard_Step2.TLabel1.Top = 150
  RailWizard_Step2.TLabel1.Font.Style = 1
  RailWizard_Step2.TLabel1.Caption = "Please wait while saving rail ..."
  ActiveObjects:Add("RailWizard_Step2.TLabel1")

  RailWizard_Step2.TTimer1 = Obj.Create("TTimer")
  RailWizard_Step2.TTimer1.OnTimer = RailWizard_Step2.TTimer1_Handler
  RailWizard_Step2.TTimer1.Interval = 5
  RailWizard_Step2.TTimer1.Enabled = true
  --ActiveObjects:Add("RailWizard_Step2.TTimer1")

  RailWizard_Step2.TTimer2 = Obj.Create("TTimer")
  RailWizard_Step2.TTimer2.OnTimer = RailWizard_Step2.TTimer2_Handler
  RailWizard_Step2.TTimer2.Interval = 2000
  --ActiveObjects:Add("RailWizard_Step2.TTimer2")
end

function RailWizard_Step2.TTimer1_Handler()
  RailWizard_Step2.TTimer1.Enabled = false
  ActiveObjects:Purge()
  RailWizard_Step2.TTimer2.Enabled = true
end

function RailWizard_Step2.TTimer2_Handler()
  RailWizard_Step2.TTimer2.Enabled = false
  if not ShardFeatures:Get(ShardFeatures.SmeltDblClickOre) then
    Config:write()
  end
  Rail:save()
  MainMenu.Show()
end

-- ---------------------------
-- # Settings Wizard
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
SettingsWizard = {}

function SettingsWizard.Show()
  ActiveObjects:toGC()
  MainForm.Caption = "Settings"

  SettingsWizard.TLabel1 = Obj.Create("TLabel")
  SettingsWizard.TLabel1.Parent = MainForm
  SettingsWizard.TLabel1.Left = 25
  SettingsWizard.TLabel1.Top = 60
  SettingsWizard.TLabel1.Font.Style = 1
  SettingsWizard.TLabel1.Caption = ":: Settings."
  ActiveObjects:Add("SettingsWizard.TLabel1")

  SettingsWizard.TCheckBox1 = Obj.Create("TCheckBox")
  SettingsWizard.TCheckBox1.Parent = MainForm
  SettingsWizard.TCheckBox1.Left = 25
  SettingsWizard.TCheckBox1.Top = 100
  SettingsWizard.TCheckBox1.Width = 300
  SettingsWizard.TCheckBox1.Height = 20
  SettingsWizard.TCheckBox1.Checked = Config.Tinkering
  SettingsWizard.TCheckBox1.Caption = "Enable Tinkering (requires +30 Skill)."
  ActiveObjects:Add("SettingsWizard.TCheckBox1")

  SettingsWizard.TCheckBox2 = Obj.Create("TCheckBox")
  SettingsWizard.TCheckBox2.Parent = MainForm
  SettingsWizard.TCheckBox2.Left = 25
  SettingsWizard.TCheckBox2.Top = 120
  SettingsWizard.TCheckBox2.Width = 300
  SettingsWizard.TCheckBox2.Height = 20
  SettingsWizard.TCheckBox2.Checked = Config.Hiding
  SettingsWizard.TCheckBox2.Caption = "Enable Hiding Skill (requires +25 Skill)."
  ActiveObjects:Add("SettingsWizard.TCheckBox2")

  SettingsWizard.TLabel2 = Obj.Create("TLabel")
  SettingsWizard.TLabel2.Parent = MainForm
  SettingsWizard.TLabel2.Left = 62
  SettingsWizard.TLabel2.Top = 217
  SettingsWizard.TLabel2.Caption = "Max amount of Ingots to carry in Backpack. [50-999]"
  ActiveObjects:Add("SettingsWizard.TLabel2")

  SettingsWizard.TEdit1 = Obj.Create("TEdit")
  SettingsWizard.TEdit1.Parent = MainForm
  SettingsWizard.TEdit1.Left = 25
  SettingsWizard.TEdit1.Top = 215
  SettingsWizard.TEdit1.Width = 30
  SettingsWizard.TEdit1.MaxLength = 3
  SettingsWizard.TEdit1.Text = tostring(Config.Coward)
  ActiveObjects:Add("SettingsWizard.TEdit1")

  SettingsWizard.TLabel3 = Obj.Create("TLabel")
  SettingsWizard.TLabel3.Parent = MainForm
  SettingsWizard.TLabel3.Left = 52
  SettingsWizard.TLabel3.Top = 242
  SettingsWizard.TLabel3.Caption = "Tools to carry in Backpack. [1-5]"
  ActiveObjects:Add("SettingsWizard.TLabel3")

  SettingsWizard.TEdit2 = Obj.Create("TEdit")
  SettingsWizard.TEdit2.Parent = MainForm
  SettingsWizard.TEdit2.Left = 25
  SettingsWizard.TEdit2.Top = 240
  SettingsWizard.TEdit2.Width = 20
  SettingsWizard.TEdit2.MaxLength = 1
  SettingsWizard.TEdit2.Text = tostring(Config.ToolsInBackPack)
  ActiveObjects:Add("SettingsWizard.TEdit2")

  SettingsWizard.TButton1 = Obj.Create("TButton")
  SettingsWizard.TButton1.Parent = MainForm
  SettingsWizard.TButton1.Left = 260
  SettingsWizard.TButton1.Top = 320
  SettingsWizard.TButton1.Width = 130
  SettingsWizard.TButton1.Height = 30
  SettingsWizard.TButton1.Font.Style = 1
  SettingsWizard.TButton1.Caption = "SAVE SETTINGS"
  SettingsWizard.TButton1.OnClick = SettingsWizard.TButton1_Handler
  SettingsWizard.TButton1.Tag = 1
  ActiveObjects:Add("SettingsWizard.TButton1")

  SettingsWizard.TTimer1 = Obj.Create("TTimer")
  SettingsWizard.TTimer1.OnTimer = SettingsWizard.TTimer1_Handler
  SettingsWizard.TTimer1.Interval = 5
  SettingsWizard.TTimer1.Enabled = true
  --ActiveObjects:Add("SettingsWizard.TTimer1")

  MainForm.ActiveControl = SettingsWizard.TButton1
end

function SettingsWizard.TTimer1_Handler()
  SettingsWizard.TTimer1.Enabled = false
  ActiveObjects:Purge()
end

function SettingsWizard.TButton1_Handler()
  ShardFeatures.Set(ShardFeatures.HumanStrongBack)
  Config.Coward = tonumber(SettingsWizard.TEdit1.Text)
  if not Config.Coward or Config.Coward < 50 or Config.Coward > 999 then
    Config.Coward = 250
  end
  Config.ToolsInBackPack = tonumber(SettingsWizard.TEdit2.Text)
  if not Config.ToolsInBackPack or Config.ToolsInBackPack < 1 or Config.ToolsInBackPack > 5 then
    Config.ToolsInBackPack = 1
  end
  Config.Tinkering = SettingsWizard.TCheckBox1.Checked
  Config.Hiding = SettingsWizard.TCheckBox2.Checked
  Config:write()
  MainMenu.Show()
end

function Show()
  BaseWindow:Show (415, 445)
  MainMenu.Show()
  MainForm.Show()
  Obj.Loop()
  if StopScript then
    stop()
  end
end
