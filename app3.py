#!/usr/bin/env python3
"""
Simple hotel booking web app -> sends booking data to Telegram.
"""

from flask import Flask, render_template_string, request, redirect, url_for
import requests

app = Flask(__name__)

# TODO: replace with your bot token and chat id
TELEGRAM_BOT_TOKEN = "8766543374:AAHVC3rEEOGwhhIvXHEkVmZtGBQpZ1W0KJY"
TELEGRAM_CHAT_ID = "5312938858"


HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Hotel Booking</title>
</head>
<body>
    <h2>Hotel Booking Form</h2>
    <form method="post" action="/book">
        Name: <input type="text" name="name" required><br><br>
        Phone: <input type="text" name="phone" required><br><br>
        Check-in: <input type="date" name="checkin" required><br><br>
        Check-out: <input type="date" name="checkout" required><br><br>
        Guests: <input type="number" name="guests" required><br><br>
        <button type="submit">Book Now</button>
    </form>
</body>
</html>
"""


def send_to_telegram(message: str) -> None:
    """Send message to Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Telegram error: {response.text}")


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_FORM)


@app.route("/book", methods=["POST"])
def book():
    try:
        data = {
            "name": request.form["name"],
            "phone": request.form["phone"],
            "checkin": request.form["checkin"],
            "checkout": request.form["checkout"],
            "guests": request.form["guests"],
        }

        message = (
            f"📌 New Booking\n"
            f"Name: {data['name']}\n"
            f"Phone: {data['phone']}\n"
            f"Check-in: {data['checkin']}\n"
            f"Check-out: {data['checkout']}\n"
            f"Guests: {data['guests']}"
        )

        send_to_telegram(message)
        return "<h3>Booking submitted successfully!</h3>"

    except Exception as exc:
        return f"<h3>Error: {exc}</h3>"


if __name__ == "__main__":
    app.run(debug=True)