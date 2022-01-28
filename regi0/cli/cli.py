"""
CLI entry point.
"""
import click

from regi0.cli.commands.geographic import geo
from regi0.cli.commands.setup import setup


@click.group()
def main():
    pass


main.add_command(geo)
main.add_command(setup)
