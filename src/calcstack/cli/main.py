"""The ``calcstack`` command-line entry point.

Usage::

    calcstack calc "2 + 3 * 4"      # -> 14
    calcstack history show          # table of past calculations
    calcstack history clear         # wipe the history file

Output is rendered with Rich; errors from bad expressions become a red panel
and a non-zero exit code rather than a traceback.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from calcstack.engine.errors import CalculatorError
from calcstack.history import History, default_history
from calcstack.parser import evaluate

app = typer.Typer(
    help="calcstack — a deliberately over-engineered calculator.",
    no_args_is_help=True,
    add_completion=False,
)
history_app = typer.Typer(help="Inspect or clear calculation history.", no_args_is_help=True)
app.add_typer(history_app, name="history")

console = Console()


@app.command(context_settings={"ignore_unknown_options": True})
def calc(
    expression: str = typer.Argument(..., help="Expression to evaluate, e.g. '2 + 3 * 4'."),
    save: bool = typer.Option(True, help="Record this calculation in history."),
) -> None:
    """Evaluate an arithmetic EXPRESSION and print the result.

    ``ignore_unknown_options`` lets expressions that start with a minus sign
    (e.g. ``calcstack calc "-2 ^ 2"``) be read as the argument rather than as a
    command-line option.
    """
    try:
        result = evaluate(expression)
    except CalculatorError as exc:
        console.print(f"[bold red]Error:[/] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(f"[bold]{expression}[/] = [bold cyan]{result}[/]")
    if save:
        default_history().add(expression, str(result))


@history_app.command("show")
def history_show() -> None:
    """Show past calculations as a table."""
    entries = _history().all()
    if not entries:
        console.print("[dim]No history yet.[/]")
        return

    table = Table(title="Calculation history")
    table.add_column("#", justify="right", style="dim")
    table.add_column("When (UTC)")
    table.add_column("Expression")
    table.add_column("Result", justify="right", style="cyan")
    for index, entry in enumerate(entries, start=1):
        table.add_row(
            str(index),
            entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            entry.expression,
            entry.result,
        )
    console.print(table)


@history_app.command("clear")
def history_clear() -> None:
    """Delete all recorded calculations."""
    _history().clear()
    console.print("[green]History cleared.[/]")


def _history() -> History:
    return default_history()


def main() -> None:
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
