import time
from servo import Servo, servo2040        # type: ignore


class Arm():

    def __init__(self, bottom_servo_num, top_servo_num, gripper_servo_num):
        self.bottom = Servo(bottom_servo_num)
        self.top = Servo(top_servo_num)
        self.gripper = Servo(gripper_servo_num)
        self.bottom.enable()
        self.top.enable()
        self.gripper.enable()
        time.sleep(1)


    def close_gripper(self):
        self.gripper.value(-50)

    def open_gripper(self):
        self.gripper.value(10)

    def move_arm(self, angle_bottom, angle_top):
        self.bottom.value(angle_bottom)
        self.top.value(angle_top)
        
    def disable(self):
        self.bottom.disable()
        self.top.disable()
        self.gripper.disable()
        
    def home(self):
        self.bottom.value(0)
        self.top.value(0)
        self.open_gripper()

    def rest(self):
        self.bottom.value(0)
        self.top.value(0)
        self.open_gripper()



class Drivebase():

    def __init__(self, front_servo_num, left_servo_num, right_servo_num):
        self.front = Servo(front_servo_num)
        self.left = Servo(left_servo_num)
        self.right = Servo(right_servo_num)
        self.front.enable()
        self.left.enable()
        self.right.enable()
        time.sleep(1)
