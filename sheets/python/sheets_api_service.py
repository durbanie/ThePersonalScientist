import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Need write-access scope for google sheets.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
LOCAL_PATH = '%s/Work/ThePersonalScientist/sheets' % (os.path.expanduser('~'))

def get_creds(creds_path, scopes):
    '''Get's credentials for accessing sheets through the API.'''
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time. 
    token_pickle = '%s/token.pickle' % (creds_path)
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_json = '%s/credentials.json' % (creds_path)
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open(token_pickle, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def build_sheets_api():
    creds_path = '%s/creds/' % (LOCAL_PATH)
    creds = get_creds(creds_path, SCOPES)
    return build('sheets', 'v4', credentials=creds)

def create_spreadsheet(sheets_api, title):
    '''Creates a new spreadsheet with the title provided.'''
    spreadsheet = {
        'properties': {
            'title': title
        }
    }
    return sheets_api.spreadsheets().create(
        body=spreadsheet, fields='spreadsheetId').execute()
