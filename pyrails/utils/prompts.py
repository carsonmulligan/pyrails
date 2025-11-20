"""Interactive prompt utilities."""
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


def select_option(question: str, options: list[tuple[str, str]], default: int = 0) -> str:
    """
    Display options and get user selection.

    Args:
        question: Question to ask
        options: List of (value, description) tuples
        default: Default option index

    Returns:
        Selected option value
    """
    console.print(f"\n[bold cyan]{question}[/bold cyan]")

    table = Table(show_header=False, box=None, padding=(0, 2))

    for i, (value, description) in enumerate(options, 1):
        marker = "[green]→[/green]" if i - 1 == default else " "
        table.add_row(f"{marker} {i}.", f"[yellow]{value}[/yellow]", description)

    console.print(table)

    while True:
        choice = Prompt.ask(
            "Select an option",
            default=str(default + 1),
            show_default=True
        )

        try:
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index][0]
            console.print(f"[red]Please enter a number between 1 and {len(options)}[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")


def confirm(question: str, default: bool = True) -> bool:
    """Ask yes/no confirmation."""
    return Confirm.ask(question, default=default)


def prompt_text(question: str, default: str = "") -> str:
    """Prompt for text input."""
    return Prompt.ask(question, default=default if default else None)
