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

