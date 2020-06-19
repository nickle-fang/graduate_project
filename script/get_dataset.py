from picamera import PiCamera
import time


if __name__ == "__main__":

    camera = PiCamera()
    camera.rotation = 180

    for i in range(100):
        print("3 seconds..............")
        time.sleep(1.5)
        print("2 seconds........")
        time.sleep(1.5)
        print("1 second.")
        time.sleep(1.5)

        camera.capture('/home/pi/Desktop/dataset_test/%s.jpg' % (i+400))
        print("photo taken!!!", i)
