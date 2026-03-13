import time
import math
from pimoroni import Button
from servo import Servo, servo2040,CONTINUOUS
from plasma import WS2812
from machine import I2C, Pin

r_w = 2.75 * 0.0254
vmax = 0.5 
wmax = 5
stop = [1486, 1496, 1513]
pulse_range = [300,300,300]
dt = 0.02

ADDR = 0x17
REG_STATUS = 0x1F
REG_POS_XL = 0x20
REG_VEL_XL = 0x26

INT16_TO_M = 10.0 / 32768.0
INT16_TO_MPS = 5.0 / 32768.0
INT16_TO_RAD = math.pi / 32768.0


def pointtopoint(x1, y1, x2, y2, kp=0.25):
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)
    if dist < 1e-9:
        return dx, dy, 0, 0, dist
    speed = min(vmax, kp * dist)
    vx = speed * (dx / dist)
    vy = speed * (dy / dist)
    return dx, dy, vx, vy, dist

def omegas(vx,vy):
    w2 = (-0.5*vx + 0.866*vy)/r_w
    w3 = (-0.5*vx - 0.866*vy)/r_w
    w1 = vx/r_w
    return (w1, w2, w3)

def clamp(x, low = -1, high = 1):
    return low if x < low else high if x > high else x

def omegatopulse(w,i):
    x = clamp(w/wmax)
    return stop[i] - x * pulse_range[i]

def bytecombo(lo, hi):
    v = (hi << 8) | lo
    if v & 0x8000:
        v -= 65536
    return v

def read_pos(i2c):
    pos = i2c.readfrom_mem(ADDR, REG_POS_XL, 6)
    x = bytecombo(pos[0], pos[1]) * INT16_TO_M
    y = bytecombo(pos[2], pos[3]) * INT16_TO_M
    h = bytecombo(pos[4], pos[5]) * INT16_TO_RAD
    return x, y, h

def read_vel(i2c):
    vel = i2c.readfrom_mem(ADDR, REG_VEL_XL, 6)
    vx = bytecombo(vel[0], vel[1]) * INT16_TO_MPS
    vy = bytecombo(vel[2], vel[3]) * INT16_TO_MPS
    vh = bytecombo(vel[4], vel[5]) * INT16_TO_RAD
    return vx, vy, vh

def stopmotor():
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
stopmotor()

i2c = I2C(0, sda=Pin(servo2040.SDA), scl=Pin(servo2040.SCL), freq=100000)
print("I2C devices:", i2c.scan())

x,y,h = read_pos(i2c)
xf,yf = (1, 0)
x_target = x + xf
y_target = y + yf
dx,dy,vx,vy,dist= pointtopoint(x,y,xf,yf)

print("Start pose: x={:.4f}, y={:.4f}, h={:.3f}".format(x, y, h))
print("Target pose: x={:.4f}, y={:.4f}".format(x_target, y_target))

try:
    while True:
        x, y, h = read_pos(i2c)
        vx_meas, vy_meas, vh_meas = read_vel(i2c)
        dx, dy, vx_cmd, vy_cmd, dist = pointtopoint(x, y, x_target, y_target, kp=1.5)
        if dist < 0.01:
            break
        w1, w2, w3 = omegas(vx_cmd, vy_cmd)
        servo1.pulse(omegatopulse(w1, 0))
        servo2.pulse(omegatopulse(w2, 1))
        servo3.pulse(omegatopulse(w3, 2))
        print(
            "x={:+.4f} y={:+.4f} h={:+.3f} | "
            "dx={:+.4f} dy={:+.4f} dist={:.4f} | "
            "vx_cmd={:+.3f} vy_cmd={:+.3f}"
            .format(x, y, h, dx, dy, dist, vx_cmd, vy_cmd)
        )
        time.sleep(dt)

finally:
    stopmotor()
    time.sleep(0.2)
    servo1.disable()
    servo2.disable()
    servo3.disable()
    print("Done")
