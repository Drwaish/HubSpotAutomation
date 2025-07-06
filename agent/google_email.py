import os.path
import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailClient:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
    ]

    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticate the api using credentials.josn
        """
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_file, "w") as token:
                token.write(self.creds.to_json())
        self.service = build("gmail", "v1", credentials=self.creds)

    def send_email(self, to, subject, message_text):
        """
        Send email to the user.

        Parameters
        ----------
        to
            Recpient of email.

        subject
            Email subject for recepient.

        message_text
            Text of the body
        
        Return
        ------
        str
            Confirmation message

        """
        try:
            message = MIMEText(message_text)
            message['to'] = to
            message['subject'] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            body = {'raw': raw}
            sent_message = self.service.users().messages().send(userId="me", body=body).execute()
            print(f"Message sent to {to} with id: {sent_message['id']}")
            return sent_message
        except HttpError as error:
            print(f"An error occurred while sending the email: {error}")
            return None

# Example usage
if __name__ == "__main__":
    client = GmailClient()
    client.send_email(
        to="mirzazainalinasir@gmail.com",
        subject="Test Subject ",
        message_text="This is the email body sent  Gmail client."
    )
