; 

` & f:: 
SendInput, {LButton down}
KeyWait, f
SendInput, {LButton up}
return

` & j:: 
SendInput, {RButton down}
KeyWait, j
SendInput, {RButton up} 
return


; Map a hotkey, such as F1, to reset the mouse pointer to the center of the screen
!F5::
CoordMode, Mouse, Screen
SysGet, MonitorCount, MonitorCount

SysGet, Monitor, Monitor
CenterX := (MonitorRight - MonitorLeft) / 2 + MonitorLeft
CenterY := (MonitorBottom - MonitorTop) / 2 + MonitorTop
MouseMove, CenterX, CenterY, 0

return