import click
from click.testing import CliRunner

import click_spinner


def test_spinner():
    @click.command()
    def cli():
       with click_spinner.spinner():
           for thing in range(10):
               pass

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exception is None


def test_spinner_resume():
    @click.command()
    def cli():
       spinner = click_spinner.Spinner()
       spinner.start()
       for thing in range(10):
           pass
       spinner.stop()
       spinner.start()
       for thing in range(10):
           pass
       spinner.stop()

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exception is None

