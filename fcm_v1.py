import json
import google.auth.transport.requests
from google.oauth2 import service_account
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_CREDENTIALS_FILE = os.getenv("FIREBASE_CREDENTIALS_FILE")
PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        FIREBASE_CREDENTIALS_FILE, scopes=SCOPES
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token


def send_fcm_v1(token, title, body):
    access_token = get_access_token()
    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }

    message = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body,
            },
            "data": {  # Optional custom data for Flutter navigation
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "screen": "news_detail",
            },
        }
    }

    response = requests.post(url, headers=headers, json=message)
    return response.json()
