from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List
from typing import Tuple
from typing import Union

import typer
from typing_extensions import Annotated

from cli.common import console
from cli.common import epilog
from cli.common import err_console

app = typer.Typer(
    name="Sample Code",
    add_completion=False,
    rich_markup_mode="rich",
    epilog=epilog,
)

state = {"verbose": False}


class NeuralNetwork(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


def validate_file_location(location: Union[Path, None]) -> Path:
    if location is None:
        err_console.print("Please, provide file path with --location")
        raise typer.Exit(code=2)

    if (
        location.is_socket()
        or location.is_fifo()
        or location.is_block_device()
        or location.is_char_device()
    ):
        err_console.print("The given location does not point to a regular file.")
        raise typer.Exit(code=2)

    if location.is_symlink():
        console.print("Careful, this is a symlink, not a file", style="yellow underline")

    return location


@app.command(
    name="run_me",
    help="The only command in this sample.",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    epilog=epilog,
)
def sample(
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
        raise typer.Exit(code=1)

    if verbose:
        state["verbose"] = True
        console.print(f"About to execute command: {ctx.invoked_subcommand}")


if __name__ == "__main__":
    app()
