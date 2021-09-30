import threading


def call_function_non_blocking(function, *args):
    thread = threading.Thread(target=function, args=(args))
    thread.start()
