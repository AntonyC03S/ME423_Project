import time
import math
from servo import Servo, servo2040, ANGULAR


base = Servo(servo2040.SERVO_4, ANGULAR)
elbow = Servo(servo2040.SERVO_5, ANGULAR)
gripper = Servo(servo2040.SERVO_6, ANGULAR)

base.enable()
elbow.enable()
gripper.enable()
time.sleep(1)

base.to_mid()
elbow.to_mid()