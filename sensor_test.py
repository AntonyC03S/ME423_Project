from machine import I2C, Pin
from servo import servo2040
import time
import math

ADDR = 0x17

# Registers from your map
REG_STATUS = 0x1F
REG_POS_XL = 0x20
REG_VEL_XL = 0x26

# Conversion constants (from register map full-scale ranges)
INT16_TO_M = 10.0 / 32768.0
INT16_TO_MPS = 5.0 / 32768.0
INT16_TO_RAD = math.pi / 32768.0

def s16(lo, hi):
    v = (hi << 8) | lo
    if v & 0x8000:
        v -= 65536
    return v

i2c = I2C(0, sda=Pin(servo2040.SDA), scl=Pin(servo2040.SCL), freq=100000)

print("I2C devices:", i2c.scan())
print("Using SDA =", servo2040.SDA, "SCL =", servo2040.SCL)
print("Move the sensor on a surface. Ctrl-C to stop.\n")

while True:
    # Read 6 bytes of position (X,Y,H)
    pos = i2c.readfrom_mem(ADDR, REG_POS_XL, 6)
    x = s16(pos[0], pos[1]) * INT16_TO_M
    y = s16(pos[2], pos[3]) * INT16_TO_M
    h = s16(pos[4], pos[5]) * INT16_TO_RAD

    # Read 6 bytes of velocity (Vx,Vy,Vh)
    vel = i2c.readfrom_mem(ADDR, REG_VEL_XL, 6)
    vx = s16(vel[0], vel[1]) * INT16_TO_MPS
    vy = s16(vel[2], vel[3]) * INT16_TO_MPS
    vh = s16(vel[4], vel[5]) * INT16_TO_RAD

    status = i2c.readfrom_mem(ADDR, REG_STATUS, 1)[0]

    print("pos: x={:+.4f}m y={:+.4f}m h={:+.3f}rad | "
          "vel: vx={:+.4f} vy={:+.4f} vh={:+.3f} | status=0x{:02X}"
          .format(x, y, h, vx, vy, vh, status))

    time.sleep(0.1)