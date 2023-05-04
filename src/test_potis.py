import Adafruit_ADS1x15
import time

from ads1115_t import clear_screen

# create an ADS1115 ADC object with address 0x4b on bus number 3
adc = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=3)

DIVIDER_RATIO = 10e4/(10e4 + 10e4)

# +/- 6.144V
GAIN = 2/3

while True:
    clear_screen()
    # read the voltage on A3 and print the result
    raw_value = adc.read_adc(2, gain=GAIN)

    # Convert the raw ADC value to voltage
    voltage = raw_value * 0.0001875 / DIVIDER_RATIO
    print("Voltage on A3: {:.4f} V".format(voltage))

    # wait for 1 second before taking the next reading
    time.sleep(.5)
