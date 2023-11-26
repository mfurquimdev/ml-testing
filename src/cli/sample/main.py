"""Script containing sample of Typer CLI."""
import time
from datetime import datetime
from pathlib import Path
from typing import Union

import httpx
import typer
from typing_extensions import Annotated

from cli.common import NeuralNetwork
from cli.common import console
from cli.common import epilog
from cli.common import err_console
from cli.common import print_json
from cli.common import validate_file_location
from cli.common import verbose_console
from config import backend_settings

app = typer.Typer(
    name="sample",
    add_completion=False,
    rich_markup_mode="rich",
    epilog=epilog,
)

state = {"verbose": False}


def raise_exception():
    """Sleep 2 seconds and raise exception"""
    time.sleep(2)

    message: str = (
        "Client error '422 Unprocessable Entity' for url"
        "'http://localhost:44681/sample/1?name=test'\nFor more information check:"
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422"
    )

    request: httpx.Request = httpx.Request(
        method="POST",
        url="http://localhost:44681/sample/1?name=test",
    )

    response: httpx.Response = httpx.Response(
        status_code=422,
        json={
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.5/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["body", "num"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.5/v/missing",
                },
            ]
        },
    )
    raise httpx.HTTPStatusError(message, request=request, response=response)


@app.command(
    name="run_me",
    help="A command with most common typer features.",
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
    error: Annotated[
        bool, typer.Option("--error", "-e", is_flag=True, help="Force raising an exception.")
    ] = False,
):
    # Get default value from a function
    date_reference = date_reference or datetime.now()

    # Identify and print all unrecognized arguments
    for extra_arg in ctx.args:
        verbose_console.log(f"Got extra arg: {extra_arg}")

    # Custom validation of parameter
    location: Path = validate_file_location(location)

    if error:
        try:
            with console.status("Generating sample exception", spinner="arc"):
                raise_exception()

        except httpx.HTTPStatusError as exc:
            err_console.print_exception()
            print_json(err_console, data=exc.response.json())

            raise typer.Exit(code=1) from exc

    console.print(
        f"Hello {name} ({age}) {truth} at {date_reference.date()} with "
        f"{network.value}.\nFile located at {location} contains {location.stat().st_size} chars"
    )


@app.command(help="Sample POST request on /sample/{id} endpoint.")
def request():
    path_param = "1"
    query_params = {"name": "test"}
    body_params = {"name": "asd", "num": 2}

    endpoint = f"/sample/{path_param}"
    url = f"{backend_settings.server_address}:{backend_settings.port_number}{endpoint}"

    verbose_console.log(
        f"Making POST request on {url} with "
        f"query params: {query_params} and body params: {body_params}"
    )
    try:
        with verbose_console.status("Making POST request", spinner="arc"):
            response = httpx.post(url, params=query_params, json=body_params).raise_for_status()

        verbose_console.rule("[white]Output", style="dim blue")
        print_json(console, data=response.json())

    except httpx.HTTPStatusError as exc:
        err_console.print_exception()
        print_json(err_console, exc.response.text)

        raise typer.Exit(code=1) from exc


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
    # Custom message if no command is provided
    if ctx.invoked_subcommand is None:
        err_console.log("Please, specify a command.")
        ctx.get_help()
        raise typer.Exit(code=1)

    # Forward verbose state to commands
    state["verbose"] = verbose

    # Disable the verbose console if verbose is not set
    verbose_console.quiet = not verbose

    verbose_console.log(f"About to execute command: [bold]{ctx.invoked_subcommand}[/bold]")


if __name__ == "__main__":
    app()
