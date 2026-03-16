import time
import math
from machine import I2C, Pin
from servo import Servo, servo2040, CONTINUOUS        # type: ignore
from plasma import WS2812                             # type: ignore
from Servos import Arm                                # type: ignore

Arm = Arm(servo2040.SERVO_4, servo2040.SERVO_5, servo2040.SERVO_6)



    # arm.value(-15)
    # servo2.value(90)
Arm.move_arm(90,-15)
time.sleep(0.5)
Arm.close_gripper()
time.sleep(0.5)
Arm.move_arm(0,0)


