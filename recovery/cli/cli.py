import click

from .commands.setup import setup


@click.group()
def main():
    pass


main.add_command(setup)
