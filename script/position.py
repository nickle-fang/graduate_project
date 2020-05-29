import data_define as info
import math
import time


class Pos:
    x = 0.0
    y = 0.0


def measure_pos():
    info.Cmdsend.x_cmd = 0
    info.Cmdsend.y_cmd = 0
    info.Cmdsend.r_cmd = 0
    info.Cmdsend.kickpower_cmd = 0
    info.Cmdsend.shoot_flag = 0
    info.Cmdsend.drib_flag = 0
    info.Cmdsend.state_flag = 0

    info.Cmdsend.angle_cmd = math.pi / 2
    # wait until angle is set
    while(abs(info.Cmdsend.angle_cmd * 180 / math.pi - info.Datarev.angle_precise) > 1):
        pass
    Pos.x = info.Laser.disdata
    info.Cmdsend.angle_cmd = math.pi
    # wait until angle is set
    while(abs(info.Cmdsend.angle_cmd * 180 / math.pi - info.Datarev.angle_precise) > 1):
        pass
    Pos.y = info.Laser.disdata


def adjust_orientation(x_set, y_set):
    info.Cmdsend.x_cmd = 0
    info.Cmdsend.y_cmd = 0
    info.Cmdsend.r_cmd = 0
    info.Cmdsend.kickpower_cmd = 0
    info.Cmdsend.shoot_flag = 0
    info.Cmdsend.drib_flag = 0
    info.Cmdsend.state_flag = 0

    if (x_set != Pos.x):
        theta = math.atan(abs(y_set - Pos.y) / abs(x_set - Pos.x))
    else:
        x_set = Pos.x + 0.001

    if (((y_set - Pos.y) > 0) and ((x_set - Pos.x) > 0)):
        info.Cmdsend.angle_cmd = - theta
    elif (((y_set - Pos.y) > 0) and ((x_set - Pos.x) < 0)):
        info.Cmdsend.angle_cmd = (math.pi / 2 - theta)
    elif (((y_set - Pos.y) < 0) and ((x_set - Pos.x) < 0)):
        info.Cmdsend.angle_cmd = math.pi + theta
    elif (((y_set - Pos.y) < 0) and ((x_set - Pos.x) > 0)):
        info.Cmdsend.angle_cmd = - (theta + math.pi / 2)
    
    else:
        pass


def go_to_position(x_set, y_set):
    info.Cmdsend.state_flag = 1

    length = math.sqrt((x_set - Pos.x)*(x_set - Pos.x) + (y_set - Pos.y)*(y_set-Pos.y))
    max_speed = 0.5
    near_speed = 0.2
    if (length <= 2.75):
        stay_time = length / near_speed
        info.Cmdsend.x_cmd = near_speed
        time.sleep(stay_time)
    else:
        acc = 0.05
        change_time = 0.5
        up_length = ((acc + 0.5) * (0.5 / acc) * change_time) / 2
        stay_time = (length - (2 * up_length)) / max_speed

        while (info.Cmdsend.x_cmd < max_speed):
            info.Cmdsend.x_cmd = info.Cmdsend.x_cmd + acc
            time.sleep(0.5)

        info.Cmdsend.x_cmd = max_speed
        time.sleep(stay_time)

        while (info.Cmdsend.x_cmd > 0):
            info.Cmdsend.x_cmd = info.Cmdsend.x_cmd - acc
            time.sleep(0.5)
    
    info.Cmdsend.x_cmd = 0


def stop():
    info.Cmdsend.x_cmd = 0
    info.Cmdsend.y_cmd = 0
    info.Cmdsend.r_cmd = 0
    info.Cmdsend.kickpower_cmd = 0
    info.Cmdsend.shoot_flag = 0
    info.Cmdsend.drib_flag = 0
    info.Cmdsend.state_flag = 1
    info.Cmdsend.angle_cmd = 0


def navigation_mission():
    measure_pos()
    print("The position now is", Pos.x, Pos.y)
    x_set, y_set = input("Please set the destination:")

    while (math.sqrt((x_set - Pos.x)*(x_set - Pos.x) + (y_set - Pos.y)*(y_set-Pos.y))) > 0.05:
        adjust_orientation(x_set, y_set)
        time.sleep(1)

        go_to_position(x_set, y_set)
        time.sleep(1)

        measure_pos()

    stop()
