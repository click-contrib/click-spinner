import itertools
import sys
import threading
from typing import Any, TextIO, Union


class Spinner(object):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self, beep: bool = False, disable: bool = False, force: bool = False,
                 stream: TextIO = sys.stdout) -> None:
        self.disable: bool = disable
        self.beep: bool = beep
        self.force: bool = force
        self.stream: TextIO = stream
        self.stop_running: Union[threading.Event, None] = None
        self.spin_thread: Union[threading.Thread, None] = None

    def start(self) -> None:
        if self.disable:
            return
        if self.stream.isatty() or self.force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self) -> None:
        if self.spin_thread:
            if self.stop_running:
                self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self) -> None:
        if self.stop_running:
            while not self.stop_running.is_set():
                self.stream.write(next(self.spinner_cycle))
                self.stream.flush()
                self.stop_running.wait(0.25)
                self.stream.write('\b')

        self.stream.write(' ')
        self.stream.write('\b')
        self.stream.flush()

    def __enter__(self) -> "Spinner":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        if self.disable:
            return False
        self.stop()
        if self.beep:
            self.stream.write('\7')
            self.stream.flush()
        return False


def spinner(beep: bool = False, disable: bool = False, force: bool = False, stream: TextIO = sys.stdout) -> Spinner:
    """This function creates a context manager that is used to display a
    spinner on stdout as long as the context has not exited.

    The spinner is created only if stdout is not redirected, or if the spinner
    is forced using the `force` parameter.

    Parameters
    ----------
    beep : bool
        Beep when spinner finishes.
    disable : bool
        Hide spinner.
    force : bool
        Force creation of spinner even when stdout is redirected.

    Example
    -------

        with spinner():
            do_something()
            do_something_else()

    """
    return Spinner(beep, disable, force, stream)


__version__ = '0.2.0'
