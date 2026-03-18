import time
import math
from servo import Servo, servo2040, CONTINUOUS        # type: ignore


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
    r = 0.0665 #m
    l = 0.1135 #l
    front_theta =  math.radians(0+90)
    left_theta =  math.radians(120+90) 
    right_theta =  math.radians(240+90)
    stop = [1486, 1496, 1513]
    pulse_range = [300, 300, 300]
    wmax = 5 

    def __init__(self, front_servo_num, left_servo_num, right_servo_num):
        self.front = Servo(front_servo_num, CONTINUOUS)
        self.left = Servo(left_servo_num, CONTINUOUS)
        self.right = Servo(right_servo_num, CONTINUOUS)
        self.front.enable()
        self.left.enable()
        self.right.enable()
        self.kp = 1
        self.ki = 0
        self.kd = 0
        time.sleep(1)

    def set_kp(self, kp):
        self.kp = kp

    def set_ki(self, ki):
        self.ki = ki

    def set_kd(self, kd):
        self.kd = kd
        
    def servos_speed(self, w1, w2, w3):
        p1= self.front.pulse(self.omegatopulse(w1, 0))
        p2= self.left.pulse(self.omegatopulse(w2, 1))
        p3= self.right.pulse(self.omegatopulse(w3, 2))
        return p1, p2, p3

    def drive_stop(self):
        self.servos_speed(0,0,0)
        print("stop")

    def drive(self, desired, real):
        print("drive")
        x = desired[0] - real[0]
        y = desired[1] - real[1]
        theta = desired[2] - real[2]

        x = x*self.kp
        y = y*self.kp
        theta = theta*self.kp

        if abs(x) < 0.01 and abs(y) < 0.01 and abs(theta) < 0.01:
            self.servos_speed(Drivebase.stop[0],Drivebase.stop[1], Drivebase.stop[2])
            return 0

        if abs(x) < 0.020 or abs(y) < 0.020 or abs(theta) < 0.020:
            V = 0.05
            W = 0.05
        else:
            V = 0.25
            W = 0.1
        
        if abs(theta == 0):
            W = 0

        
        angle = math.atan2(y, x)
        print(x,y,theta)
        w1,w2,w3=self.cal_wheel_speed(math.cos(angle)*V, math.sin(angle)*V, W)
        print(w1,w2,w3)
        p1, p2, p3= self.servos_speed(w1, w2, w3)
        print(p1, p2, p3)
        return 1


    def cal_wheel_speed(self, Vx, Vy, W):
        u1 = -math.sin(Drivebase.front_theta)*Vx + math.cos(Drivebase.front_theta)*Vy + Drivebase.l*W
        u2 = -math.sin(Drivebase.left_theta)*Vx + math.cos(Drivebase.left_theta)*Vy + Drivebase.l*W
        u3 = -math.sin(Drivebase.right_theta)*Vx + math.cos(Drivebase.right_theta)*Vy + Drivebase.l*W
        w1 = u1/Drivebase.r
        w2 = u2/Drivebase.r
        w3 = u3/Drivebase.r
        
        return w1, w2, w3 
    
    def clamp(self, x, low, high):
        if x < low:
            return low
        elif x > high:
            return high
        return x

    def omegatopulse(self,w, i):
        x = self.clamp(w / Drivebase.wmax, -1.0, 1.0)
        return int(Drivebase.stop[i] - x * Drivebase.pulse_range[i])