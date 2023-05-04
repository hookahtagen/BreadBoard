import os
import sys
import time
from Adafruit_ADS1x15 import ADS1115

def clear_screen():
    os.system("clear")


if __name__ == '__main__':
  # Create ADS1115 objects for each channel
  adc0 = ADS1115(address=0x4b, busnum=3)
  adc1 = ADS1115(address=0x4b, busnum=3)
  adc2 = ADS1115(address=0x4b, busnum=3)
  adc3 = ADS1115(address=0x4b, busnum=3)

  # Start continuous conversion on each channel
  adc0.start_adc(0, gain=1)
  adc1.start_adc(1, gain=1)
  adc2.start_adc(2, gain=1)
  adc3.start_adc(3, gain=1)

  start = time.time()
  while (time.time() - start) <= 120.0:
      clear_screen()

      # Read and print the result of each channel
      value0 = adc0.get_last_result()
      voltage0 = float(value0) * 4.096 / 32767.0
      voltage0 = round(voltage0, 4)

      value1 = adc1.get_last_result()
      voltage1 = float(value1) * 4.096 / 32767.0
      voltage1 = round(voltage1, 4)

      value2 = adc2.get_last_result()
      voltage2 = float(value2) * 4.096 / 32767.0
      voltage2 = round(voltage2, 4)

      value3 = adc3.get_last_result()
      voltage3 = float(value3) * 4.096 / 32767.0
      voltage3 = round(voltage3, 4)

      msg = f"""
    ************************
    *                      *
    *  Voltage 0 = {voltage0} V  *
    *  Voltage 1 = {voltage1} V  *
    *  Voltage 2 = {voltage2} V  *
    *  Voltage 3 = {voltage3} V  *
    *                      *
    ************************
      """

      print(msg)

      time.sleep(0.5)

  # Stop continuous conversion on each channel
  adc0.stop_adc()
  adc1.stop_adc()
  adc2.stop_adc()
  adc3.stop_adc()
