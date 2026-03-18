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

def sensor_loop():
    pass


def arm_loop():


    pass

def drive_loop():
    pass


# Main Loop 

# 100 Hz main loop
dt = 0.001
next_t = time.ticks_us()

sensor_state = 0
arm_state = 0
drive_state = 0


while True:
    # # 1. Read sensors
    # read_odometry()
    # read_distance()
    # read_arm_feedback()

    # # 2. Compute control
    # update_drive_controller()
    # update_arm_controller()

    # # 3. Send outputs
    # set_drive_servos()
    # set_arm_servos()

    sensor_loop()
    drive_loop()
    sensor_loop()



    # 4. Wait until next cycle
    next_t = time.ticks_add(next_t, int(dt * 1_000_000))
    while time.ticks_diff(next_t, time.ticks_us()) > 0:
        pass


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