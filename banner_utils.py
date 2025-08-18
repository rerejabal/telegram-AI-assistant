from art import text2art
from rich.console import Console
from rich.panel import Panel
import os
from dotenv import load_dotenv

console = Console()

# load env biar bisa ambil BOT_USERNAME_ENV, MODEL LIST, dsb
load_dotenv()

BOT_USERNAME_ENV = (os.getenv("BOT_USERNAME") or "").lower().strip()

# Model list (optional bisa dipass dari luar juga)
DEFAULT_MODELS = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "gemma2-9b-it",
    "qwen/qwen3-32b",
]

def show_banner(models=None):
    """Tampilkan banner utama bot."""
    models = models or DEFAULT_MODELS
    banner = text2art("        MYSTIC   BOT   SCRIPT", font="small")
    console.print(
        Panel(
            banner,
            title="🤖 Telegram AI Assistant",
            subtitle="by rerejabal",
            style="bold magenta",
        )
    )
    console.print("\n\n" + f"[cyan]Bot username:[/cyan] @{BOT_USERNAME_ENV or 'unknown'}")
    console.print(f"[yellow]Active models order:[/yellow]\n- " + "\n- ".join(models) + "\n")
