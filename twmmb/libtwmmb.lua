-- ;==================================
-- ; TWMMB Library
-- ; Author: Antipatiko
-- ;==================================
setfenv(1, TWMMB)

function table.copy(t)
  local t_new = {}
  for k, v in pairs(t) do
    t_new[k] = v
  end
  return t_new
end

function table.count(t)
  local count = 0
  for k, v in pairs(t) do
    count = count + 1
  end
  return count
end

-- [ http://stackoverflow.com/questions/640642/how-do-you-copy-a-lua-table-by-value ]
function table.deepcopy(o, seen)
  seen = seen or {}
  if o == nil then return nil end
  if seen[o] then return seen[o] end

  local no = {}
  seen[o] = no
  setmetatable(no, table.deepcopy(getmetatable(o), seen))

  for k, v in next, o, nil do
    k = (type(k) == 'table') and k:deepcopy(seen) or k
    v = (type(v) == 'table') and v:deepcopy(seen) or v
    no[k] = v
  end
  return no
end

function table.empty(t)
  return next(t) == nil
end

function table.fast_insert(t, v)
  t[#t+1] = v
end

function table.join(...)
  local tables = arg.n
  local t = {}
  for i = 1, tables do
    local this = arg[i]
    for it = 1, #this do
      table.insert(t, this[it])
    end
  end
  return t
end

function table.match(t, s)
  if table.pos(t, s) == 0 then
    return false
  else
    return true
  end
end

function table.merge(t1, t2)
  for k, v in pairs(t2) do
    if (type(v) == "table") and (type(t1[k] or false) == "table") then
      table.merge(t1[k], t2[k])
    else
      t1[k] = v
    end
  end
  return t1
end

function table.pack(...)
  return { n = select("#", ...), ... }
end

function table.pos(t, s)
  for k, v in pairs(t) do
    if v == s then
      return k
    end
  end
  return 0 -- Not a valid pos.
end

function table.print(t)
  print ("========================")
  print ("PRINTING TABLE:")
  for index, value in pairs(t) do
    print (("[%s] %s"):format(tostring(index), tostring(value)))
  end
  print ("========================")
end

function table.remove_value(t, v)
  table.remove(t, table.pos(t, v))
end

function table.getKeys(t)
  local t2 = {}
  for k, v in pairs(t) do
    table.insert(t2, k)
  end
  return t2
end

function table.getValues(t)
  local t2 = {}
  for k, v in pairs(t) do
    table.insert(t2, v)
  end
  return t2
end

function average(...)
  local args = table.pack(...)
  if args.n > 0 then
    local sum = 0
    for i = 1, args.n do
      sum = sum + args[i]
    end
    return sum / args.n
  end
end

function swap(a, b)
  local _a = a
  a, b = b, _a
  return a, b
end

function Display(MSG)
  local DisplayBox = Object_Create("TMessageBox")
  DisplayBox.Button, DisplayBox.Icon = 0, 4
  DisplayBox.Show(MSG)
end

-- ---------------------------
-- Journal functions
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
Journal = { _ref = UO.ScanJournal(0), _list = {}, _count = 0, idx = nil }

-- ---------------------------
-- # Journal.check()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Journal:check()
  local JournalCnt = 0
  Journal._ref, JournalCnt = UO.ScanJournal(Journal._ref)
  dbg_ifprint(Debug.Journal, ("Journal.check() -> ref: %s; new count: %d"):format(Journal._ref, JournalCnt))
  for i = JournalCnt - 1, 0, -1 do
    local Line = UO.GetJournal(i)
    table.insert(Journal._list, Line)
  end
  Journal._count = Journal._count + JournalCnt
end

-- ---------------------------
-- # Journal:getEntry()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Journal:getEntry(n)
  local JournalEntry = Journal._list[n]
  dbg_ifprint(Debug.Journal, ("Journal:getEntry() -> %s"):format(JournalEntry))
  return JournalEntry
end

-- ---------------------------
-- # Journal:EntryCount()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Journal:EntryCount()
  Journal:check()
  return Journal._count
end

-- ---------------------------
-- # Journal:FindEntry()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Journal:FindEntry (Entry)
  local idx = Bot.JournalIndex
  local count = Journal:EntryCount()
  dbg_ifprint(Debug.Journal, ("Journal:FindEntry() -> idx: %d; count: %d"):format(idx, count))
  while (idx < count) do
    idx = idx + 1
    if Journal:getEntry(idx):match(Entry) then
      return true
    end
  end
  return false
end

-- ---------------------------
-- # FindItem
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
FindItem = {
  __Clear = 0,
  __ID = 1,
  __Type = 2,
  __Container = 3,
  __Ground = 4,
  __None = 5
}

function FindItem:Filter2Str(idx)
  local Filters = { "CLEAR", "ID (additive)", "TYPE (additive)", "CONTAINER", "GROUND", "NONE" }
  return Filters[idx+1]
end

FindItem.Internal = { visibleOnly = true, doRefresh = true, RefreshNest = 0, count = 0 }

function FindItem:init()
  FindItem.Item = {}
  FindItem.Index = 1
  FindItem.Count = 0
end

function FindItem:get(idx)
  idx = idx or FindItem.Index
  return FindItem.Item[idx]
end

function FindItem:Applyfilter(filter, ...)
  local args = table.pack(...)
  FindItem.Internal.count = UO.FilterItems(filter, ...)
  dbg_ifprint(Debug.FindItem, ("FindItem.Applyfilter() -> @Filter: %s"):format(FindItem:Filter2Str(filter)))
  dbg_ifprint(Debug.FindItem and args.n > 0, ("FindItem.Applyfilter() -> @Value: %d"):format(args[1]))
  dbg_ifprint(Debug.FindItem, ("FindItem.Applyfilter() ->  ^ Updated item count: %d"):format(FindItem.Internal.count))
end

function FindItem.Internal:handler(filter, ...)
  if FindItem.Internal.doRefresh then
    dbg_ifprint(Debug.FindItem, "FindItem.Internal.handler() -> calling UO.ScanItems()")
    FindItem.Internal.count = UO.ScanItems (FindItem.Internal.visibleOnly)
    FindItem.Internal.visibleOnly = true
  else
    dbg_ifprint(Debug.FindItem, "FindItem.Internal.handler() -> clearing filter.")
    FindItem.Internal.count = UO.FilterItems (FindItem.__Clear)
  end
    if not (filter == FindItem.__None) then
    FindItem:Applyfilter(filter, ...)
  end
end

-- ---------------------------
-- # FindItem.isIgnored()
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~
function FindItem:isIgnored (IDType)
  return IgnoreItem:Ignoring (IDType) or IgnoreItem.Local:Ignoring (IDType)
end

function FindItem:AddtoList()
  for i = 0, FindItem.Internal.count - 1 do
    local nID, nType, nKind, nContID, nX, nY, nZ, nStack, nRep, nCol = UO.GetItem(i)
    if not FindItem:isIgnored (nID) and not FindItem:isIgnored (nType) then
      dbg_ifprint(Debug.FindItem, ("FindItem.AddtoList() -> Inserting: %d in items list."):format(nID))
      table.insert(FindItem.Item, {ID = nID, Type = nType, Kind = nKind, ContID = nContID, X = nX, Y = nY, Z = nZ,
        Stack = nStack, Rep = nRep, Col = nCol})
      FindItem.Count = FindItem.Count + 1
    end
  end
end

function FindItem:All()
  FindItem:init()
  FindItem.Internal:handler(FindItem.__None)
  FindItem:AddtoList()
end

function FindItem:Cont(Container, doList)
  FindItem:init()
  dbg_ifprint(Debug.FindItem, ("FindItem:Cont() -> Container: %d"):format(Container))
  FindItem.Internal:handler(FindItem.__Container, Container)
  if doList then
    FindItem:AddtoList()
  end
end

function FindItem:Ground(Distance, doList)
  local Distance = Distance or 2
  FindItem:init()
  dbg_ifprint(Debug.FindItem, ("FindItem:Ground() -> Distance: %d"):format(Distance))
  FindItem.Internal:handler(FindItem.__Ground, Distance)
  if doList then
    FindItem:AddtoList()
  end
end

function FindItem:Type(Type)
  FindItem:init()
  for k, v in pairs(Type) do
    FindItem:Applyfilter(FindItem.__Type, v)
  end
  FindItem:AddtoList()
end

function FindItem:ID(ID)
  FindItem:init()
  for k, v in pairs(ID) do
    FindItem:Applyfilter(FindItem.__ID, v)
  end
  FindItem:AddtoList()
end
