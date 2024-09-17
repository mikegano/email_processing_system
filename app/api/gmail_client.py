import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailClient:
    def __init__(self, config):
        self.creds = None
        self.authenticate()

    def authenticate(self):
        """Authenticates the Gmail API client using OAuth 2.0."""
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('gmail', 'v1', credentials=self.creds)

    def fetch_emails(self, query=None):
        """Fetches emails based on the provided query."""
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        email_list = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            email_list.append(msg['snippet'])

        return email_list
