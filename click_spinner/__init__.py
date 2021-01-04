import itertools
import sys
import threading
from types import TracebackType
from typing import IO, Literal, Optional, Type

from ._version import get_versions


class Spinner(object):
    spinner_cycle = itertools.cycle(["-", "/", "|", "\\"])

    def __init__(
        self,
        beep: bool = False,
        disable: bool = False,
        force: bool = False,
        stream: IO[str] = sys.stdout,
    ):
        self.disable = disable
        self.beep = beep
        self.force = force
        self.stream = stream
        self.stop_running: Optional[threading.Event] = None
        self.spin_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if self.disable:
            return
        if self.stream.isatty() or self.force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self) -> None:
        if self.spin_thread and self.stop_running:
            self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self) -> None:
        if self.stop_running:
            while not self.stop_running.is_set():
                self.stream.write(next(self.spinner_cycle))
                self.stream.flush()
                self.stop_running.wait(0.25)
                self.stream.write("\b")
                self.stream.flush()

    def __enter__(self) -> "Spinner":
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        if self.disable:
            return False
        self.stop()
        if self.beep:
            self.stream.write("\7")
            self.stream.flush()
        return False


def spinner(
    beep: bool = False,
    disable: bool = False,
    force: bool = False,
    stream: IO[str] = sys.stdout,
) -> "Spinner":
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


__version__ = get_versions()["version"]
del get_versions
