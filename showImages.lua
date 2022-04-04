print("Image Display Program")

function input(text)
  term.write(text)
  return read()
end

function dump(o)
   if type(o) == 'table' then
      local s = '{\n'
      for k,v in pairs(o) do
         if type(k) ~= 'number' then k = '"'..k..'"' end
         s = s .. '['..k..'] = ' .. dump(v) .. ',\n'
      end
      return s .. '} '
   else
      return tostring(o)
   end
end

image = input("Image Name: ")

mode = input("Single or Quad Monitors? (S/Q)")

print("Connected Peripherals: ")
print(dump(peripheral.getNames()))


if mode == "s" or mode == "S" then

  mon = peripheral.wrap(input("Monitor Name: "))
  mon.setTextScale(0.5)
  image = paintutils.loadImage(image .. ".nfp")
  term.redirect(mon)
  shell.run("colorchanger.lua")
  paintutils.drawImage(image,1,1)
  term.redirect(term.native())

else

  mon_tl = peripheral.wrap("monitor_" .. input("Top Left Monitor: monitor_"))
  mon_tl.setTextScale(0.5)
  tl = paintutils.loadImage(image .. "_tl.nfp")
  term.redirect(mon_tl)
  shell.run("colorchanger.lua")
  paintutils.drawImage(tl,1,1)
  term.redirect(term.native())

  mon_tr = peripheral.wrap("monitor_" .. input("Top Right Monitor: monitor_"))
  mon_tr.setTextScale(0.5)
  tr = paintutils.loadImage(image .. "_tr.nfp")
  term.redirect(mon_tr)
  shell.run("colorchanger.lua")
  paintutils.drawImage(tr,1,1)
  term.redirect(term.native())

  mon_bl = peripheral.wrap("monitor_" .. input("Bottom Left Monitor: monitor_"))
  mon_bl.setTextScale(0.5)
  bl = paintutils.loadImage(image .. "_bl.nfp")
  term.redirect(mon_bl)
  shell.run("colorchanger.lua")
  paintutils.drawImage(bl,1,1)
  term.redirect(term.native())

  mon_br = peripheral.wrap("monitor_" .. input("Bottom Right Monitor: monitor_"))
  mon_br.setTextScale(0.5)
  br = paintutils.loadImage(image .. "_br.nfp")
  term.redirect(mon_br)
  shell.run("colorchanger.lua")
  paintutils.drawImage(br,1,1)
  term.redirect(term.native())
end


print("Finished.")
