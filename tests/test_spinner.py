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


class CMException(Exception):
    pass


def test_spinner_exc():
    @click.command()
    def cli():
       with click_spinner.spinner():
           for thing in range(10):
               if thing == 5:
                   raise CMException("foo")

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert isinstance(result.exception, CMException)
