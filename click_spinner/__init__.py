import sys
import threading
import time
import itertools


class Spinner(object):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self):
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self.init_spin)

    def start(self):
        self.spin_thread.start()

    def stop(self):
        self.stop_running.set()
        self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(next(self.spinner_cycle))
            sys.stdout.flush()
            time.sleep(0.25)
            sys.stdout.write('\b')

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def spinner():
    """This function creates a context manager that is used to display a
    spinner as long as the context has not exited.

    Example usage::

        with spinner():
            do_something()
            do_something_else()

    """
    return Spinner()


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
