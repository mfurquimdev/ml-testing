"""Main script for Typer CLI."""
import typer

from cli.common import console
from cli.common import epilog
from cli.common import err_console
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


@app.callback()
def main():
    """
    Make requests to the API.
    """


if __name__ == "__main__":
    app()
