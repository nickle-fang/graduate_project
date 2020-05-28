import threading
import time
import SerialCom as sc


class Cmdsend:
    x_cmd = 0
    y_cmd = 0
    r_cmd = 0
    kickpower_cmd = 0
    angle_cmd = 0

    shoot_flag = 0   # shoot:0   chip:1
    drib_flag = 0    # drib:1    stop:0

    state_flag = 0    # angle:0  zheng:1  fan:2
    
    
def sign(x):
    if (x >= 0):
        return 0
    else:
        return 1


def pack():
    global tx_data

    tx_data[0] = 0x08
    tx_data[1] = (Cmdsend.state_flag << 4) | Cmdsend.drib_flag

    tx_data[2] = ((abs(Cmdsend.x_cmd) & 0xff00) >> 8) | (sign(Cmdsend.x_cmd) << 7)
    tx_data[3] = abs(Cmdsend.x_cmd) & 0xff

    tx_data[4] = ((abs(Cmdsend.y_cmd) & 0xff00) >> 8) | (sign(Cmdsend.y_cmd) << 7)
    tx_data[5] = abs(Cmdsend.y_cmd) & 0xff

    # TODO:
    tx_data[6] = 0
    tx_data[7] = 0

    # TODO:
    tx_data[8] = 0

    tx_data[9] = 0




def laser_task():
    global disdata
    mylaser = sc.Revlaser()

    while True:
        disdata = mylaser.readlaser()
        # print(disdata)
        # time.sleep(1)


def rev_task():
    global rx_data
    myrev = sc.H7com()

    while True:
        temp = myrev.readh7()
        if(len(temp) == 5):
            for i in range(5):
                rx_data.append(temp[i])
        else:
            print("fxxk")


def sendcmd_task():
    global tx_data
    mysend = sc.H7com()

    while True:
        mysend.sendcmd(tx_data)
        time.sleep(0.016)


def main_task():
    global disdata
    global rx_data
    global tx_data

    while True:
        pack()
        print("main", disdata)
        print("main", rx_data)
        time.sleep(0.5)


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
    disdata = 0
    tx_data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    rx_data = []
    main()
