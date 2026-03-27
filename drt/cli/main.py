"""drt CLI entry point."""

import typer
from rich.console import Console

from drt import __version__

app = typer.Typer(
    name="drt",
    help="Reverse ETL for the code-first data stack.",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"drt version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", callback=version_callback, is_eager=True, help="Show version."
    ),
) -> None:
    pass


@app.command()
def init() -> None:
    """Initialize a new drt project in the current directory."""
    console.print("[bold green]Initializing drt project...[/bold green]")
    # TODO: Phase 1 — scaffold drt_project.yml and syncs/
    console.print("[yellow]Coming soon in Phase 1[/yellow]")


@app.command()
def run(
    select: str = typer.Option(None, "--select", "-s", help="Run a specific sync by name."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing data."),
) -> None:
    """Run sync(s) defined in the project."""
    if dry_run:
        console.print("[bold]Dry-run mode[/bold] — no data will be written.")
    # TODO: Phase 1 — load config, run engine
    console.print("[yellow]Coming soon in Phase 1[/yellow]")


@app.command(name="list")
def list_syncs() -> None:
    """List all sync definitions in the project."""
    # TODO: Phase 1 — parse syncs/ and display
    console.print("[yellow]Coming soon in Phase 1[/yellow]")


@app.command()
def validate() -> None:
    """Validate sync definitions against the JSON Schema."""
    # TODO: Phase 1 — validate YAML configs
    console.print("[yellow]Coming soon in Phase 1[/yellow]")


@app.command()
def status() -> None:
    """Show the status of the most recent sync runs."""
    # TODO: Phase 2 — read from StateManager
    console.print("[yellow]Coming soon in Phase 2[/yellow]")
