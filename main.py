
import time
import math
from machine import I2C, Pin
from servo import Servo, servo2040, CONTINUOUS
from plasma import WS2812

r_w = 2.75 * 0.0254

vmax = 1        
vhmax = 1.5         
wmax = 10       

stop = [1486, 1496, 1513]
pulse_range = [300, 300, 300]

kp_pos = 1.2      
kd_pos = 0.35    

kp_h = 2.5        
kd_h = 0.3       

pos_tol = 0.01       
head_tol = 0.08      
dt = 0.02

ADDR = 0x17
REG_STATUS = 0x1F
REG_POS_XL = 0x20
REG_VEL_XL = 0x26

INT16_TO_M = 10.0 / 32768.0
INT16_TO_MPS = 5.0 / 32768.0
INT16_TO_RAD = math.pi / 32768.0


def s16(lo, hi):
    v = (hi << 8) | lo
    if v & 0x8000:
        v -= 65536
    return v

def clamp(x, low, high):
    if x < low:
        return low
    if x > high:
        return high
    return x

def wrap_angle(a):
    while a > math.pi:
        a -= 2.0 * math.pi
    while a < -math.pi:
        a += 2.0 * math.pi
    return a

def omegatopulse(w, i):
    x = clamp(w / wmax, -1.0, 1.0)
    return int(stop[i] - x * pulse_range[i])

def omegas(vx, vy, vh=0.0):
    w1 = (vx) / r_w + vh
    w2 = (-0.5 * vx + 0.866 * vy) / r_w + vh
    w3 = (-0.5 * vx - 0.866 * vy) / r_w + vh
    return w1, w2, w3

def read_status(i2c):
    return i2c.readfrom_mem(ADDR, REG_STATUS, 1)[0]

def read_pose(i2c):
    pos = i2c.readfrom_mem(ADDR, REG_POS_XL, 6)

    xs = s16(pos[0], pos[1]) * INT16_TO_M
    ys = s16(pos[2], pos[3]) * INT16_TO_M
    hs = s16(pos[4], pos[5]) * INT16_TO_RAD

    x = -xs
    y = -ys
    h = wrap_angle(hs + math.pi)

    return x, y, h

def read_velocity(i2c):
    vel = i2c.readfrom_mem(ADDR, REG_VEL_XL, 6)

    vxs = s16(vel[0], vel[1]) * INT16_TO_MPS
    vys = s16(vel[2], vel[3]) * INT16_TO_MPS
    vhs = s16(vel[4], vel[5]) * INT16_TO_RAD

    vx = -vxs
    vy = -vys
    vh = vhs

    return vx, vy, vh

def position_heading_controller(x, y, h, vx_meas, vy_meas, vh_meas,
                                x_target, y_target, h_target):
    ex = x_target - x
    ey = y_target - y
    dist = math.sqrt(ex * ex + ey * ey)

    vx_cmd = kp_pos * ex
    vy_cmd = kp_pos * ey

    eh = wrap_angle(h_target - h)
    vh_cmd = 0.0

    vmag = math.sqrt(vx_cmd * vx_cmd + vy_cmd * vy_cmd)
    if vmag > vmax and vmag > 1e-9:
        scale = vmax / vmag
        vx_cmd *= scale
        vy_cmd *= scale

    return ex, ey, eh, dist, vx_cmd, vy_cmd, vh_cmd

def set_wheels(vx_cmd, vy_cmd, vh_cmd):
    w1, w2, w3 = omegas(vx_cmd, vy_cmd, vh_cmd)
    servo1.pulse(omegatopulse(w1, 0))
    servo2.pulse(omegatopulse(w2, 1))
    servo3.pulse(omegatopulse(w3, 2))
    return w1, w2, w3

def stop_all():
    servo1.pulse(stop[0])
    servo2.pulse(stop[1])
    servo3.pulse(stop[2])


led_bar = WS2812(servo2040.NUM_LEDS, 1, 0, servo2040.LED_DATA)
led_bar.start()

servo1 = Servo(servo2040.SERVO_1, CONTINUOUS)  
servo2 = Servo(servo2040.SERVO_2, CONTINUOUS)   
servo3 = Servo(servo2040.SERVO_3, CONTINUOUS)   

servo1.enable()
servo2.enable()
servo3.enable()
stop_all()

i2c = I2C(0, sda=Pin(servo2040.SDA), scl=Pin(servo2040.SCL), freq=100000)

print("I2C devices:", i2c.scan())

print("Calibrating IMU... keep robot still")

i2c.writeto_mem(ADDR, 0x06, bytes([150]))

time.sleep(0.6)

print("Calibration done")

x0, y0, h0 = read_pose(i2c)

print("Start pose:")
print("x = {:.4f} m, y = {:.4f} m, h = {:.3f} rad".format(x0, y0, h0))

dx_target = 0
dy_target = 1
dh_target = 0

x_target = x0 + dx_target
y_target = y0 + dy_target
h_target = wrap_angle(h0 + dh_target)

print("Target pose:")
print("x = {:.4f} m, y = {:.4f} m, h = {:.3f} rad".format(x_target, y_target, h_target))

while True:
        x, y, h = read_pose(i2c)
        vx_meas, vy_meas, vh_meas = read_velocity(i2c)

        ex, ey, eh, dist, vx_cmd, vy_cmd, vh_cmd = position_heading_controller(
            x, y, h,
            vx_meas, vy_meas, vh_meas,
            x_target, y_target, h_target
        )
        if dist < pos_tol and abs(eh) < head_tol:
            break

        w1, w2, w3 = set_wheels(vx_cmd, vy_cmd, 0)

        status = read_status(i2c)
        print(
            "x={:+.3f} y={:+.3f} h={:+.3f} | "
            "ex={:+.3f} ey={:+.3f} eh={:+.3f} | "
            "vx={:+.3f} vy={:+.3f} vh={:+.3f} | "
            "status=0x{:02X}"
            .format(x, y, h, ex, ey, eh, vx_cmd, vy_cmd, vh_cmd, status)
        )
        time.sleep(dt)

stop_all()
time.sleep(0.25)
servo1.disable()
servo2.disable()
servo3.disable()
print("Done")
