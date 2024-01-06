"""
Author:     Vince Black
Date:       1/4/2024
Brief:      Cemu hook client 
"""

macHex = "000000000001"  # server mac address, hex format, e.g., ff:aa:bb:00:55:77 should be "ffaabb005577"
serverAddressPort = ("192.168.1.6", 26760)
update_interval = 0.15 # update the data once in an interval (unit seconds), seems too small value causing problem 
CONTROL_MOUSE = True  # use your gyroscope to control your mouse
OUTPUT_GYRO_INFO = False  # verbal on gyroscope data
OUTPUT_DSU_PACKAGE = False # verbal on all data received, including the whole dsu package

VERTICAL_SENSITIVITY = 4.0
HORIZONTAL_SENSITIVITY = 4.8

SLOW_MOVE_FACTOR = 0.4
SLOW_THRESHOLD = 20