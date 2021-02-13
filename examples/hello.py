import click
import click_spinner
import time


@click.command()
@click.option(
    "--beep",
    type=bool,
    default=False,
    show_default=True,
    help="""Beep when spinner finishes.""",
)
@click.option(
    "--disable",
    type=bool,
    default=False,
    show_default=True,
    help="""Hide spinner.""",
)
@click.option(
    "--force",
    type=bool,
    default=False,
    help="""Force creation of spinner even when stdout is redirected.""",
)
@click.option(
    "--direction",
    type=str,
    default="counter-clockwise",
    show_default=True,
    help="""Direction of spinner.
    Supported values are 'clockwise' and 'counter-clockwise'.
    """,
)
@click.option(
    "--duration",
    type=click.IntRange(min=1, max=10, clamp=True),
    default=5,
    show_default=True,
    help="""Amount of time to let spinner spin in program.""",
)
def hello(beep, disable, force, direction, duration):
    """Simple CLI that shows inputs to click_spinner.spinner."""
    with click_spinner.spinner(
        beep=beep, disable=disable, force=force, direction=direction
    ):
        time.sleep(duration)
    click.echo("That's how it works!")


if __name__ == "__main__":
    hello()
