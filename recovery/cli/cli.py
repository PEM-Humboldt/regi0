import click

from .commands.download import download
from .commands.setup import setup


@click.group()
def main():
    pass


main.add_command(download)
main.add_command(setup)
