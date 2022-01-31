"""
CLI entry point.
"""
import warnings

import click

from .commands.geographic import geo
from .commands.setup import setup
from .commands.taxonomic import tax

warnings.filterwarnings("ignore")


@click.group()
def main():
    pass


main.add_command(geo)
main.add_command(setup)
main.add_command(tax)
