from datetime import datetime
from enum import Enum
from typing import List
from typing import Tuple
from typing import Union

import typer
from rich.console import Console
from typing_extensions import Annotated

app = typer.Typer()
err_console = Console(stderr=True)

state = {"verbose": False}

valid_completion_items: List[Tuple[str, str]] = [
    ("Aurora", "The light of my life"),
    ("Larissa", "My life's partner"),
    ("Mateus", "Me self"),
    ("Olivia", "The youngest adorable daughter"),
    ("Romeo", "The brightest mind"),
]


def complete_name(incomplete: str):
    completion = []
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            completion_item = (name, help_text)
            completion.append(completion_item)
    return completion


class NeuralNetwork(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)
def post(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(autocompletion=complete_name)],
    age: Annotated[int, typer.Option(prompt="How old are you?", min=18)] = 21,
    truth: Annotated[Union[bool, None], typer.Option("--truth/--lie", "-t/-f")] = None,
    date_reference: Annotated[
        Union[datetime, None],
        typer.Option(
            help="Choose a date. Default is the current date.",
            show_default=False,
            formats=["%Y-%m-%d"],
        ),
    ] = None,
    network: Annotated[NeuralNetwork, typer.Option(case_sensitive=False)] = NeuralNetwork.simple,
):
    date_reference = date_reference or datetime.now()

    if state["verbose"]:
        for extra_arg in ctx.args:
            err_console.print(f"Got extra arg: {extra_arg}")

    print(
        f"Hello {name} ({age}) {'yes' if truth else 'no'} "
        f"at {date_reference.date()} with {network.value}"
    )


@app.command()
def get(age: int, name: str):
    print(f"Hello {name} ({age})")


@app.callback(
    invoke_without_command=True,
)
def main(ctx: typer.Context, verbose: bool = False):
    """
    Make requests to the API.
    """
    if verbose:
        state["verbose"] = True

    if ctx.invoked_subcommand is None:
        print(f"About to execute command: {ctx.invoked_subcommand}")


if __name__ == "__main__":
    app()
