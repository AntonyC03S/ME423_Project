import time
import math
from pimoroni import Button
from servo import Servo, servo2040, ANGULAR
from plasma import WS2812


def coeff(theta, end, t):
    a0 = theta
    a1 = 0
    a2 = theta*(-3/t**2) + end*(3/t**2)
    a3 = theta*(2/t**3) + end*(-2/t**3)
    return a0, a1, a2, a3

def cubic(t, a0, a1, a2, a3):
    return a0 + a1*t + a2*t**2 + a3*t**3

servo4 = Servo(servo2040.SERVO_4, ANGULAR)
servo5 = Servo(servo2040.SERVO_5, ANGULAR)

servo4.enable()
servo5.enable() 

theta4 = 0
theta5 = 0
end4 = 75
end5 = 50
a0 ,a1, a2, a3 = coeff(theta4, end4, 7)
t = 0
servo4.value(theta4)
servo5.value(theta5)
time.sleep(1)

while t <= 7:
    theta4 = cubic(t, a0, a1, a2, a3)
    servo4.value(theta4)
    t += 0.1
    time.sleep(0.1)


