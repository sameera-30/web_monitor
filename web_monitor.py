import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Website URL to monitor
URL = "https://google.com"

# Alert email configuration - using environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Function to check website status
def check_website():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            print(f"Website {URL} is up. Status code: {response.status_code}")
        else:
            print(f"Warning: Website {URL} returned status code {response.status_code}")
            send_alert_email(f"Website {URL} returned status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error: Website {URL} is down. Error: {e}")
        send_alert_email(f"Website {URL} is down. Error: {e}")

# Function to send an alert email
def send_alert_email(message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = f"Alert: Issue with {URL}"
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print("Alert email sent.")
    except Exception as e:
        print(f"Failed to send alert email: {e}")

# Run the check once (not a loop since GitHub Actions controls the schedule)
if __name__ == "__main__":
    check_website()
