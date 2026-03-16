import time
from machine import I2C, Pin

# OTOS I2C address
OTOS_ADDR = 0x17

# Registers
REG_PRODUCT_ID = 0x00
REG_IMU_CALIB  = 0x06
REG_RESET      = 0x07
REG_STATUS     = 0x1F
REG_POS_XL     = 0x20   # x, y, heading = 3 signed int16 values

EXPECTED_PRODUCT_ID = 0x5F

# Conversion factors
INT16_TO_METER = 10.0 / 32768.0
INT16_TO_RAD   = 3.14159 / 32768.0


# --------------------------------------------------
# Manual wiring version:
# SDA = GPIO20
# SCL = GPIO21
# --------------------------------------------------
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)


def read_u8(reg):
    return i2c.readfrom_mem(OTOS_ADDR, reg, 1)[0]


def write_u8(reg, value):
    i2c.writeto_mem(OTOS_ADDR, reg, bytes([value & 0xFF]))


def read_s16_le(buf, idx):
    v = buf[idx] | (buf[idx + 1] << 8)
    if v & 0x8000:
        v -= 65536
    return v


def read_pose_raw():
    data = i2c.readfrom_mem(OTOS_ADDR, REG_POS_XL, 6)
    x_raw = read_s16_le(data, 0)
    y_raw = read_s16_le(data, 2)
    h_raw = read_s16_le(data, 4)
    return x_raw, y_raw, h_raw


def calibrate_imu():
    try:
        print("Keep the sensor flat and still...")
        write_u8(REG_IMU_CALIB, 255)
        time.sleep_ms(800)
        print("Calibration command sent")
    except Exception as e:
        print("Calibration failed:", e)


def reset_tracking():
    try:
        write_u8(REG_RESET, 1)
        time.sleep_ms(50)
        print("Tracking reset")
    except Exception as e:
        print("Reset failed:", e)


print("Scanning I2C...")
devices = i2c.scan()
print("Found:", [hex(d) for d in devices])

if OTOS_ADDR not in devices:
    print("OTOS not found at address 0x17")
    print("Check wiring:")
    print("  VIN/3V3 -> 3V3")
    print("  GND     -> GND")
    print("  SDA     -> GP20")
    print("  SCL     -> GP21")
    raise SystemExit

try:
    product_id = read_u8(REG_PRODUCT_ID)
    print("Product ID:", hex(product_id))
    if product_id != EXPECTED_PRODUCT_ID:
        print("Warning: expected 0x5F")
except Exception as e:
    print("Could not read product ID:", e)
    raise SystemExit

try:
    status = read_u8(REG_STATUS)
    print("Status:", hex(status))
except Exception as e:
    print("Could not read status:", e)

calibrate_imu()
reset_tracking()

print("\nMove the sensor slowly on the table.\n")

while True:
    try:
        x_raw, y_raw, h_raw = read_pose_raw()

        x_m = x_raw * INT16_TO_METER
        y_m = y_raw * INT16_TO_METER
        h_rad = h_raw * INT16_TO_RAD
        h_deg = h_rad * 180.0 / 3.14159

        print(
            "x_raw={:6d}  y_raw={:6d}  h_raw={:6d}   "
            "x={: .4f} m  y={: .4f} m  h={: .2f} deg".format(
                x_raw, y_raw, h_raw, x_m, y_m, h_deg
            )
        )

    except Exception as e:
        print("Read failed:", e)

    time.sleep(0.2)