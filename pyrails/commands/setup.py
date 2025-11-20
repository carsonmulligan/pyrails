"""Setup commands for configuring API keys and services."""
import sys
from pathlib import Path

from rich.console import Console

from pyrails.utils import prompt_text

console = Console()


def run_setup(*args):
    """Run setup wizard."""
    if not args:
        console.print("\n[bold green]🔧 PyRails Setup Wizard[/bold green]\n")
        console.print("Available setup commands:")
        console.print("  [cyan]pyrails setup stripe[/cyan]  - Configure Stripe API keys")
        console.print("  [cyan]pyrails setup openai[/cyan]  - Configure OpenAI API keys")
        return

    service = args[0]

    if service == "stripe":
        setup_stripe()
    elif service == "openai":
        setup_openai()
    else:
        console.print(f"[red]Unknown service:[/red] {service}")


def setup_stripe():
    """Setup Stripe API keys."""
    console.print("\n[bold green]💳 Stripe Setup[/bold green]\n")

    env_file = Path.cwd() / ".env"

    if not env_file.exists():
        console.print("[red]❌ .env file not found[/red]")
        sys.exit(1)

    console.print("Enter your Stripe API keys:")
    console.print("[dim](Find them at: https://dashboard.stripe.com/apikeys)[/dim]\n")

    secret_key = prompt_text("Stripe Secret Key (sk_...)")
    publishable_key = prompt_text("Stripe Publishable Key (pk_...)")

    # Read existing .env
    env_content = env_file.read_text()

    # Add or update Stripe keys
    if "STRIPE_SECRET_KEY" in env_content:
        # Update existing
        import re
        env_content = re.sub(
            r'STRIPE_SECRET_KEY=.*',
            f'STRIPE_SECRET_KEY="{secret_key}"',
            env_content
        )
        env_content = re.sub(
            r'STRIPE_PUBLISHABLE_KEY=.*',
            f'STRIPE_PUBLISHABLE_KEY="{publishable_key}"',
            env_content
        )
    else:
        # Add new
        env_content += f'\n# Stripe\nSTRIPE_SECRET_KEY="{secret_key}"\n'
        env_content += f'STRIPE_PUBLISHABLE_KEY="{publishable_key}"\n'

    env_file.write_text(env_content)

    console.print("\n[green]✅ Stripe configuration saved to .env[/green]")


def setup_openai():
    """Setup OpenAI API keys."""
    console.print("\n[bold green]🤖 OpenAI Setup[/bold green]\n")

    env_file = Path.cwd() / ".env"

    if not env_file.exists():
        console.print("[red]❌ .env file not found[/red]")
        sys.exit(1)

    console.print("Enter your OpenAI API key:")
    console.print("[dim](Find it at: https://platform.openai.com/api-keys)[/dim]\n")

    api_key = prompt_text("OpenAI API Key (sk-...)")

    # Read existing .env
    env_content = env_file.read_text()

    # Add or update OpenAI key
    if "OPENAI_API_KEY" in env_content:
        # Update existing
        import re
        env_content = re.sub(
            r'OPENAI_API_KEY=.*',
            f'OPENAI_API_KEY="{api_key}"',
            env_content
        )
    else:
        # Add new
        env_content += f'\n# OpenAI\nOPENAI_API_KEY="{api_key}"\n'

    env_file.write_text(env_content)

    console.print("\n[green]✅ OpenAI configuration saved to .env[/green]")
