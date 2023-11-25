"""Script containing common variables and functions."""
from pathlib import Path
from typing import Union

import typer
from rich.console import Console

epilog = r"[dim]Made in brazil by [bold blue]MFurquim Dev[/bold blue][/dim]"
err_console = Console(stderr=True, style="bold red")
console = Console()


def validate_file_location(location: Union[Path, None]) -> Path:
    if location is None:
        err_console.print("Please, provide file path with --location")
        raise typer.Exit(code=1)

    if (
        location.is_socket()
        or location.is_fifo()
        or location.is_block_device()
        or location.is_char_device()
    ):
        err_console.print("The given location does not point to a regular file.")
        raise typer.Exit(code=1)

    if location.is_symlink():
        console.print("Careful, this is a symlink, not a file", style="yellow underline")

    return location
