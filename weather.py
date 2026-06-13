import os
import smtplib
from datetime import date
from email.message import EmailMessage
import requests


def check_weather_and_alert():
    # 1. Load configuration from secure environment variables
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("CITY", "Thiruvananthapuram")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = (
        os.getenv("SENDER_PASSWORD")  # Your 16-digit Gmail App Password
    )
    receiver_email = os.getenv("RECEIVER_EMAIL")

    # Guard clause: stop if API key or email configurations are missing
    if not api_key or not sender_email or not sender_password or not receiver_email:
        print("⚠️ Missing required environment configurations. Exiting.")
        return

    # 2. Fetch live data from OpenWeatherMap (Metric units for Celsius)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Failed to fetch weather data: {e}")
        return

    # Extract required metrics
    temp = data["main"]["temp"]
    weather_desc = data["weather"][0]["description"].lower()
    weather_main = data["weather"][0]["main"].lower()

    print(f"Current temperature in {city}: {temp}°C")
    print(f"Current conditions: {weather_desc}")

    # 3. Evaluate Threshold Conditions
    is_hot = temp > 35
    is_raining = (
        "rain" in weather_desc
        or "drizzle" in weather_desc
        or "thunderstorm" in weather_main
    )

    if is_hot or is_raining:
        print("🚨 Alert condition triggered! Assembling email alert...")

        reasons = []
        if is_hot:
            reasons.append(f"• High Temperature detected: {temp}°C")
        if is_raining:
            reasons.append(f"• Precipitation detected: {weather_desc.title()}")

        # Construct email layout
        msg = EmailMessage()
        msg["Subject"] = f"⚠️ WEATHER ALERT: {city}"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        content = f"""PULSE WEATHER ALERT SYSTEM
Location: {city}
Date: {date.today().strftime('%A, %d %B %Y')}

The following triggers have met your alert criteria:
{chr(10).join(reasons)}

Current Workspace Metrics:
- Actual Temperature: {temp}°C
- Sky Condition: {weather_desc.capitalize()}

Please prepare accordingly!
"""
        msg.set_content(content)

        # 4. Dispatch Email
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print("🚀 Alert email dispatched successfully!")
        except Exception as e:
            print(f"❌ Failed to send email alert: {e}")
    else:
        print("✅ Weather conditions within safe boundaries. No alert necessary.")


if __name__ == "__main__":
    check_weather_and_alert()
