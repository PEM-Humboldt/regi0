"""
CLI entry point.
"""
import click

from .commands.download import download
from .commands.geographic import geographic
from .commands.setup import setup
from .commands.taxonomic import taxonomic


@click.group()
def main():
    pass


main.add_command(download)
main.add_command(geographic)
main.add_command(setup)
main.add_command(taxonomic)
