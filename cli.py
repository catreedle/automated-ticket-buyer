import json
import questionary
from main import main

with open("events.json", "r") as file:
    data = json.load(file)



events = [item["name"] for item in data["modifications"][0]["value"]]


event_name = questionary.select(
    "Which event you want to buy the tickets for?",
    choices=events,
).ask()

main(event_name)

