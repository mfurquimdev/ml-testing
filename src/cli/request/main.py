"""Script containg Typer CLI for making request on server."""
import typer
from typing_extensions import Annotated

from cli.common import console
from cli.common import epilog
from cli.common import err_console
from cli.common import verbose_console

app = typer.Typer(
    name="request",
    add_completion=False,
    rich_markup_mode="rich",
    epilog=epilog,
)

state = {"verbose": False}


@app.command(help="Request model training")
def train(
    ctx: typer.Context,
):
    if state["verbose"]:
        for extra_arg in ctx.args:
            verbose_console.log(f"Got extra arg: [bold]{extra_arg}[/bold]")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: Annotated[bool, typer.Option("--verbose")] = False,
):
    """
    Make request on server
    """
    if ctx.invoked_subcommand is None:
        err_console.log("Please, specify a command.")
        ctx.get_help()
        raise typer.Exit(code=1)

    if verbose:
        state["verbose"] = True
        verbose_console.log(f"About to execute command: [bold]{ctx.invoked_subcommand}[/bold]")
