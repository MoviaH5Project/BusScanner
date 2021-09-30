import time, threading
import RPi.GPIO as GPIO

from CallFunctionNonBlocking import call_function_non_blocking


class GPIOHandler:
    def __init__(self):
        # Set board mode (pin addressing)
        GPIO.setmode(GPIO.BOARD)
        # create a dictionary to hold pwm objects with pin number as key
        self.pwm_pin = {int: GPIO.PWM}
        self.OUT = GPIO.OUT
        self.IN = GPIO.IN

    def __del__(self):
        # On destruction clean up GPIO
        GPIO.cleanup()

    # Loop over pwm pins, set frequency, duty cycle, start them and if they arent in the pwm dictionary add them
    def turn_on_pins_pwm(self, frequency=100, duty_cycle=100, *pins):
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            if pin not in self.pwm_pin:
                self.pwm_pin[pin] = GPIO.PWM(pin, frequency)
            self.pwm_pin[pin].start(duty_cycle)

    # Change the frequency of pins
    def change_frequency(self, frequency, *pins):
        for pin in pins:
            if pin in self.pwm_pin:
                self.pwm_pin[pin].ChangeFrequency(frequency)

    # Turn off pwm pins
    def turn_off_pins_pwm(self, *pins):
        for pin in pins:
            if pin in self.pwm_pin:
                self.pwm_pin[pin].stop()

    # Method for thread to use to turn off pins after delay without blocking
    def _turn_off_delay(self, delay, *pins):
        time.sleep(delay)
        self.turn_off_pins(*pins)

    # Turn off pins after delay, non blocking
    def turn_off_delay(self, delay=1, *pins):
        call_function_non_blocking(self._turn_off_delay, delay, *pins)

    # Method for thread to use to turn off pwm pins after delay without blocking
    def _turn_off_pwm_delay(self, delay, *pins):
        time.sleep(delay)
        self.turn_off_pins_pwm(*pins)

    # Turn off pwm pins after delay, non blocking
    def turn_off_pwm_delay(self, delay=1, *pins):
        call_function_non_blocking(self._turn_off_pwm_delay, delay, *pins)

    # Turn on pins
    def turn_on_pins(self, *pins):
        for pin in pins:
            self.setup_pin(pin, GPIO.OUT)
            self.output(pin, GPIO.HIGH)

    # Turn off pins
    def turn_off_pins(self, *pins):
        for pin in pins:
            self.setup_pin(pin, GPIO.OUT)
            self.output(pin, GPIO.LOW)

    def setup_pin(self, pin, mode):
        GPIO.setup(pin, mode)

    def output(self, pin, on):
        GPIO.output(pin, on)
