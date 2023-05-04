import Adafruit_ADS1x15

# Create an ADS1115 ADC instance
adc = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=3)

# Set the gain (input voltage range) of the ADC
# Available options: 2/3, 1, 2, 4, 8, 16
GAIN = 1

# Set the reference voltage (in volts)
REF_VOLTAGE = 3.3

# Read the voltage from channel 0
voltage = adc.read_adc(2, gain=GAIN) / 32767.0

# Print the measured voltage to the console
print("Voltage at pin 0: {} V".format(voltage))
