import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Constants
URL = "https://www.google.com"  # The website you want to monitor
SLACK_TOKEN = os.getenv("SLACK_TOKEN")  # Use GitHub Actions secrets for the Slack bot token
SLACK_CHANNEL = "#alerts"  # Replace with your Slack channel name

# Initialize Slack client
slack_client = WebClient(token=SLACK_TOKEN)

# Function to send alert to Slack
def send_slack_alert(message):
    try:
        slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        print("Slack alert sent successfully.")
    except SlackApiError as e:
        print(f"Error sending alert to Slack: {e.response['error']}")

# Function to check website performance
def check_performance():
    # Setup Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode for non-GUI testing
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Running website monitoring checks...")
        start_time = time.time()
        driver.get(URL)  # Access the URL

        # Check if the page loaded successfully by locating an element
        try:
            element = driver.find_element(By.TAG_NAME, "h1")  # Replace with a reliable element on the page
            load_time = time.time() - start_time
            print(f"Page loaded successfully in {load_time:.2f} seconds.")
            
            # Example alert if page load time exceeds threshold (e.g., 3 seconds)
            if load_time > 3:
                send_slack_alert(f"Warning: {URL} took {load_time:.2f} seconds to load.")
            else:
                print("Load time is within acceptable range.")
                
        except Exception as e:
            print("Page element not found. The site may be down.")
            send_slack_alert(f"Error: {URL} is not loading correctly - {str(e)}")

    except Exception as e:
        print(f"Error accessing the URL: {e}")
        send_slack_alert(f"Error accessing {URL}: {e}")

    finally:
        # Close the driver
        driver.quit()

# Run performance check
if __name__ == "__main__":
    check_performance()
