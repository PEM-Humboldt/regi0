"""
Common options using across two or more recovery CLI interfaces.
"""

import click

quiet = click.option(
    "--quiet",
    default=False,
    is_flag=True,
    help="Silence information logging.",
    show_default=True
)
