# notification.py

import os
import requests

def send_notification_via_logic_app(escalation_message: str):
    """
    Sends a notification by triggering an Azure Logic App.
    """
    logic_app_url = os.getenv("LOGIC_APP_TRIGGER_URL")
    if not logic_app_url:
        return "Logic App trigger URL not configured."

    payload = {
        "subject": "Customer Service Query Escalation",
        "body": escalation_message,
        "to": os.getenv("SUPPORT_EMAIL")
    }

    response = requests.post(logic_app_url, json=payload)
    if response.status_code in [200, 202]:
        return "Notification sent successfully."
    else:
        return f"Failed to send notification. Status code: {response.status_code}"