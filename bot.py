# Pulse Daily Summary Bot
# Fetches weather (wttr.in) & quotes (zenquotes.io)
import requests
from datetime import date

def get_weather(city="Kochi"):
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather unavailable ({e})"

def get_quote():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}" — {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"

def build_summary():
    today = date.today().strftime("%A, %d %B %Y")
    weather = get_weather()
    quote = get_quote()
    
    summary = f"""
PULSE Daily Summary
{today}
-------------------
WEATHER
{weather}

TODAY'S QUOTE
{quote}
"""
    return summary

def run():
    summary = build_summary()
    print(summary)
    
    # Save a physical text file artifact
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("Pulse run successful!")

if __name__ == "__main__":
    run()
