import questionary
from purchase_bot import run_purchase_bot
from socket_client import events
from rich.console import Console
from rich.table import Table
from datetime import datetime, timezone

event_names = [item["name"] for item in events]

def show_event_info():
    console = Console()
    table = Table(title="Events Information")

    table.add_column("Name", justify="left", style="cyan")
    table.add_column("Date", justify="left", style="magenta")
    table.add_column("Location", justify="left", style="magenta")
    table.add_column("Price", justify="left", style="green")
    table.add_column("Total tickets", justify="right", style="green")
    
    for event in events:
        timestamp_seconds = int(event["eventDate"]) / 1000  # Convert milliseconds to seconds
        date_object = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
        formatted_date = date_object.strftime("%b %d, %Y")  # Format as "Jan 01, 2030"
        
        formatted_price = f"${float(event.get('price', 0)):,.2f}"
        
        table.add_row(event["name"], formatted_date, event["location"], formatted_price, str(int(event["totalTickets"])))
    
    console.print(table)
    
def process_buy_tickets():
    event_name = questionary.select(
        "Which event you want to buy the tickets for?",
        choices=event_names + ["x Exit Program x"],
    ).ask()
    
    if event_name == "x Exit Program x":
        print("Exiting program...")
    else:
        run_purchase_bot(event_name)

def check_tickets_availability():
    return 0

def main():
    action = questionary.select(
    "What do you need help with?",
    choices=["Event Info", "Buy Tickets", "Check Availability"]
    ).ask()
    
    if action == "Event Info":
        show_event_info()
    elif action == "Buy Tickets":
        process_buy_tickets()
    else:
        print("This command is under construction.")

main()