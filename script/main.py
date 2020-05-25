import threading
import time
import SerialCom as sc


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
    tx_data = "12345"
    rx_data = []
    main()
