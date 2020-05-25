import time
import serial


class Revlaser:

    def __init__(self):
        self.lasercom = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5)
    
    def readlaser(self):
        # read the serial data
        # self.lasercom.inWaiting()
        laser_data = self.lasercom.read(19)

        # decode the data
        laser_data_decode = laser_data.decode('utf-8')

        # get the distance data
        distance_raw = laser_data_decode[9:13]
        # print('debug', distance_raw)
        try:
            distance = int(distance_raw, 16) / 1000
            # print("task", distance)
            return distance
        except:
            return 0


class H7com:

    def __init__(self):
        self.h743com = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)

    def readh7(self):
        try:
            # self.h743com.inWaiting()
            rx_data_raw = self.h743com.read(5)

            rx_data_raw_decode = rx_data_raw.decode('utf-8')
           # print("test1", rx_data_raw_decode)
            return rx_data_raw_decode
            # print("sc", rx_data)
        except:
            print("err")
            return 0

    def sendcmd(self, tx_data):
        self.h743com.write(tx_data.encode())
