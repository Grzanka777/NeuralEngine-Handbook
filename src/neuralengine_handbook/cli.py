from pathlib import Path
import typer

from neuralengine_handbook.builder import build

app = typer.Typer(no_args_is_help=True)


@app.command()
def build_all(
    root: Path = typer.Option(
        Path("."),
        "--root",
        help="Handbook repository root.",
        exists=True,
        file_okay=False,
        dir_okay=True,
    )
) -> None:
    """Generate all handbook outputs."""
    outputs = build(root.resolve())
    for output in outputs:
        typer.echo(output)


@app.command("build")
def build_command(
    root: Path = typer.Option(
        Path("."),
        "--root",
        help="Handbook repository root.",
        exists=True,
        file_okay=False,
        dir_okay=True,
    )
) -> None:
    """Generate all handbook outputs."""
    outputs = build(root.resolve())
    for output in outputs:
        typer.echo(output)


if __name__ == "__main__":
    app()
