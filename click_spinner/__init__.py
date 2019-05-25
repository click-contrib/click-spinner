import sys
import threading
import time
import itertools

# Non-default spinners copied from https://github.com/molovo/revolver
# Credit to James Dindale 
spinner_types ={
    'default': ['-', '/', '|', '\\'],
    'dots': [ '⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏',],
    'dots2': [ '⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷',],
    'dots3': [ '⠋', '⠙', '⠚', '⠞', '⠖', '⠦', '⠴', '⠲', '⠳', '⠓',],
    'dots4': [ '⠄', '⠆', '⠇', '⠋', '⠙', '⠸', '⠰', '⠠', '⠰', '⠸', '⠙', '⠋', '⠇', '⠆',],
    'dots5': [ '⠋', '⠙', '⠚', '⠒', '⠂', '⠂', '⠒', '⠲', '⠴', '⠦', '⠖', '⠒', '⠐', '⠐', '⠒', '⠓', '⠋',],
    'dots6': [ '⠁', '⠉', '⠙', '⠚', '⠒', '⠂', '⠂', '⠒', '⠲', '⠴', '⠤', '⠄', '⠄', '⠤', '⠴', '⠲', '⠒', '⠂', '⠂', '⠒', '⠚', '⠙', '⠉', '⠁',],
    'dots7': [ '⠈', '⠉', '⠋', '⠓', '⠒', '⠐', '⠐', '⠒', '⠖', '⠦', '⠤', '⠠', '⠠', '⠤', '⠦', '⠖', '⠒', '⠐', '⠐', '⠒', '⠓', '⠋', '⠉', '⠈',],
    'dots8': [ '⠁', '⠁', '⠉', '⠙', '⠚', '⠒', '⠂', '⠂', '⠒', '⠲', '⠴', '⠤', '⠄', '⠄', '⠤', '⠠', '⠠', '⠤', '⠦', '⠖', '⠒', '⠐', '⠐', '⠒', '⠓', '⠋', '⠉', '⠈', '⠈',],
    'dots9': [ '⢹', '⢺', '⢼', '⣸', '⣇', '⡧', '⡗', '⡏',],
    'dots10': [ '⢄', '⢂', '⢁', '⡁', '⡈', '⡐', '⡠'],
    'dots11': [ '⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈',],
    'dots12': [ "⢀⠀", "⡀⠀", "⠄⠀", "⢂⠀", "⡂⠀", "⠅⠀", "⢃⠀", "⡃⠀", "⠍⠀", "⢋⠀", "⡋⠀", "⠍⠁", "⢋⠁", "⡋⠁", "⠍⠉", "⠋⠉", "⠋⠉", "⠉⠙", "⠉⠙", "⠉⠩", "⠈⢙", "⠈⡙", "⢈⠩", "⡀⢙", "⠄⡙", "⢂⠩", "⡂⢘", "⠅⡘", "⢃⠨", "⡃⢐", "⠍⡐", "⢋⠠", "⡋⢀", "⠍⡁", "⢋⠁", "⡋⠁", "⠍⠉", "⠋⠉", "⠋⠉", "⠉⠙", "⠉⠙", "⠉⠩", "⠈⢙", "⠈⡙", "⠈⠩", "⠀⢙", "⠀⡙", "⠀⠩", "⠀⢘", "⠀⡘", "⠀⠨", "⠀⢐", "⠀⡐", "⠀⠠", "⠀⢀", "⠀⡀"],
    'line':  ['-', '\\', '|', '/',],
    'line2': ['⠂', '-', '–', '—', '–', '-'],
    'pipe':  ['┤', '┘', '┴', '└', '├', '┌', '┬', '┐',],
    'simpleDots': [".  ", ".. ", "...", "   ",],
    'simpleDotsScrolling': [".  ", ".. ", "...", " ..", "  .", "   ",],
    'star': [ "✶", "✸", "✹", "✺", "✹", "✷"],
    'star2': [ "+", "x", "*",],
    'flip': [ "_", "_", "_", "-", "\`", "\`", "'", "´", "-", "_", "_", "_",],
    'hamburger': ["☱", "☲", "☴",],
    'growVertical': [ "▁", "▃", "▄", "▅", "▆", "▇", "▆", "▅", "▄", "▃"],
    'growHorizontal': [ "▏", "▎", "▍", "▌", "▋", "▊", "▉", "▊", "▋", "▌", "▍", "▎",],
    'balloon': [ ", " ".", "o", "O", "@", "*", " "],
    'balloon2': [ ".", "o", "O", "°", "O", "o", ".",],
    'noise': ["░"],
    'bounce': ["⠁", "⠂", "⠄", "⠂",],
    'boxBounce': [ "▖", "▘", "▝", "▗"],
    'boxBounce2': ["▌", "▀", "▐", "▄"],
    'triangle': [ "◢", "◣", "◤", "◥",],
    'arc': ["◜","◠", "◝", "◞", "◡", "◟",],
    'circle': [ "◡", "⊙", "◠",],
    'squareCorners':  [ "◰", "◳", "◲", "◱",],
    'circleQuarters': [ "◴", "◷", "◶", "◵",],
    'circleHalves': [ "◐", "◓", "◑", "◒",],
    'squish':  ["╫", "╪",],
    'toggle': [ "⊶", "⊷",],
    'toggle2':[ "▫", "▪",],
    'toggle3':[ "□", "■",],
    'toggle4': ["■", "□", "▪", "▫",],
    'toggle5': ["▮", "▯",],
    'toggle6': ["ဝ", "၀",],
    'toggle7': ["⦾", "⦿",],
    'toggle8': ["◍", "◌",],
    'toggle9': ["◉", "◎",],
    'toggle10': ["㊂", "㊀", "㊁"],
    'toggle11': [ "⧇", "⧆",],
    'toggle12': [ "☗", "☖",],
    'toggle13': [ "=", "*", "-"],
    'arrow': ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙",],
    #'arrow2': [ "▹▹▹▹▹", "▸▹▹▹▹", "▹▸▹▹▹", "▹▹▸▹▹", "▹▹▹▸▹", "▹▹▹▹▸"],
    #'bouncingBar': [ "[    ]", "[   =]", "[  ==]", "[ ===]", "[====]", "[=== ]", "[==  ]", "[=   ]"],
    #'bouncingBall': [ "( ●    )", "(  ●   )", "(   ●  )", "(    ● )", "(     ●)", "(    ● )", "(   ●  )", "(  ●   )", "( ●    )", "(●     )"],
    #'pong': [ "▐⠂       ▌", "▐⠈       ▌", "▐ ⠂      ▌", "▐ ⠠      ▌", "▐  ⡀     ▌", "▐  ⠠     ▌", "▐   ⠂    ▌", "▐   ⠈    ▌", "▐    ⠂   ▌", "▐    ⠠   ▌", "▐     ⡀  ▌", "▐     ⠠  ▌", "▐      ⠂ ▌", "▐      ⠈ ▌", "▐       ⠂▌", "▐       ⠠▌", "▐       ⡀▌", "▐      ⠠ ▌", "▐      ⠂ ▌", "▐     ⠈  ▌", "▐     ⠂  ▌", "▐    ⠠   ▌", "▐    ⡀   ▌", "▐   ⠠    ▌", "▐   ⠂    ▌", "▐  ⠈     ▌", "▐  ⠂     ▌", "▐ ⠠      ▌", "▐ ⡀      ▌", "▐⠠       ▌"],
    #'shark': [ "▐|\\____________▌", "▐_|\\___________▌", "▐__|\\__________▌", "▐___|\\_________▌", "▐____|\\________▌", "▐_____|\\_______▌", "▐______|\\______▌", "▐_______|\\_____▌", "▐________|\\____▌", "▐_________|\\___▌", "▐__________|\\__▌", "▐___________|\\_▌", "▐____________|\\▌", "▐____________/|▌", "▐___________/|_▌", "▐__________/|__▌", "▐_________/|___▌", "▐________/|____▌", "▐_______/|_____▌", "▐______/|______▌", "▐_____/|_______▌", "▐____/|________▌", "▐___/|_________▌", "▐__/|__________▌", "▐_/|___________▌", "▐/|____________▌"],
}

class Spinner(object):

    def __init__(self, beep=False, disable=False, force=False, spinner_type='default', custom_spinner=None):
        self.disable = disable
        self.beep = beep
        self.force = force
        self.stop_running = None
        self.spin_thread = None
        if custom_spinner: # User can provide their own spinner as a list of strings
            self.spinner_cycle = itertools.cycle(custom_spinner)
        else: 
            self.spinner_cycle = itertools.cycle(spinner_types[spinner_type])

    def start(self):
        if self.disable:
            return
        if sys.stdout.isatty() or self.force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self):
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(next(self.spinner_cycle))
            sys.stdout.flush()
            time.sleep(0.25)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disable:
            return False
        self.stop()
        if self.beep:
            sys.stdout.write('\7')
            sys.stdout.flush()
        return False


def spinner(beep=False, disable=False, force=False, spinner_type='default', custom_spinner=None):
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
    spinner_type: string
        Optionally specify the type of spinner to use.
    custom_spinner: list 
        Optionally provide a custom spinner as a list of ASCII characters.

    Example
    -------

        with spinner():
            do_something()
            do_something_else()

    """
    return Spinner(beep, disable, force, spinner_type, custom_spinner)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
