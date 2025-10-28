from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table
import time
import requests

console = Console()

TOOL_NAME = "WHITE DEVIL-21 AADHAAR OSINT"
DEVELOPER = "WHITEDEVIL-21"

API_URL = "https://ck-aadhaar-osint.vercel.app/fetch"
API_KEY = "paidchx"

def animate_header():
    console.clear()
    tool_title = Text(TOOL_NAME, style="bold cyan on black", justify="center")
    dev_name = Text(DEVELOPER, style="italic green", justify="center")
    console.print()
    console.print(Align.center(tool_title))
    console.print(Align.center(dev_name))
    console.print()

def prompt_aadhaar():
    while True:
        console.print("[bold yellow]Enter Aadhaar Number:[/bold yellow] ", end="")
        aadhaar = input().strip()
        if len(aadhaar) == 12 and aadhaar.isdigit():
            return aadhaar
        else:
            console.print("[red]Invalid Aadhaar number! Please enter a 12-digit numeric Aadhaar.[/red]")

def loading_animation(stage: str, seconds: float = 3):
    spinner = Spinner("dots", text=stage, style="cyan")
    with Live(spinner, refresh_per_second=12, transient=True):
        time.sleep(seconds)

def fetch_data(aadhaar):
    try:
        loading_animation("Collecting database access...")
        loading_animation("Fetching details from server...")
        response = requests.get(f"{API_URL}?key={API_KEY}&aadhaar={aadhaar}", timeout=15)
        if response.status_code == 200:
            loading_animation("Processing data...")
            return response.json()
        else:
            console.print(f"[red]Error: Server responded with status code {response.status_code}[/red]")
            return None
    except requests.RequestException as e:
        console.print(f"[red]Network error: {e}[/red]")
        return None

def display_data(data):
    console.clear()
    animate_header()
    console.print("[bold magenta]Fetched Aadhaar Data:[/bold magenta]\n")

    basic_details = Table(show_header=False, box=None, expand=True)
    basic_details.add_row("State:", f"[bold green]{data.get('homeStateName', 'N/A')}[/bold green]")
    basic_details.add_row("District:", f"[bold green]{data.get('homeDistName', 'N/A')}[/bold green]")
    basic_details.add_row("FPS ID:", f"[bold green]{data.get('fpsId', 'N/A')}[/bold green]")
    basic_details.add_row("Allowed ONORC:", f"[bold green]{data.get('allowed_onorc', 'N/A')}[/bold green]")
    basic_details.add_row("Duplicate UID Status:", f"[bold green]{data.get('dup_uid_status', 'N/A')}[/bold green]")
    console.print(Panel(basic_details, title="Basic Info", border_style="bright_blue"))

    members = data.get("memberDetailsList", [])
    if members:
        member_table = Table(title="Family Members Details", show_lines=True, header_style="bold cyan", border_style="bright_yellow")
        member_table.add_column("ID", style="dim", width=12)
        member_table.add_column("Name", style="bold magenta")
        member_table.add_column("Relationship Code", justify="center")
        member_table.add_column("Relationship", style="bold green")
        member_table.add_column("UID Linked", justify="center")
        for member in members:
            member_table.add_row(
                member.get("memberId", "N/A"),
                member.get("memberName", "N/A"),
                str(member.get("relationship_code", "N/A")),
                member.get("releationship_name", "N/A"),
                member.get("uid", "N/A")
            )
        console.print(member_table)
    else:
        console.print("[yellow]No member details found.[/yellow]")

def main():
    console.clear()  # ← this clears the screen before everything starts
    animate_header()
    aadhaar_number = prompt_aadhaar()
    data = fetch_data(aadhaar_number)
    if data:
        display_data(data)
    else:
        console.print("\n[red bold]Failed to retrieve data. Please try again later.[/red bold]")

if __name__ == "__main__":
    main()
