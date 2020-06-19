# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import data_define as info
import position as posi


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


# def getposHsv(event,x,y,flags,param):
#     if event==cv2.EVENT_LBUTTONDOWN:
#         # return [y, x]
#         print("HSV is", img_hsv[y,x])


def show_image():
# if __name__ == "__main__":
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time_count = 0.0
    time_num = 0

    # define the ball color space
    lower_orange = np.array([0, 235, 100])
    upper_orange = np.array([17, 255, 255])
    
    # allow the camera to warmup
    time.sleep(0.1)
    
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        time_start = time.time()
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # rotate the image
        img_rotate = rotate_bound(image, 180)

        # Guess Processing
        img_rotate_guess = cv2.GaussianBlur(img_rotate, (11, 11), 0)

        img_guess_hsv = cv2.cvtColor(img_rotate_guess, cv2.COLOR_BGR2HSV)
        img_hsv = cv2.cvtColor(img_rotate, cv2.COLOR_BGR2HSV)

        mask_o = cv2.inRange(img_hsv, lower_orange, upper_orange)
        mask_o_guess = cv2.inRange(img_guess_hsv, lower_orange, upper_orange)
    
        # show the frame
        cv2.imshow("Frame", img_rotate)
        cv2.imshow("Frame_guess", img_rotate_guess)
        cv2.imshow("imageHSV", img_hsv)
        cv2.imshow("mask", mask_o)
        cv2.imshow("mask_guess", mask_o_guess)
        # cv2.setMouseCallback("imageHSV", getposHsv)
        time_end = time.time()
        time_count = time_count + (time_end - time_start)
        time_num = time_num + 1
        if (time_num == 10):
            # print("fps = ", 10 / time_count)
            time_num = 0
            time_count = 0     
        key = cv2.waitKey(1) & 0xFF
    
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
    
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break


def detect_ball():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # define the ball color space
    lower_orange = np.array([0, 235, 100])
    upper_orange = np.array([17, 255, 255])

    # allow the camera to warmup
    time.sleep(0.1)

    ball_mid_flag = 0

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # rotate the image
        img_rotate = rotate_bound(image, 180)

        # Guess Processing
        img_rotate_guess = cv2.GaussianBlur(img_rotate, (11, 11), 0)

        # transfer to hsv space
        # img_hsv = cv2.cvtColor(img_rotate, cv2.COLOR_BGR2HSV)
        img_hsv_guess = cv2.cvtColor(img_rotate_guess, cv2.COLOR_BGR2HSV)

        # keep the orange
        # mask_o = cv2.inRange(img_hsv, lower_orange, upper_orange)
        mask_o_guess = cv2.inRange(img_hsv_guess, lower_orange, upper_orange)

        # mask lvbo
        # mask_1 = cv2.erode(mask_o_guess, None, iterations=2)
        # mask_2 = cv2.erode(mask_1, None, iterations=2)

        # keep the ball
        # res = cv2.bitwise_and(img_rotate, img_rotate, mask=mask_o)
        # res_guess = cv2.bitwise_and(img_rotate, img_rotate, mask=mask_o_guess)

        # cv2.imshow("mask", mask_o)
        # cv2.imshow("mask_guess", mask_o_guess)
        # cv2.imshow("mask_1", mask_1)
        # cv2.imshow("mask_2", mask_2)
        # cv2.imshow("rest", res_guess)
        # cv2.imshow("raw", img_rotate)
        # cv2.imshow("guess_raw", img_rotate_guess)

        # find the contour
        cnts = cv2.findContours(mask_o_guess.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        find_ball_flag = len(cnts)

        if find_ball_flag:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            print("Center", round(x), round(y))
            # M = cv2.moments(c)
            # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # print("center", center)
            print("The ball radius is", radius)
            if (put_ball_mid(x, y)):
                ball_mid_flag = 1
                get_ball()
            # stop()
        else:
            # stop()
            search_ball()
            print("Finding the ball......")

        # if (ball_mid_flag):
            # get_ball()

        # cv2.drawContours(img_rotate, cnts, -1, (0,255,0), 2)
        # cv2.imshow("raw", img_rotate)
    
        # key = cv2.waitKey(1) & 0xFF
    
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
    
        # if the `q` key was pressed, break from the loop
        # if key == ord("q"):
        #     break


def get_sign(num):
    if num < 0:
        return 1
    else:
        return 0


def get_ball():
    info.Cmdsend.x_cmd = 10
    info.Cmdsend.y_cmd = 0
    info.Cmdsend.r_cmd = 0
    info.Cmdsend.kickpower_cmd = 0
    info.Cmdsend.angle_cmd = 0
    info.Cmdsend.shoot_flag = 0
    info.Cmdsend.drib_flag = 1
    info.Cmdsend.state_flag = 1

    while (info.Datarev.infrared != 1):
        pass

    if (info.Datarev.infrared == 1):
         info.Cmdsend.x_cmd = 0
         info.Cmdsend.drib_flag = 1
         time.sleep(2)
         shoot()


def shoot():
    posi.adjust_orientation(0.1, 2)
    time.sleep(2)


    info.Cmdsend.x_cmd = 0
    info.Cmdsend.y_cmd = 0
    info.Cmdsend.r_cmd = 0
    info.Cmdsend.kickpower_cmd = 30
    info.Cmdsend.angle_cmd = 0
    info.Cmdsend.shoot_flag = 0
    info.Cmdsend.drib_flag = 1
    info.Cmdsend.state_flag = 1

    time.sleep(2)
    info.Cmdsend.kickpower_cmd = 0

def put_ball_mid(x, y):
    x_diff = x - 320

    if get_sign(x_diff):
        temp = 1
    else:
        temp = 2

    if (x_diff > -50) and (x_diff < 50):
        x_diff = 0
    else:
        x_diff = 1

    info.Cmdsend.x_cmd = 0
    info.Cmdsend.y_cmd = 0
    info.Cmdsend.r_cmd = 0.3
    info.Cmdsend.kickpower_cmd = 0
    info.Cmdsend.angle_cmd = 0
    info.Cmdsend.shoot_flag = 0
    info.Cmdsend.drib_flag = 0
    info.Cmdsend.state_flag = temp

    if x_diff == 0:
        info.Cmdsend.r_cmd = 0
        info.Cmdsend.drib_flag = 1
        return 1
    else:
        return 0


def search_ball():
    info.Cmdsend.x_cmd = 0
    info.Cmdsend.y_cmd = 0
    info.Cmdsend.r_cmd = 0.7
    info.Cmdsend.kickpower_cmd = 0
    info.Cmdsend.angle_cmd = 0
    info.Cmdsend.shoot_flag = 0
    info.Cmdsend.drib_flag = 0
    info.Cmdsend.state_flag = 1


def stop():
    info.Cmdsend.x_cmd = 0
    info.Cmdsend.y_cmd = 0
    info.Cmdsend.r_cmd = 0
    info.Cmdsend.kickpower_cmd = 0
    info.Cmdsend.angle_cmd = 0
    info.Cmdsend.shoot_flag = 0
    info.Cmdsend.drib_flag = 0
    info.Cmdsend.state_flag = 1


if __name__ == "__main__":
    # show_image()
    detect_ball()

# info command send
#     x_cmd = 0   # 1 cm/s
#     y_cmd = 0
#     r_cmd = 0   # 1 rad/s
#     kickpower_cmd = 0
#     angle_cmd = 0   # rad:range from -pi to pi

#     shoot_flag = 0   # shoot:0   chip:1
#     drib_flag = 0    # drib:1    stop:0

#     state_flag = 0    # angle:0  zheng:1  fan:2
