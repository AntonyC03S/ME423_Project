import time
import math
from machine import I2C, Pin
from servo import Servo, servo2040, CONTINUOUS        # type: ignore
from plasma import WS2812                             # type: ignore
from Servos import Arm                                
from Sensor import Light_sensor                       

print("Scanning I2C...")
arm = Arm(servo2040.SERVO_4, servo2040.SERVO_5, servo2040.SERVO_6)
sensor = Light_sensor()
print("ansjdf")
sensor.calibrate_imu()
sensor.reset_tracking()
print("\nMove the sensor slowly on the table.\n")


# arm.move_arm(90,-15)
# time.sleep(0.5)
# arm.close_gripper()
# time.sleep(0.5)
# arm.move_arm(0,0)



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

    time.sleep(0.2)