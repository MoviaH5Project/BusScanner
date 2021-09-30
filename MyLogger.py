import logging
import traceback
import inspect
from LoggerInterface import LoggerInterface


class MyLogger(LoggerInterface):
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=logging.NOTSET)
        self.min_level = 20

    def get_caller(self):
        # region Taken from: https://stackoverflow.com/questions/17065086/how-to-get-the-caller-class-name-inside-a-function-of-another-class-in-python
        stack = inspect.stack()
        caller_class = stack[2][0].f_locals["self"].__class__.__name__
        caller_method = stack[2][0].f_code.co_name
        return caller_class, caller_method
        # endregion

    def log(self, message: str, level: int = logging.DEBUG):
        if level >= self.min_level:
            caller = self.get_caller()
            logging.log(msg=f"{caller[0]}.{caller[1]} - {message}", level=level)

    def log_exception(self, message: str, exception: Exception):
        self.log(f'{message}\n'
                 f'Exception: {exception}\n'
                 f'Traceback: {traceback.format_exc()}',
                 level=self.ERROR)
