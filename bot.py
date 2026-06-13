# Pulse Daily Summary Bot
# Fetches weather (wttr.in) & quotes (zenquotes.io)
# Pulse Daily Summary Bot
# Fetches weather, quotes, and emails the summary
# Pulse Daily Summary Bot
# Fetches weather, quotes, and emails the summary
import os
import smtplib
from datetime import date
from email.message import EmailMessage
import requests


def get_weather():
    # Looks for a secret variable named 'CITY' on GitHub; defaults to Thiruvananthapuram
    city = os.getenv("CITY", "Thiruvananthapuram")
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


def send_email(summary_text):
    """Fetches credentials from environment variables and emails the summary."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv(
        "SENDER_PASSWORD"
    )  # Must be a 16-digit Google App Password
    receiver_email = os.getenv("RECEIVER_EMAIL")

    # If any credential variable is missing, skip email sending and don't crash
    if not sender_email or not sender_password or not receiver_email:
        print(
            "⚠️ Email credentials missing from environment. Skipping email dispatch."
        )
        return

    today_str = date.today().strftime("%d %B %Y")

    # Set up the email format structure
    msg = EmailMessage()
    msg["Subject"] = f"📩 Pulse Daily Summary — {today_str}"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(summary_text)

    # Establish connection with Gmail's secure server and send
    try:
        print("Connecting to secure mail server...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("🚀 Email summary dispatched successfully!")
    except Exception as e:
        print(f"❌ Failed to send email alert: {e}")


def run():
    summary = build_summary()
    print(summary)

    # Save a physical text file artifact
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("Pulse run successful!")

    # Execute the email sender function
    send_email(summary)


if __name__ == "__main__":
    run()