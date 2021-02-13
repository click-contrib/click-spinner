import sys
import threading
import itertools
from ._version import get_versions

_iter_vals = ["-", "/", "|", "\\"]


class Spinner(object):
    spinner_iter = _iter_vals

    def __init__(
        self,
        beep: bool = False,
        disable: bool = False,
        force: bool = False,
        stream=sys.stdout,
        direction: str = "counter-clockwise",
    ):
        if not isinstance(beep, bool):
            raise TypeError("must be bool, not %s" % (type(beep).__name__))
        self.beep = beep

        if not isinstance(disable, bool):
            raise TypeError("must be bool, not %s" % (type(disable).__name__))
        self.disable = disable

        if not isinstance(force, bool):
            raise TypeError("must be bool, not %s" % (type(force).__name__))
        self.force = force

        self.stream = stream
        self.stop_running = None
        self.spin_thread = None

        if not isinstance(direction, str):
            raise TypeError("must be str, not %s" % (type(direction).__name__))
        if direction == "clockwise":
            self.spinner_iter = [
                element for element in reversed(self.spinner_iter)
            ]
        elif direction == "counter-clockwise":
            pass
        else:
            raise ValueError(
                "unsupported value '%s' for direction" % (direction)
            )
        self.direction = direction

        self.spinner_cycle = itertools.cycle(self.spinner_iter)

    def start(self):
        if self.disable:
            return
        if self.stream.isatty() or self.force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self):
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            self.stream.write(next(self.spinner_cycle))
            self.stream.flush()
            self.stop_running.wait(0.25)
            self.stream.write("\b")
            self.stream.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
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
    stream=sys.stdout,
    direction: str = "counter-clockwise",
):
    """This function creates a context manager that is used to display a
    spinner on stdout as long as the context has not exited.

    The spinner is created only if stdout is not redirected, or if the spinner
    is forced using the `force` parameter.

    Parameters
    ----------
    beep : bool, default = False
        Beep when spinner finishes.
    disable : bool, default = False
        Hide spinner.
    force : bool, default = False
        Force creation of spinner even when stdout is redirected.
    direction: str, default = "clockwise"
        Direction of spinner. Supported values are:
            - "clockwise"
            - "counter-clockwise"

    Example
    -------

        with spinner():
            do_something()
            do_something_else()

    """
    if not isinstance(beep, bool):
        raise TypeError("must be bool, not %s" % (type(beep).__name__))

    if not isinstance(beep, bool):
        raise TypeError("must be bool, not %s" % (type(disable).__name__))

    if not isinstance(force, bool):
        raise TypeError("must be bool, not %s" % (type(force).__name__))

    if not isinstance(direction, str):
        raise TypeError("must be str, not %s" % (type(direction).__name__))

    return Spinner(beep, disable, force, stream, direction)


__version__ = get_versions()["version"]
del get_versions
