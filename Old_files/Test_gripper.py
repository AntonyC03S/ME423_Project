import time
from servo import Servo, servo2040

servo = Servo(servo2040.SERVO_6)
servo.enable()
time.sleep(1)

while True:
    for angle in range(-50, 10, 1):
        servo.value(angle)
        time.sleep(0.03)


    for angle in range(10, -50, -1):
        servo.value(angle)
        time.sleep(0.03)
    time.sleep(5)