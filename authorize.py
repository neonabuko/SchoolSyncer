from typing import Union
import os
from google.oauth2.credentials import Credentials as OAuth2Credentials
from google.auth.credentials import Credentials as ExternalCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_creds() -> Union[OAuth2Credentials, ExternalCredentials, None]:
    creds = None
    if os.path.exists("token.json"):
        creds = OAuth2Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
                
    return creds