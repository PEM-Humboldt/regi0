"""
CLI entry point.
"""
import click

from .geographic import geo
from .setup import setup


@click.group()
def main():
    pass


main.add_command(geo)
main.add_command(setup)
