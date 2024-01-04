"""
Author:     Vince Black
Date:       1/4/2024
Brief:      Cemu hook client 
"""

# only things you need to configure is mac and server address & port.
macHex = "000000000001"  # server mac address, hex format, e.g., ff:aa:bb:00:55:77 should be "ffaabb005577"
serverAddressPort = ("192.168.1.6", 26760)


import socket
import time
from struct import *



request_body = "44535543e9030c00b8d74153c7aad276020010000200" 
byte_array = bytes.fromhex(request_body + macHex)


bufferSize = 1024

def parse_dsu_response(data:bytes):
    print("======================================================")
    # header = data[:20]
    # res = unpack('<ccccHHIII', header)
    # magic = res[:4]
    # version = res[4]
    # length  = res[5]
    # crc32   = res[6]
    # serverId= res[7]
    # messageType    = res[8]
    # print("magic: {}\nversion:{}\nserverId:{}\nmessageType:{}".format(magic, version, serverId, hex(messageType)))

    # if (messageType != 1048578):
    #     print("Not supported message type")
    #     exit(-1)


    # shared_part = data[20:31]
    # res = unpack('<BBBBBBBBBBB', shared_part)
    # slotId     = res[0]
    # slotState  = "not connected" if res[1] == 0 else \
    #                 "connected" if res[1] == 2 else \
    #                 "reserved"
    # deviceMode = "not applicable" if res[2] == 0 else \
    #                 "no or partial gyro" if res[2] == 1 else\
    #                 "full gyro" if res[2] == 2 else\
    #                 "invalid value" 
    # connectType= "not applicable" if res[3] == 0 else\
    #                 "USB" if res[3] == 1 else\
    #                 "bluetooth" if res[3] == 2 else\
    #                 "invalid value"
    # macAddress = list(map(hex, res[4:10]))
    # battery    = "not applicable" if res[10] == 0 else\
    #                 "dying" if res[10] == 1 else\
    #                 "low" if res[10] == 2 else\
    #                 "medium" if res[10] == 3 else\
    #                 "high" if res[10] == 4 else\
    #                 "full" if res[10] == 5 else\
    #                 "charging" if res[10] == 238 else\
    #                 "charged" if res[10] == 239 else\
    #                 "invalid value"
    # print("slotId: {}\nslotState: {}\ndeviceMode: {}\nconnectType: {}\nmacAddress: {}\nbattery: {}\n".format(
    #     slotId,
    #     slotState,
    #     deviceMode,
    #     connectType,
    #     macAddress,
    #     battery
    # ))
    controller_data_part = data[31:111]

    res = tuple(unpack('<BIBBBBBBBBBBBBBBBBBBBBIHIHQffffff', controller_data_part))
    gyro_pitch = res[-3]
    gyro_yaw = res[-2]
    gyro_roll = res[-1]
    # print("Accelerometer X axis: {}\nAccelerometer Y axis: {}\nAccelerometer Z axis: {}\nGyroscope pitch: {}\nGyroscope yaw: {}\nGyroscope roll: {}".format(
    #     res[-6],
    #     res[-5],
    #     res[-4],
    #     gyro_pitch,
    #     gyro_yaw,
    #     gyro_roll
    # ))
    if abs(gyro_pitch) < 10:
        print("静止 速度:{:.1f} ".format(abs(gyro_pitch)))
    elif gyro_pitch > 0:
        print("抬头 速度:{:.1f}".format(abs(gyro_pitch)))
    else:
        print("低头 速度:{:.1f}".format(abs(gyro_pitch)))
    
    if abs(gyro_yaw) < 10:
        print("无旋转 速度:{:.1f}".format(abs(gyro_yaw)))
    elif gyro_yaw > 0:
        print("右转 速度:{:.1f}".format(abs(gyro_yaw)))
    else:
        print("左转 速度:{:.1f}".format(abs(gyro_yaw)))

    if abs(gyro_roll) < 10:
        print("无翻滚 速度:{:.1f}".format(abs(gyro_roll)))
    elif gyro_roll > 0:
        print("右歪头 速度:{:.1f}".format(abs(gyro_roll)))
    else:
        print("左歪头 速度:{:.1f}".format(abs(gyro_roll)))
    print()

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
        if (current_time - last_parse_time > 0.8):
            parse_dsu_response(msg_from_server[0])
            last_parse_time = current_time


if __name__ == '__main__':
    main()