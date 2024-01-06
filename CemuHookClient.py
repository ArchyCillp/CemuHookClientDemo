"""
Author:     Vince Black
Date:       1/4/2024
Brief:      Cemu hook client 
"""
from config import *
import socket
import time
from struct import *
import pyautogui
import pydirectinput
if CONTROL_MOUSE: import win32api, win32con

request_body = "44535543e9030c00b8d74153c7aad276020010000200" 
byte_array = bytes.fromhex(request_body + macHex)


bufferSize = 1024

def parse_dsu_response(data:bytes):
    if OUTPUT_DSU_PACKAGE:
        print("======================================================")
        header = data[:20]
        res = unpack('<ccccHHIII', header)
        magic = res[:4]
        version = res[4]
        length  = res[5]
        crc32   = res[6]
        serverId= res[7]
        messageType    = res[8]
        print("magic: {}\nversion:{}\nserverId:{}\nmessageType:{}".format(magic, version, serverId, hex(messageType)))

        if (messageType != 1048578):
            print("Not supported message type")
            exit(-1)


        shared_part = data[20:31]
        res = unpack('<BBBBBBBBBBB', shared_part)
        slotId     = res[0]
        slotState  = "not connected" if res[1] == 0 else \
                        "connected" if res[1] == 2 else \
                        "reserved"
        deviceMode = "not applicable" if res[2] == 0 else \
                        "no or partial gyro" if res[2] == 1 else\
                        "full gyro" if res[2] == 2 else\
                        "invalid value" 
        connectType= "not applicable" if res[3] == 0 else\
                        "USB" if res[3] == 1 else\
                        "bluetooth" if res[3] == 2 else\
                        "invalid value"
        macAddress = list(map(hex, res[4:10]))
        battery    = "not applicable" if res[10] == 0 else\
                        "dying" if res[10] == 1 else\
                        "low" if res[10] == 2 else\
                        "medium" if res[10] == 3 else\
                        "high" if res[10] == 4 else\
                        "full" if res[10] == 5 else\
                        "charging" if res[10] == 238 else\
                        "charged" if res[10] == 239 else\
                        "invalid value"
        print("slotId: {}\nslotState: {}\ndeviceMode: {}\nconnectType: {}\nmacAddress: {}\nbattery: {}\n".format(
            slotId,
            slotState,
            deviceMode,
            connectType,
            macAddress,
            battery
        ))
    controller_data_part = data[31:111]

    res = tuple(unpack('<BIBBBBBBBBBBBBBBBBBBBBIHIHQffffff', controller_data_part))
    gyro_pitch = res[-3]
    gyro_yaw = res[-2]
    gyro_roll = res[-1]

    if OUTPUT_DSU_PACKAGE:
        print("Accelerometer X axis: {}\nAccelerometer Y axis: {}\nAccelerometer Z axis: {}\nGyroscope pitch: {}\nGyroscope yaw: {}\nGyroscope roll: {}".format(
            res[-6],
            res[-5],
            res[-4],
            gyro_pitch,
            gyro_yaw,
            gyro_roll
        ))
    if OUTPUT_GYRO_INFO:    
        if abs(gyro_pitch) < 10:
            print("Static speed:{:.1f} ".format(abs(gyro_pitch)))
        elif gyro_pitch > 0:
            print("Head up speed:{:.1f}".format(abs(gyro_pitch)))
        else:
            print("Head down speed:{:.1f}".format(abs(gyro_pitch)))
        
        if abs(gyro_yaw) < 10:
            print("Static speed:{:.1f}".format(abs(gyro_yaw)))
        elif gyro_yaw > 0:
            print("Turn right speed:{:.1f}".format(abs(gyro_yaw)))
        else:
            print("Turn left speed:{:.1f}".format(abs(gyro_yaw)))

        if abs(gyro_roll) < 10:
            print("Static speed:{:.1f}".format(abs(gyro_roll)))
        elif gyro_roll > 0:
            print("Right roll speed:{:.1f}".format(abs(gyro_roll)))
        else:
            print("Left roll speed:{:.1f}".format(abs(gyro_roll)))
        print()
    return gyro_pitch, gyro_yaw, gyro_roll

MOVE_MODE = 0
def move_mode_det(gyro_pitch, gyro_yaw, gyro_roll):
    global MOVE_MODE
    print(gyro_yaw, gyro_pitch)
    if abs(gyro_yaw) > FAST_THRESHOLD or abs(gyro_pitch) > FAST_THRESHOLD:
        MOVE_MODE = 1
    elif abs(gyro_yaw) < SLOW_THRESHOLD and abs(gyro_pitch) < SLOW_THRESHOLD:
        MOVE_MODE = 0
    
def moveMouse(gyro_pitch, gyro_yaw, gyro_roll):
    if MOVE_MODE == 0:
        pitch_speed = -VERTICAL_SENSITIVITY * SLOW_MOVE_FACTOR 
        yaw_speed = HORIZONTAL_SENSITIVITY * SLOW_MOVE_FACTOR
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(gyro_yaw * yaw_speed), int(gyro_pitch * pitch_speed),0,0)
        print("debug move slow\t\t{} {}".format(int(gyro_yaw * yaw_speed), int(gyro_pitch * pitch_speed)))
    else:
        pitch_speed = -VERTICAL_SENSITIVITY 
        yaw_speed = HORIZONTAL_SENSITIVITY
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(gyro_yaw * yaw_speed), int(gyro_pitch * pitch_speed),0,0)
        print("debug move fast\t\t{} {}".format(int(gyro_yaw * yaw_speed), int(gyro_pitch * pitch_speed)))


def main():
    # Create a UDP socket at client side
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_client_socket.settimeout(3)
    last_parse_time = 0
    # Send to server using created UDP socket
    while 1:
        udp_client_socket.sendto(byte_array, serverAddressPort)

        msg_from_server = udp_client_socket.recvfrom(bufferSize)

        current_time = time.time()
        smooth = 50
        if (current_time - last_parse_time > update_interval):
            res = parse_dsu_response(msg_from_server[0])
            if CONTROL_MOUSE:
                move_mode_det(*res)
                moveMouse(*res)
            last_parse_time = current_time


if __name__ == '__main__':
    main()