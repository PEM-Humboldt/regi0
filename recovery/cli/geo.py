import click


@click.command()
@click.argument("src")
@click.argument("dst")
def main(src, dst):
    click.echo("Fuck!")


if __name__ == "__main__":
    main()
