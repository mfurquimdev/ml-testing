"""Main script for Typer CLI."""
import typer
from typing_extensions import Annotated

from cli.common import epilog
from cli.request import app as request_app
from cli.sample import app as sample_app

app = typer.Typer(
    name="Main Code",
    add_completion=False,
    rich_markup_mode="rich",
    epilog=epilog,
)

app.add_typer(
    sample_app,
    name="sample",
    help="Sample code with most used features",
)

app.add_typer(
    request_app,
    name="request",
    help="Make request on server",
)


@app.callback()
def main():
    """
    Main script for Typer CLI.
    """


if __name__ == "__main__":
    app()
