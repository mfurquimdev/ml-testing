"""Main script for Typer CLI."""
import typer

from cli.common import epilog
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
    Main script for Typer CLI.
    """


if __name__ == "__main__":
    app()
