"""Script containg Typer CLI for making request on server."""
from asyncio import run as aiorun

import httpx
import orjson
import typer
from attrs import frozen
from typing_extensions import Annotated

from cli.common import console
from cli.common import epilog
from cli.common import err_console
from cli.common import print_json
from cli.common import verbose_console
from config import backend_settings

app = typer.Typer(
    name="request",
    add_completion=False,
    rich_markup_mode="rich",
    epilog=epilog,
)


@frozen
class TrackFeatures:
    track_id: str
    track_name: str
    track_artists: set[str]
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: float
    time_signature: int

    def __iter__(self):
        for k in self.__slots__:
            if not k.startswith("_"):
                v = self.__getattribute__(k)
                yield k, v


state = {"verbose": False}

client = httpx.AsyncClient()


async def make_request(url: str) -> list[TrackFeatures]:
    track_features: list[TrackFeatures] = []
    async with client.stream("GET", url) as response:
        async for chunk in response.aiter_bytes():
            track_features.extend(
                [TrackFeatures(**track) for track in orjson.loads(chunk).values()]
            )
            verbose_console.log(f"chunk: {chunk}")
    return track_features


@app.command(help="Request saved tracks")
def tracks(ctx: typer.Context):
    verbose_console.quiet = not state["verbose"]

    for extra_arg in ctx.args:
        verbose_console.log(f"Got extra arg: [bold]{extra_arg}[/bold]")

    endpoint = "/tracks/saved"
    url = f"{backend_settings.server_address}:56626{endpoint}"

    verbose_console.log(f"Making GET request on {url}")
    try:
        with verbose_console.status("Making GET request", spinner="arc"):
            track_features = aiorun(make_request(url=url))
        console.rule("Output", style="dim blue")
        console.print(track_features)
        # print_json(console, data=track_features)

    except httpx.HTTPStatusError as exc:
        err_console.print_exception()
        print_json(err_console, exc.response.text)

        raise typer.Exit(code=1) from exc


@app.command(help="Request model training")
def train(ctx: typer.Context):
    verbose_console.quiet = not state["verbose"]

    for extra_arg in ctx.args:
        verbose_console.log(f"Got extra arg: [bold]{extra_arg}[/bold]")

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
        data = response.json()
        console.rule("Output", style="dim blue")
        print_json(console, data=data)

    except httpx.HTTPStatusError as exc:
        err_console.print_exception()
        print_json(err_console, exc.response.text)

        raise typer.Exit(code=1) from exc


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
