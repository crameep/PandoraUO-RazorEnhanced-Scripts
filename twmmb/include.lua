-- ;==================================
-- ; TWMMB External Libraries
-- ;==================================
setfenv(1, TWMMB)

--[[
    IntToSys26()
    Author: Cheffe
--]]
function IntToSys26(i)
  local i, s = Bit.Xor(i, 69) + 7,""
  repeat
    s = s..s.char(65 + i % 26)
    i = math.floor(i / 26)
  until i < 1
  return s
end 

--[[
    Sys26ToInt()
    Author: Cheffe
--]]
function Sys26ToInt(s)
  local s, r = s:upper(), 0
  for i = #s, 1, -1 do
    r = r * 26 + s:byte(i) - 65
  end
  return Bit.Xor(r - 7, 69)
end

--[[
    getObjectName()
    Author: Cheffe
--]]
function getObjectName(object)
  local objName = UO.Property(object)
  return objName:match("%s(.+)%s")
end

--[[
    getObjectProperty()
    Author: Cheffe
--]]
function getObjectProperty(object, idx)
  local objName, objInfo = UO.Property(object)
  objInfo = "\r\n" .. objInfo
  local i = 0
  for s, n in objInfo:gmatch("%c+([^%c]-)%s([%d%.]+)") do
    i = i + 1
    if i == idx then
      return n
    end
  end
end
