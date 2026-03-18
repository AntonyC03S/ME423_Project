import time
import math
from machine import I2C, Pin
from servo import Servo, servo2040, CONTINUOUS        # type: ignore
from plasma import WS2812                             # type: ignore
from Servos import Arm, Drivebase                                
from Sensor import Light_sensor                       
from pimoroni import Button                            # type: ignore



print("Scanning I2C...")
arm = Arm(servo2040.SERVO_4, servo2040.SERVO_5, servo2040.SERVO_6)
drive = Drivebase(servo2040.SERVO_1, servo2040.SERVO_2, servo2040.SERVO_3)
sensor = Light_sensor()

time.sleep(3)
sensor.calibrate_imu()
sensor.reset_tracking()
print("\nMove the sensor slowly on the table.\n")


arm_mov =0
spin= 0
move_forward =0
place = 0
user_sw = Button(servo2040.USER_SW)
button = 0
drive_p = 1
while True:
    try:
        x_m, y_m, h_deg = sensor.read_pose_real_m()
        print(
            "x={: .4f} m  y={: .4f} m  h={: .2f} deg".format(
                x_m, y_m, h_deg
            )
        )
    except Exception as e:
        print("Read failed:", e)
    # if drive_p == 1:
    #     drive_p = drive.drive((0,0.05,0), (x_m, y_m, h_deg))
    if user_sw.raw():
        button = 1 #- button

    if button == 1:
        if arm_mov == 0:
            arm.move_arm(90,-15)
            time.sleep(2)
            arm.close_gripper()
            time.sleep(0.5)
            arm.move_arm(0,0)
            arm_mov = 1
        elif spin == 0:
            if abs(h_deg) > 120:
                spin =1
            else:
                drive.rotate(2)
        elif move_forward ==0:
            if abs(y_m) > 0.05:
                move_forward = 1
                drive.drive_stop()
            else:
                drive.drive_y(2, 2)
        elif place == 0:
            arm.move_arm(90,-15)
            time.sleep(0.5)
            arm.open_gripper()
            time.sleep(0.5)
            arm.move_arm(0,0)
            place = 1
            break
    else:
        drive.drive_stop()


    time.sleep(0.2)