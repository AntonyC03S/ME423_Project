import time
import math
from machine import I2C, Pin
from servo import Servo, servo2040, CONTINUOUS        # type: ignore
from plasma import WS2812                             # type: ignore
from Servos import Arm, Drivebase                                
from Sensor import Light_sensor                       
from pimoroni import Button    # type: ignore


drive = Drivebase(servo2040.SERVO_1, servo2040.SERVO_2, servo2040.SERVO_3)

