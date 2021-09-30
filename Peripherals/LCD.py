import time

import threading

from Peripherals.GPIOHandler import GPIOHandler


class LCD:
    def __init__(self, gpio_handler: GPIOHandler):
        self.gpio_handler = gpio_handler
        self.lcd_lock = threading.Lock()

        # GPIO to LCD mapping
        self.LCD_RS = 26
        self.LCD_E = 24
        self.LCD_D4 = 22
        self.LCD_D5 = 18
        self.LCD_D6 = 16
        self.LCD_D7 = 12

        # Devices constants
        self.LCD_CHR = True  # Character mode
        self.LCD_CMD = False  # Command mode
        self.LCD_CHARS = 16  # Characters per line (16 max)
        self.LCD_LINE_1 = 0x80  # LCD memory location for 1st line
        self.LCD_LINE_2 = 0xC0  # LCD memory location 2nd line
        self.setup()

    # Define main program code
    def setup(self):
        # Set GPIO's to output mode
        self.gpio_handler.setup_pin(self.LCD_E, self.gpio_handler.OUT)
        self.gpio_handler.setup_pin(self.LCD_RS, self.gpio_handler.OUT)
        self.gpio_handler.setup_pin(self.LCD_D4, self.gpio_handler.OUT)
        self.gpio_handler.setup_pin(self.LCD_D5, self.gpio_handler.OUT)
        self.gpio_handler.setup_pin(self.LCD_D6, self.gpio_handler.OUT)
        self.gpio_handler.setup_pin(self.LCD_D7, self.gpio_handler.OUT)

        # Initialize display
        self.lcd_init()

        # Loop - send text and sleep 3 seconds between texts
        # Change text to anything you wish, but must be 16 characters or less
        '''
        lcd_text("Hello World!", LCD_LINE_1)
        lcd_text("", LCD_LINE_2)

        lcd_text("Rasbperry Pi", LCD_LINE_1)
        lcd_text("16x2 LCD Display", LCD_LINE_2)

        time.sleep(3)  # 3 second delay

        lcd_text("ABCDEFGHIJKLMNOP", LCD_LINE_1)
        lcd_text("1234567890123456", LCD_LINE_2)

        time.sleep(3)  # 3 second delay

        lcd_text("I love my", LCD_LINE_1)
        lcd_text("Raspberry Pi!", LCD_LINE_2)

        time.sleep(3)

        lcd_text("MBTechWorks.com", LCD_LINE_1)
        lcd_text("For more R Pi", LCD_LINE_2)

        time.sleep(3)
        '''

    # Initialize and clear display
    def lcd_init(self):
        self.lcd_write(0x33, self.LCD_CMD)  # Initialize
        self.lcd_write(0x32, self.LCD_CMD)  # Set to 4-bit mode
        self.lcd_write(0x06, self.LCD_CMD)  # Cursor move direction
        self.lcd_write(0x0C, self.LCD_CMD)  # Turn cursor off
        self.lcd_write(0x28, self.LCD_CMD)  # 2 line display
        self.lcd_write(0x01, self.LCD_CMD)  # Clear display
        time.sleep(0.0005)  # Delay to allow commands to process

    def lcd_write(self, bits, mode):
        # High bits
        self.gpio_handler.output(self.LCD_RS, mode)  # RS

        self.gpio_handler.output(self.LCD_D4, False)
        self.gpio_handler.output(self.LCD_D5, False)
        self.gpio_handler.output(self.LCD_D6, False)
        self.gpio_handler.output(self.LCD_D7, False)
        if bits & 0x10 == 0x10:
            self.gpio_handler.output(self.LCD_D4, True)
        if bits & 0x20 == 0x20:
            self.gpio_handler.output(self.LCD_D5, True)
        if bits & 0x40 == 0x40:
            self.gpio_handler.output(self.LCD_D6, True)
        if bits & 0x80 == 0x80:
            self.gpio_handler.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        self.gpio_handler.output(self.LCD_D4, False)
        self.gpio_handler.output(self.LCD_D5, False)
        self.gpio_handler.output(self.LCD_D6, False)
        self.gpio_handler.output(self.LCD_D7, False)
        if bits & 0x01 == 0x01:
            self.gpio_handler.output(self.LCD_D4, True)
        if bits & 0x02 == 0x02:
            self.gpio_handler.output(self.LCD_D5, True)
        if bits & 0x04 == 0x04:
            self.gpio_handler.output(self.LCD_D6, True)
        if bits & 0x08 == 0x08:
            self.gpio_handler.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        time.sleep(0.0005)
        self.gpio_handler.output(self.LCD_E, True)
        time.sleep(0.0005)
        self.gpio_handler.output(self.LCD_E, False)
        time.sleep(0.0005)

    def lcd_text(self, message, line):
        with self.lcd_lock:
            # Send text to display
            message = message.ljust(self.LCD_CHARS, " ")

            self.lcd_write(line, self.LCD_CMD)

            for i in range(self.LCD_CHARS):
                self.lcd_write(ord(message[i]), self.LCD_CHR)
        time.sleep(0.1)