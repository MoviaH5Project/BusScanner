from Peripherals.GPIOHandler import GPIOHandler


class LED:

    def __init__(self, gpio_handler: GPIOHandler):
        # Define the pins that the LED is attached to (GPIO.BOARD format)
        self.redPin = 23
        self.greenPin = 32
        self.bluePin = 33
        self.gpio_handler = gpio_handler

    def __del__(self):
        self.turn_off_leds(self.redPin, self.greenPin, self.bluePin)

    def turn_on_led_pwm(self, pin, frequency=100, duty_cycle=100):
        # If frequency is set to zero, turn off LED to avoid GPIOHandler throwing an exception
        if frequency == 0:
            self.gpio_handler.turn_off_pins_pwm(pin)
        else:
            self.gpio_handler.turn_on_pins_pwm(frequency, duty_cycle, pin)

    def turn_off_leds(self, *pins):
        self.gpio_handler.turn_off_pins_pwm(*pins)

    # Method combining the logic, taking 3 values for red, green and blue power, their individual blink rates
    # and the delay before they should be turned off
    def rgb_led_color(self, red_power=100, green_power=100, blue_power=100, red_blink=100, green_blink=100,
                      blue_blink=100, turn_off_delay=0):
        self.turn_on_led_pwm(self.redPin, red_power, red_blink)
        self.turn_on_led_pwm(self.greenPin, green_power, green_blink)
        self.turn_on_led_pwm(self.bluePin, blue_power, blue_blink)
        if turn_off_delay != 0:
            self.gpio_handler.turn_off_pwm_delay(turn_off_delay, self.redPin, self.greenPin, self.bluePin)
