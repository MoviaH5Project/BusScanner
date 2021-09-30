# Use an interface to allow a different logger implementation to be used, without changing all references

class LoggerInterface:
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def log(self, message: str, level: int):
        pass

    def log_exception(self, message: str, exception: Exception):
        pass
