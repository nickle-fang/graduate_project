class Cmdsend:
    x_cmd = 0   # 1 cm/s
    y_cmd = 0
    r_cmd = 0   # 1 rad/s
    kickpower_cmd = 0
    angle_cmd = 0   # rad:range from -pi to pi

    shoot_flag = 0   # shoot:0   chip:1
    drib_flag = 0    # drib:1    stop:0

    state_flag = 1    # angle:0  zheng:1  fan:2


class Datarev:
    infrared = 0   # 1:triggered  0:not
    chipped = 0
    shooted = 0
    battery = 0
    imu_angle = 0
    robot_num = 0
    angle_precise = 0.0


class Laser:
    disdata = 0.0
