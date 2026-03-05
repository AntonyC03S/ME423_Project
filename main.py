import time
import math
from pimoroni import Button
from servo import Servo, servo2040,CONTINUOUS
from plasma import WS2812

r_w = 2.75 * 0.0254
vmax = 0.5 
wmax = 5
stop = [1482, 1490, 1506]
range = [300,300,300]
led_bar = WS2812(servo2040.NUM_LEDS, 1, 0, servo2040.LED_DATA)
led_bar.start()
servo1 = Servo(servo2040.SERVO_1, CONTINUOUS)
servo2 = Servo(servo2040.SERVO_2, CONTINUOUS)
servo3 = Servo(servo2040.SERVO_3, CONTINUOUS)
servo1.enable()
servo2.enable()
servo3.enable()

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
    w1 = (-0.5*vx + 0.866*vy)/r_w
    w2 = (-0.5*vx - 0.866*vy)/r_w
    w3 = vx/r_w
    return (w1, w2, w3)

def clamp(x, low = -1, high = 1):
    return low if x < low else high if x > high else x

def omegatopulse(w,i):
    x = clamp(w/wmax)
    return stop[i] - x * range[i]

dt = 0.01
rows = []
t = 0
x,y = (0, 0)
xf,yf = (15, 0)
dx,dy,vx,vy,dist= pointtopoint(x,y,xf,yf)

while dist >= 0.01:
    dx,dy,vx,vy,dist= pointtopoint(x,y,xf,yf)
    w1,w2,w3 = omegas(vx,vy)
    servo1.pulse(omegatopulse(w1,0))
    servo2.pulse(omegatopulse(w2,1))
    servo3.pulse(omegatopulse(w3,2))
    x += vx*dt
    y += vy*dt
    t += dt
    time.sleep(dt)

servo1.disable()
servo2.disable()
servo3.disable()


