import time
import smbus2


class I2cInterface:

    # Define MCP23017 params
    MCP23017_ADDR = 0x20
    MCP23017_IODIR_A = 0x00
    MCP23017_IODIR_B = 0x01
    MCP23017_GPIO_A = 0x12
    MCP23017_GPIO_B = 0x13
    MCP23017_OLAT_A = 0x14    # Output latch register A
    MCP23017_OLAT_B = 0x15    # Output latch register B

    # Define PCF8574 params
    PCF8574_ADDR = 0x21
    PCF8574_IODIR = 0x00
    PCF8574_GPIO = 0x01

    # Define other params
    BUS_NUM = 3
    IODIR_LST = [PCF8574_IODIR, MCP23017_IODIR_A, MCP23017_IODIR_B]
    GPIO_LST = [PCF8574_GPIO, MCP23017_GPIO_A, MCP23017_GPIO_B]

    def __init__(self, name="i2c_interface", addr=None):
        """
        Initialize the I2CIOExpander instance.

        Args:
            name (str): Name for the interface object
            addr (int): I2C address of the I/O expander chip.
        """
        
        self.name = name
        self.addr = addr
        self.bus = smbus2.SMBus(self.BUS_NUM)

    def set_direction(self, iodir, channel, direction):
        """
        Set the direction of a specific channel.

        Args:
            channel (int): Channel number (0-7) of the channel.
            direction (bool): Direction of the channel. True for input, False for output.
        """
        
        IODIR = self.MCP23017_IODIR_A if iodir else self.MCP23017_IODIR_B

        if not (0 <= channel <= 7):
            raise ValueError("Channel number must be between 0 and 7.")

        if isinstance(direction, bool):
            if self.addr == self.MCP23017_ADDR:  # MCP23017
                if direction:
                    self.bus.write_byte_data(self.addr, IODIR, self.bus.read_byte_data(
                        self.addr, IODIR) | (1 << channel))
                else:
                    self.bus.write_byte_data(self.addr, IODIR, self.bus.read_byte_data(
                        self.addr, IODIR) & ~(1 << channel))
            elif self.addr == self.PCF8574_ADDR:  # PCF8574
                if direction:
                    self.bus.write_byte_data(self.addr, self.PCF8574_IODIR, self.bus.read_byte_data(
                        self.addr, self.PCF8574_IODIR) | (1 << channel))
                else:
                    self.bus.write_byte_data(self.addr, self.PCF8574_IODIR, self.bus.read_byte_data(
                        self.addr, self.PCF8574_IODIR) & ~(1 << channel))
            else:
                raise ValueError(
                    "Invalid I2C address. Supported addresses are 0x20 for MCP23017 and 0x21 for PCF8574.")
        else:
            raise TypeError("Direction must be a boolean value.")

    def set_output(self, channel, bank, state):
        """
        Set the output state of a specific channel.

        Args:
            channel (int): Channel number (0-7) of the channel.
            state (bool): State of the channel. True for HIGH, False for LOW.
        """
        
        GPIO = self.MCP23017_GPIO_A if bank else self.MCP23017_GPIO_B

        if not (0 <= channel <= 7):
            raise ValueError("Channel number must be between 0 and 7.")

        if isinstance(state, bool):
            if self.addr == self.MCP23017_ADDR:  # MCP23017
                if state:
                    self.bus.write_byte_data(self.addr, GPIO, self.bus.read_byte_data(
                        self.addr, GPIO) | (1 << channel))
                else:
                    self.bus.write_byte_data(self.addr, GPIO, self.bus.read_byte_data(
                        self.addr, GPIO) & ~(1 << channel))

            elif self.addr == self.PCF8574_ADDR:  # PCF8574
                if state:
                    self.bus.write_byte_data(self.addr, self.PCF8574_GPIO, self.bus.read_byte_data(
                        self.addr, self.PCF8574_GPIO) | (1 << channel))
                else:
                    self.bus.write_byte_data(self.addr, self.PCF8574_GPIO, self.bus.read_byte_data(
                        self.addr, self.PCF8574_GPIO) & ~(1 << channel))
            else:
                raise ValueError(
                    "Invalid I2C address. Supported addresses are 0x20 for MCP23017 and 0x21 for PCF8574.")
        else:
            raise TypeError("State must be a boolean value.")

    def read_input(self, bank: bool, channel: int):
        """
        Read the input state of a specific channel.

        Args:
            channel (int): Channel number (0-7) of the channel.

        Returns:
            bool: True if the channel is HIGH, False if the channel is LOW.
        """
        
        GPIO = self.MCP23017_GPIO_A if bank else self.MCP23017_GPIO_B
        
        if not (0 <= channel <= 7):
            raise ValueError("Channel number must be between 0 and 7.")
        
        if self.addr == self.MCP23017_ADDR:  # MCP23017
            return (self.bus.read_byte_data(self.addr, GPIO) >> channel) & 0x01
        elif self.addr == self.PCF8574_ADDR:  # PCF8574
            return (self.bus.read_byte_data(self.addr, self.PCF8574_GPIO) >> channel) & 0x01
        else:
            raise ValueError(
                "Invalid I2C address. Supported addresses are 0x20 for MCP23017 and 0x21 for PCF8574.")

    def get_output_state(self, olat, channel):
        """
        Get the current output state of a specific channel.

        Args:
            channel (int): Channel number (0-7) of the channel.

        Returns:
            int: 0 if the channel is set to LOW, 1 if the channel is set to HIGH.
        """
        
        OLAT = self.MCP23017_OLAT_A if olat else self.MCP23017_OLAT_B
        
        if not (0 <= channel <= 7):
            raise ValueError("Channel number must be between 0 and 7.")
        
        if self.addr == self.MCP23017_ADDR:  # MCP23017
            return (self.bus.read_byte_data(self.addr, OLAT) >> channel) & 0x01
        elif self.addr == self.PCF8574_ADDR:  # PCF8574
            return (self.bus.read_byte_data(self.addr, self.PCF8574_GPIO) >> channel) & 0x01
        else:
            raise ValueError("Invalid I2C address. Supported addresses are 0x20 for MCP23017 and 0x38 for PCF8574.")


if __name__ == '__main__':
    interface = I2cInterface("i2c_interface")
    interface.addr=interface.MCP23017_ADDR
    interface.set_direction(iodir = True, channel = 0, direction = True)
    interface.set_direction(iodir = True, channel = 2, direction = True)
    interface.set_direction(iodir = True, channel = 7, direction = False)
    
    while True:
        state = interface.read_input(True, 0)
        if state == 1:    
            interface.set_output(channel=7, bank = True, state = True)
        else:
            interface.set_output(channel=7, bank = True, state = False)
            
        time.sleep(.1)
    
    exit(0)