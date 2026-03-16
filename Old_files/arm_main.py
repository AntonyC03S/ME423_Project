import time
from servo import Servo, servo2040, ANGULAR


base = Servo(servo2040.SERVO_4, ANGULAR)
elbow = Servo(servo2040.SERVO_5, ANGULAR)
gripper = Servo(servo2040.SERVO_6, ANGULAR)


BASE_OFFSET = 0
ELBOW_OFFSET = 0
GRIPPER_OFFSET = 0

GRIP_OPEN = -20
GRIP_CLOSE = -200

base.enable()
elbow.enable()
gripper.enable()

time.sleep(1)


def move_base(angle):
    base.value(angle)

def move_elbow(angle):
    elbow.value(angle)

def open_gripper():
    gripper.value(GRIP_OPEN)

def close_gripper():
    gripper.value(GRIP_CLOSE)


def move_arm(base_angle, elbow_angle):
    move_base(base_angle)
    move_elbow(elbow_angle)


def home():
    move_arm(0, 0)
    open_gripper()

def pick(base_angle, elbow_angle):

    open_gripper()
    time.sleep(1)

    move_arm(base_angle, elbow_angle)
    time.sleep(1)

    close_gripper()
    time.sleep(4)

    move_elbow(elbow_angle + 20)
    time.sleep(1)


def place(base_angle, elbow_angle):

    move_arm(base_angle, elbow_angle)
    time.sleep(1)

    open_gripper()
    time.sleep(1)


# home()

time.sleep(2)


gripper.value(-200)
print("Gripper value set to 100")

# pick(45, 0)

# time.sleep(2)

# place(-70, -15)

# time.sleep(2)

# home()