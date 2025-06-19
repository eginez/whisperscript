"""Main CLI entry point for WhisperScript."""

import click


@click.command()
@click.option("--debug", is_flag=True, help="Enable debug mode")
def cli(debug: bool) -> None:
    """Voice-controlled automation tool for macOS."""
    if debug:
        click.echo("Debug mode enabled")

    click.echo("WhisperScript starting...")
    # TODO: Implement main application logic


if __name__ == "__main__":
    cli()
