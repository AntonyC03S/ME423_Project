import time
import math
from matplotlib import pyplot as plt 

def coeff(theta, end, t):
    a0 = theta
    a1 = 0
    a2 = theta*(-3/t**2) + end*(3/t**2)
    a3 = theta*(2/t**3) + end*(-2/t**3)
    return a0, a1, a2, a3

def cubic(t, a0, a1, a2, a3):
    return a0 + a1*t + a2*t**2 + a3*t**3

theta4 = 0 
end4 = 75
a0 ,a1, a2, a3 = coeff(theta4, end4, 7)
t4 = []
t = 0

while t <= 7:
    theta4 = cubic(t, a0, a1, a2, a3)
    t4.append((t, theta4))
    t += 0.1

ts = [row[0] for row in t4]
theta4s = [row[1] for row in t4]

plt.figure()
plt.plot(ts, theta4s)
plt.xlabel('Time (s)')
plt.ylabel('Theta4 (degrees)')
plt.show()