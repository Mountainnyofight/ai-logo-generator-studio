"""CLI entrypoint. `logo-studio generate|plugins|serve`."""
from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

from .bootstrap import StudioHost

app = typer.Typer(help="AI Logo Generator Studio", no_args_is_help=True)
console = Console()

@app.command()
def generate(
    prompt: str = typer.Argument(..., help="logo prompt"),
    out: Path = typer.Option(Path("out"), "--out", "-o"),
    pipeline: str = typer.Option("default", "--pipeline"),
) -> None:
    host = StudioHost.from_config()
    result = asyncio.run(host.generate(prompt=prompt, out_dir=out, pipeline=pipeline))
    console.print(f"[green]wrote[/green] {result.primary}")

@app.command("plugins")
def plugins_cmd(action: str = typer.Argument("list")) -> None:
    host = StudioHost.from_config()
    if action == "list":
        for m in host.registry.manifests():
            console.print(f"{m.name:<20} v{m.version:<8} {','.join(m.capabilities)}")
    elif action == "reload":
        host.reload_plugins()
        console.print("[yellow]plugins reloaded[/yellow]")

if __name__ == "__main__":
    app()