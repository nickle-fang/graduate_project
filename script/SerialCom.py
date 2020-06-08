import time
import serial
import data_define as info


class Revlaser:

    def __init__(self):
        self.lasercom = serial.Serial('/dev/ttyS0', 115200, timeout=0.5)
    
    def readlaser(self):
        # read the serial data
        # self.lasercom.inWaiting()
        laser_data = self.lasercom.read(19)
        try:
            # decode the data
            laser_data_decode = laser_data.decode('utf-8')

            # get the distance data
            distance_raw = laser_data_decode[9:13]
            # print('debug', distance_raw)
            distance = int(distance_raw, 16) / 1000.0
            # print("task", distance)
            return distance
        except:
            # print("err")
            return 0


class H7com:

    def __init__(self):
        self.h743com = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

    def readh7(self):
        # try:
        # self.h743com.inWaiting()
        # rx_data_raw_decode = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        rx_data_raw = self.h743com.read(6)

        # print("test1", rx_data_raw)
        # print("omgomg", rx_data_raw)
        # print("test2", type(rx_data_raw))

        # rx_data_raw_decode = rx_data_raw.decode('utf-8')
        # print("test1", rx_data_raw_decode)
        # print(rx_data_raw_decode)
        try:
            angle = rx_data_raw[4] + (rx_data_raw[3] * 256)
            if (angle > 32767):
                angle = angle - 65536
            # print("angle", angle/100)
            info.Datarev.angle_precise = angle / 100.0
            return rx_data_raw
        except:
            return 0
        # print("sc", rx_data)

    def sendcmd(self, tx_data):
        # tx_str = str(tx_data)
        # self.h743com.write(tx_str.encode())
        self.h743com.write(tx_data)
