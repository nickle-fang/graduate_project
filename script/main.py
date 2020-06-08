import threading
import time
import SerialCom as sc
import data_define as info
import position as loc
import cam as cam

def unpack():
    global rx_data
    
    info.Datarev.infrared = (rx_data[1] >> 6) & 0x01
    info.Datarev.chipped = (rx_data[1] >> 4) & 0x01
    info.Datarev.shooted = (rx_data[1] >> 5) & 0x01
    info.Datarev.battery = rx_data[2]
    # info.Datarev.imu_angle = rx_data[3] + (rx_data[4] * 256)
    # if (info.Datarev.imu_angle > 32767):
    #     info.Datarev.imu_angle = info.Datarev.imu_angle - 65536
    # info.Datarev.angle_precise = info.Datarev.imu_angle / 100
    info.Datarev.robot_num = rx_data[5]

    
def sign(x):
    if (x >= 0):
        return 0
    else:
        return 1


def pack():
    global tx_data

    tx_data[0] = 0x08
    tx_data[1] = (info.Cmdsend.state_flag << 4) | info.Cmdsend.drib_flag

    tx_data[2] = ((int(abs(info.Cmdsend.x_cmd)) & 0xff00) >> 8) | (sign(info.Cmdsend.x_cmd) << 7)
    tx_data[3] = int(abs(info.Cmdsend.x_cmd)) & 0xff

    tx_data[4] = (int(abs(info.Cmdsend.y_cmd) & 0xff00) >> 8) | (sign(info.Cmdsend.y_cmd) << 7)
    tx_data[5] = int(abs(info.Cmdsend.y_cmd)) & 0xff

    tx_data[6] = (int(abs(info.Cmdsend.angle_cmd * 40.0)) & 0xff00) >> 8
    tx_data[7] = int(abs(info.Cmdsend.angle_cmd * 40.0)) & 0xff
    tx_data[6] = tx_data[6] | (sign(info.Cmdsend.angle_cmd) << 7)

    tx_data[8] = int(info.Cmdsend.kickpower_cmd)

    tx_data[9] = int(abs(info.Cmdsend.r_cmd) * 40.0)


def laser_task():
    mylaser = sc.Revlaser()

    while True:
        dis_temp = mylaser.readlaser()
        if (dis_temp == 0):
                # print("err")
                pass
        else:
                info.Laser.disdata = dis_temp
        # print(info.Laser.disdata)
        # time.sleep(1)


def rev_task():
    global rx_data
    myrev = sc.H7com()

    while True:
        temp = myrev.readh7()
        # print("hello", temp)
        if(temp != 0):
            for i in range(6):
                rx_data[i] = temp[i]
            unpack()
        #     print(rx_data)    
        
        else:
        #     print("fxxk")
            pass


def sendcmd_task():
    global tx_data
    mysend = sc.H7com()

    while True:
        try:
                pack()
                mysend.sendcmd(tx_data)
                # print("sended", tx_data)
                time.sleep(0.01)
        except:
                # pass
                print("err err err!!!")
                time.sleep(0.05)
        # print("sended", tx_data)


def main_task():
    global rx_data
    global tx_data
    log_file = open('log.txt', mode='w')

#     loc.navigation_mission()
#     cam.detect_ball()

    while True:
        # info.Cmdsend.angle_cmd = 2.66
        # pack()
        # print("main", info.Laser.disdata)
        # unpack()
        # log_file.write(str(rx_data))
        # log_file.write("\n")
        # print("main rx data", rx_data)
        print("main angle", info.Datarev.angle_precise)
        log_file.write(str(info.Datarev.angle_precise))
        log_file.write("\n")
        # print("angle raw", info.Datarev.imu_angle)
        # print("Success!")
        time.sleep(2)


def main():
    # global distance
    # global rx_data
    # global tx_data
    
    laser_thread = threading.Thread(target=laser_task)
    send_thread = threading.Thread(target=sendcmd_task)
    rev_thread = threading.Thread(target=rev_task)
    main_thread = threading.Thread(target=main_task)

    laser_thread.start()
    rev_thread.start()
    send_thread.start()
    main_thread.start()

    while True:
        # the program should not be running here
        pass


if __name__ == '__main__':
    tx_data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    rx_data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    main()
