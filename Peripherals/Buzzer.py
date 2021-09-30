import time

from Peripherals.GPIOHandler import GPIOHandler
from CallFunctionNonBlocking import call_function_non_blocking
import threading


class Buzzer:
    def __init__(self, gpio_handler: GPIOHandler):
        self.gpio_handler = gpio_handler
        self.buzzer_pin = 7
        self.buzzer_lock = threading.Lock()
        # Define some melodies, they are defined as [frequency, duration]
        self.melodies = [
            [[500, 0.1]],
            [[800, 0.1], [1600, 0.1]],
            [[200, 0.1], [100, 0.1]]
        ]

    def play_node(self, node):
        self.gpio_handler.change_frequency(node, self.buzzer_pin)

    def _play_melody(self, melody):
        with self.buzzer_lock:
            self.gpio_handler.turn_on_pins_pwm(1, 50, self.buzzer_pin)
            for part in melody:
                self.play_node(part[0])
                time.sleep(part[1])
            self.gpio_handler.turn_off_pins_pwm(self.buzzer_pin)

    def play_melody(self, melody):
        call_function_non_blocking(self._play_melody, melody)