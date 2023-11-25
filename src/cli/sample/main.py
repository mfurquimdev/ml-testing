"""Script containing sample of Typer CLI."""
from datetime import datetime
from pathlib import Path
from typing import Union

import typer
from typing_extensions import Annotated

from cli.common import NeuralNetwork
from cli.common import console
from cli.common import epilog
from cli.common import err_console
from cli.common import validate_file_location
from cli.common import verbose_console

app = typer.Typer(
    name="sample",
    add_completion=False,
    rich_markup_mode="rich",
    epilog=epilog,
)

state = {"verbose": False}


@app.command(
    name="run_me",
    help="The only command in this sample.",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    epilog=epilog,
)
def replaced_by_name_in_command_decorator(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
    age: Annotated[int, typer.Option(prompt="How old are you?", min=18)] = 21,
    truth: Annotated[Union[bool, None], typer.Option("--truth/--lie", "-t/-f")] = None,
    date_reference: Annotated[
        Union[datetime, None],
        typer.Option(
            rich_help_panel="",
            help=r"[dim]\[default: today][/dim]",
            show_default=False,
            formats=["%Y-%m-%d"],
        ),
    ] = None,
    network: Annotated[NeuralNetwork, typer.Option(case_sensitive=False)] = NeuralNetwork.simple,
    location: Annotated[  # type: ignore
        Union[Path, None],
        typer.Option(exists=True, file_okay=True, dir_okay=False),
    ] = None,
):
    date_reference = date_reference or datetime.now()

    if state["verbose"]:
        for extra_arg in ctx.args:
            err_console.print(f"Got extra arg: {extra_arg}")

    location: Path = validate_file_location(location)

    console.print(
        f"Hello {name} ({age}) {truth} at {date_reference.date()} with "
        f"{network.value}.\nFile located at {location} contains {location.stat().st_size} chars"
    )


@app.callback(
    invoke_without_command=True,
)
def main(
    ctx: typer.Context,
    verbose: Annotated[bool, typer.Option("--verbose")] = False,
):
    """
    Sample code with most used features
    """
    if ctx.invoked_subcommand is None:
        err_console.print("Please, specify a command.")
        ctx.get_help()
        raise typer.Exit(code=1)

    if verbose:
        state["verbose"] = True
        verbose_console.print(f"About to execute command: [bold]{ctx.invoked_subcommand}[/bold]")


if __name__ == "__main__":
    app()
