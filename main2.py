import time
import math
from matplotlib import pyplot as plt 

r_w = 2.75 * 0.0254
vmax = 0.5 
wmax = 5
stop = [1482, 1490, 1506]
range = [300,300,300]


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
    return stop[i] + x * range[i]


dt = 0.01
rows = []
t = 0
x,y = (0, 0)
xf,yf = (3, 0)
dx,dy,vx,vy,dist= pointtopoint(x,y,xf,yf)

while dist >= 0.01:
    dx,dy,vx,vy,dist= pointtopoint(x,y,xf,yf)
    w1,w2,w3 = omegas(vx,vy)
    x += vx*dt
    y += vy*dt
    cmd1 = omegatopulse(w1, 0)
    cmd2 = omegatopulse(w2, 0)
    cmd3 = omegatopulse(w3, 0)
    rows.append((t, x, y, vx, vy, w1, w2, w3, cmd1, cmd2, cmd3, dist))
    t += dt
ts = [row[0] for row in rows]
w1s = [row[5] for row in rows]
w2s = [row[6] for row in rows]
w3s = [row[7] for row in rows]
cmd1s = [row[8] for row in rows]
cmd2s = [row[9] for row in rows]
cmd3s = [row[10] for row in rows]

plt.figure()
plt.plot(ts, w1s, label="w1")
plt.plot(ts, w2s, label="w2")
plt.plot(ts, w3s, label="w3")
plt.xlabel("Time (s)")
plt.ylabel("Angular velocity (rad/s)")
plt.legend()
plt.show()

plt.figure()
plt.plot(ts, cmd1s, label="cmd1")
plt.plot(ts, cmd2s, label="cmd2")
plt.plot(ts, cmd3s, label="cmd3")
plt.xlabel("Time (s)")
plt.legend()
plt.show()
