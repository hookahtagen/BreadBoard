import Adafruit_ADS1x15
import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO
import os
import random
import RPi.GPIO as rgpio
import time

from threading import Thread


def clear_screen():
    # Determine the command to clear the console based on the current operating system
    os.system("clear")


class InterfaceController:
    MCP23017_ADDR = 0x20
    ADS1115_ADDR = 0x4b
    BUS_NUM = 3

    POWER_SWITCH_CHANNEL = 26
    POWER_RELAY_CHANNEL = 0
    POWER_ENABLE = False

    SHOW_WARNING = True

    RAIL_1_ENABLED = False
    RAIL_2_ENABLED = False
    RAIL_3_ENABLED = False
    CUSTOM_RAIL_ENABLED = False

    EMERGENGY_STOP_PRESSED = False
    RESET_BUTTON_PRESSED = False

    VOLTAGE_TOLERANCE = .1

    def __init__(self, name="mcp_controller"):
        self.name = name
        self.mcp = MCP.MCP23017(
            address=self.MCP23017_ADDR, busnum=self.BUS_NUM)
        self.adc = Adafruit_ADS1x15.ADS1115(
            address=self.ADS1115_ADDR, busnum=self.BUS_NUM)

        rgpio.setmode(rgpio.BCM)
        rgpio.setup(self.POWER_SWITCH_CHANNEL, rgpio.IN)

        self.monitoring_running = False
        self.voltage_monitoring = Thread(target=self.power_manipulator)
    
    def check_voltages(self):
        GAIN = 2/3
        voltages = [(self.adc.read_adc(channel, gain=GAIN) * 0.0001875) for channel in range(4)]
        
        if not self.EMERGENGY_STOP_PRESSED and self.POWER_ENABLE:
            self.RAIL_1_ENABLED = True
            self.RAIL_2_ENABLED = True
            self.RAIL_3_ENABLED = True
        
        if not (3.3 - self.VOLTAGE_TOLERANCE <= voltages[3] <= 3.3 + self.VOLTAGE_TOLERANCE):
            self.POWER_ENABLE = False
            self.RAIL_1_ENABLED = False
        
        if not (4.95 - self.VOLTAGE_TOLERANCE <= voltages[2]*2 <= 5.05 + self.VOLTAGE_TOLERANCE):
            self.POWER_ENABLE = False
            self.RAIL_2_ENABLED = False
        
        if not (11.95 - self.VOLTAGE_TOLERANCE <= voltages[1]*2 <= 12.05 + self.VOLTAGE_TOLERANCE):
            # self.POWER_ENABLE = False
            self.RAIL_3_ENABLED = False
            
        
        return voltages

    def power_manipulator(self):
        while self.monitoring_running:
            clear_screen()
            

            if self.mcp.input(8) == GPIO.HIGH:
                self.RAIL_1_ENABLED = False
                self.RAIL_2_ENABLED = False
                self.RAIL_3_ENABLED = False
                
                self.toggle_main_power()
                
                self.mcp.output(self.POWER_RELAY_CHANNEL, True)
                self.POWER_ENABLE = False
                self.EMERGENGY_STOP_PRESSED = True
                
            elif self.mcp.input(9) == GPIO.HIGH:
                self.RESET_BUTTON_PRESSED = True
                self.EMERGENGY_STOP_PRESSED = False
                self.POWER_ENABLE = True                
                
            elif self.mcp.input(9) == GPIO.LOW:
                self.RESET_BUTTON_PRESSED = False    

            voltages = self.check_voltages()
            self.toggle_main_power()
            
            round_level = 2 
            display_message = f"""
                **************************************
                *  3.3V rail:  {'enabled' if self.RAIL_1_ENABLED else 'disabled'} at Voltage {round(voltages[3], round_level)}      *
                *  5V rail:    {'enabled' if self.RAIL_2_ENABLED else 'disabled'} at Voltage {round(voltages[2]*2, round_level)}      *
                *  12V rail:   {'enabled' if self.RAIL_3_ENABLED else 'disabled'} at Voltage {round(voltages[1], round_level)}      *
                *  5-15V rail: {'enabled' if self.CUSTOM_RAIL_ENABLED else 'disabled'} at Voltage {round(voltages[0], round_level)}  *
                *  5V rail:         enabled at Voltage 3.23V    *
                *  Emergency stop:  not pressed                 *
                *  Emergency stop: {'pressed' if self.EMERGENGY_STOP_PRESSED else 'not pressed'}                    *
                *  Reset button:   {'pressed' if self.RESET_BUTTON_PRESSED else 'not pressed'}                      *
                **************************************
                """
                

            print(display_message)
            time.sleep(.25)

        print("Monitoring stopped!")

    def start(self):
        self.monitoring_running = True
        self.voltage_monitoring.start()

    def stop(self):
        # self.voltage_monitoring.join()
        self.monitoring_running = False

    def setup(self):
        # Set all pins of bank A to output
        for pin in range(0, 8):
            self.mcp.setup(pin, GPIO.OUT)

        # Set all pins of bank B to output
        for pin in range(8, 16):
            self.mcp.setup(pin, GPIO.IN)

        # Dictionary with pin as key and state as value
        pin_states = {pin: state for pin, state in zip(
            range(16), [True] * 8 + [False] * 8)}

        self.mcp.output_pins(pin_states)

        self.POWER_ENABLE = True

    def toggle_main_power(self):
        if self.POWER_ENABLE:
            if self.RAIL_1_ENABLED:
                self.mcp.output(0, not self.RAIL_1_ENABLED)
            if self.RAIL_2_ENABLED:
                self.mcp.output(1, not self.RAIL_2_ENABLED)
        elif not self.POWER_ENABLE:
            self.mcp.output(0, not self.RAIL_1_ENABLED)
            
            self.mcp.output(1, not self.RAIL_2_ENABLED)

    def machine_gun(self, delay=.1):
        DELAY = delay
        # Set pin 0 in bank A to output
        self.mcp.setup(0, GPIO.OUT)

        # Rapidly toggle the state of pin 0 in bank A to simulate a machine gun effect
        for i in range(10):
            for channel in range(8):
                self.mcp.output(channel, not False)
                time.sleep(random.uniform(.01, .1))
                self.mcp.output(channel, not True)
                time.sleep(random.uniform(.01, .2))

        for channel in range(8):
            self.mcp.output(channel, not False)


if __name__ == '__main__':

    controller = InterfaceController()
    controller.setup()
    controller.start()

    try:
        while True:
            time.sleep(.01)
    except KeyboardInterrupt:
        pass

    controller.stop()
    exit(0)
