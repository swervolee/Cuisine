#!/usr/bin/python3

import os.path
import base64
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_credentials():
    """Gets valid user credentials from a file."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    elif not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token_info = {
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "id_token": creds.id_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": creds.scopes
            }
            json.dump(token_info, token)
    return creds


def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = (
        f"From: {sender}\n"
        f"To: {to}\n"
        f"Subject: {subject}\n\n"
        f"{message_text}"
    )
    return {"raw": base64.urlsafe_b64encode(message.encode()).decode()}


def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = (
            service.users().messages().send(userId=user_id, body=message)
            .execute()
        )
        print("Message sent successfully.")
        return message
    except HttpError as error:
        print(f"An error occurred: {error}")


def main(**kwargs):
    # Get Gmail API credentials
    creds = get_credentials()
    # Authenticate with Gmail service
    service = build("gmail", "v1", credentials=creds)

    # Define email content
    sender = "cuisinemailbox@gmail.com"

    # Create email message
    message = create_message(sender,
                             kwargs["reciever"],
                             kwargs["subject"],
                             kwargs["message"])

    # Send email
    send_message(service, "me", message)


if __name__ == "__main__":
    main()
