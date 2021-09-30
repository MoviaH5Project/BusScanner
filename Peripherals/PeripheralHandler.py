import time

from Peripherals.Buzzer import Buzzer
from Peripherals.LCD import LCD
from Peripherals.LED import LED
from Peripherals.GPIOHandler import GPIOHandler


class PeripheralHandler:
    def __init__(self):
        self.gpio_handler = GPIOHandler()
        self.buzzer = Buzzer(self.gpio_handler)
        self.led = LED(self.gpio_handler)
        self.lcd = LCD(self.gpio_handler)
        self.default()

    def default(self):
        self.led.rgb_led_color(0, 0, 1)
        self.lcd.lcd_text("Please scan", self.lcd.LCD_LINE_1)
        self.lcd.lcd_text("Card or Phone", self.lcd.LCD_LINE_2)

    def scanned(self):
        self.buzzer.play_melody(self.buzzer.melodies[0])
        self.led.rgb_led_color()

    def success(self):
        self.buzzer.play_melody(self.buzzer.melodies[1])
        self.led.rgb_led_color(0, 100, 0)
        self.lcd.lcd_text("Enjoy your trip", self.lcd.LCD_LINE_2)

    def fail(self):
        self.buzzer.play_melody(self.buzzer.melodies[2])
        self.led.rgb_led_color(100, 0, 0)

    def phone_scanned(self):
        self.lcd.lcd_text("Phone scanned", self.lcd.LCD_LINE_1)
        self.scanned()
        time.sleep(1)
        self.default()

    def card_scanned(self):
        self.lcd.lcd_text("Card scanned", self.lcd.LCD_LINE_1)
        self.scanned()
        time.sleep(1)
        self.default()
