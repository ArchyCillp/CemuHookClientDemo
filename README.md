# Cemu Hook Client & gyroscope mouse
## Purpose
The python program provides you the real-time gyroscope data from your phone. You can also use gyroscope to control your mouse, like a remote control device.

作用：把手机绑在头上，可以用头控制鼠标

## Steps
1. Install net.sshnuke.dsu.MotionSource-1.1.2.apk on your phone to make your phone as server to provide real-time gyroscope data.
2. Open the app and configure as shown in 'README after you install the apk.png'
3. Open config.py, configure macHex and serverAddressPort.
4. In terminal, run 'python CemuHookClient.py' 
5. If you close your phone screen for a while and do not turn on client, the server might shut down. 
6. If you want to use your phone to control the mouse, set CONTROL_MOUSE = True. You need to install pywin32 firstly.
