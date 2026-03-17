import time
from machine import I2C, Pin
from servo import Servo, servo2040, CONTINUOUS        # type: ignore
from plasma import WS2812                             # type: ignore






class Light_sensor():
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
    # SDA = GPIO20
    # SCL = GPIO21
    # --------------------------------------------------

    def __init__(self):
        self.i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
        self.devices = self.i2c.scan()

        try:
            product_id = self.read_u8(Light_sensor.REG_PRODUCT_ID)
            print("Product ID:", hex(product_id))
            if product_id != Light_sensor.EXPECTED_PRODUCT_ID:
                print("Warning: expected 0x5F")
        except Exception as e:
            print("Could not read product ID:", e)
            raise SystemExit

        try:
            status = self.read_u8(Light_sensor.REG_STATUS)
            print("Status:", hex(status))
        except Exception as e:
            print("Could not read status:", e)



    def read_u8(self, reg):
        return self.i2c.readfrom_mem(Light_sensor.OTOS_ADDR, reg, 1)[0]


    def write_u8(self, reg, value):
        self.i2c.writeto_mem(Light_sensor.OTOS_ADDR, reg, bytes([value & 0xFF]))


    def read_s16_le(self, buf, idx):
        v = buf[idx] | (buf[idx + 1] << 8)
        if v & 0x8000:
            v -= 65536
        return v


    def read_pose_raw(self):
        data = self.i2c.readfrom_mem(Light_sensor.OTOS_ADDR, Light_sensor.REG_POS_XL, 6)
        x_raw = self.read_s16_le(data, 0)
        y_raw = self.read_s16_le(data, 2)
        h_raw = self.read_s16_le(data, 4)
        return x_raw, y_raw, h_raw

    def read_pose_real_m(self):
        x_raw, y_raw, h_raw = self.read_pose_raw()

        x_m = x_raw * Light_sensor.INT16_TO_METER
        y_m = y_raw * Light_sensor.INT16_TO_METER
        h_rad = h_raw * Light_sensor.INT16_TO_RAD
        h_deg = h_rad * 180.0 / 3.14159
        return (x_m, y_m, h_deg) 



    def calibrate_imu(self):
        try:
            print("Keep the sensor flat and still...")
            self.write_u8(Light_sensor.REG_IMU_CALIB, 255)
            time.sleep_ms(800)
            print("Calibration command sent")
        except Exception as e:
            print("Calibration failed:", e)


    def reset_tracking(self):
        try:
            self.write_u8(Light_sensor.REG_RESET, 1)
            time.sleep_ms(50)
            print("Tracking reset")
        except Exception as e:
            print("Reset failed:", e)


