import sys
import time
import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO
from scipy import interpolate

# Initialize MCP23017 with the address of the GPIO expander (0x20) and bus number (1 for Pi 4)
mcp = MCP.MCP23017(address=0x20, busnum=3)

# Set pin 0 in bank A as an output
mcp.setup(0, GPIO.OUT)

# Function to toggle the state of pin 0 in bank A
def toggle_pin():
    current_state = mcp.input(0)
    print(f"Current state: {current_state}")
    mcp.output(0, not current_state)

print(sys.argv)
print(sys.argv[1])
DELAY = float(sys.argv[1])

# Main loop to toggle the pin at 1 second intervals
while True:
    toggle_pin()
    time.sleep(DELAY)
