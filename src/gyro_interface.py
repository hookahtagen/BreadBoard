import os
import smbus
import math
import time

from i2c_interface import I2cInterface

# MPU-6050 Register Addresses
REG_PWR_MGMT_1 = 0x6B
REG_GYRO_XOUT_H = 0x43
REG_GYRO_YOUT_H = 0x45
REG_GYRO_ZOUT_H = 0x47

# MPU-6050 Gyro Full Scale Range (in deg/s)
GYRO_FULL_SCALE_RANGE = 250

# MPU-6050 Gyro Sensitivity Scale Factor (in deg/s per LSB)
GYRO_SCALE_FACTOR = GYRO_FULL_SCALE_RANGE / 32767.0

# MPU-6050 Gyro Sensitivity Scale Factor (in m/s per LSB)
GYRO_SCALE_FACTOR_MPS = GYRO_SCALE_FACTOR * math.pi / 180.0

# MPU-6050 I2C Address
MPU6050_ADDR = 0x68

# Initialize I2C bus
bus = smbus.SMBus(3)

# Wake up MPU-6050
bus.write_byte_data(MPU6050_ADDR, REG_PWR_MGMT_1, 0)

# Function to read raw gyro data
def read_gyro_raw(reg_addr):
    high = bus.read_byte_data(MPU6050_ADDR, reg_addr)
    low = bus.read_byte_data(MPU6050_ADDR, reg_addr + 1)
    value = (high << 8) + low
    if value > 32767:
        value = value - 65536
    return value

def clear_screen():
    os.system("clear")

def emergency_stop(interface: I2cInterface):
    if interface.read_input(True, 0) == 1:
        exit(0)
    else:
        pass
    

if __name__ == '__main__':
    interface = I2cInterface("i2c_interface")
    interface.addr=interface.MCP23017_ADDR
    # Main loop
    while True:
        clear_screen()
        
        gyro_x_raw = read_gyro_raw(REG_GYRO_XOUT_H)
        gyro_y_raw = read_gyro_raw(REG_GYRO_YOUT_H)
        gyro_z_raw = read_gyro_raw(REG_GYRO_ZOUT_H)

        gyro_x = gyro_x_raw * GYRO_SCALE_FACTOR_MPS
        gyro_y = gyro_y_raw * GYRO_SCALE_FACTOR_MPS
        gyro_z = gyro_z_raw * GYRO_SCALE_FACTOR_MPS

        print("Gyro X: {:.2f} m/s, Gyro Y: {:.2f} m/s, Gyro Z: {:.2f} m/s".format(gyro_x, gyro_y, gyro_z))

        time.sleep(0.25)  # Sleep for 100ms
        
        emergency_stop(interface)
