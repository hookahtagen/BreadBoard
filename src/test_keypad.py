import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO

# Define the MCP23017 address and I2C bus number
MCP23017_ADDRESS = 0x20
I2C_BUS = 3

# Initialize the MCP23017
mcp = MCP.MCP23017(MCP23017_ADDRESS, busnum=I2C_BUS)

# Set the column pins to inputs with pull-up resistors
for i in range(4):
    mcp.setup(8+i, GPIO.IN)

# Set the row pins to outputs
for i in range(4):
    mcp.setup(12+i, GPIO.OUT)

# Define the keypad layout
keypad = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Define a function to read a single character from the keypad
def read_character():
    while True:
        for i in range(4):
            # Set the current row pin to low and the others to high
            mcp.output(12+i, GPIO.LOW)
            for j in range(4):
                # If a key is pressed, return the corresponding character
                if mcp.input(8+j) == GPIO.LOW:
                    # Set all the row pins back to high
                    for k in range(4):
                        mcp.output(12+k, GPIO.HIGH)
                    return keypad[i][j]
            # Set all the row pins back to high
            mcp.output(12+i, GPIO.HIGH)

# Read four characters from the keypad
characters = ''
while len(characters) < 4:
    characters += read_character()

# Print the characters to the console
print(characters)
