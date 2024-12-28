from typing import Any, Dict, List

FOLDER_ID = "1jhIJ6e79mvy7HMhg-dSQVgk-EEHH4dJG"
PAGE_NAME = "Página1"


def find_spreadsheet_file_by_name(drive_service, spreadsheet_name:str) -> Dict[str, Any]:
    spreadsheet_file: Dict[str, Any] = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and name='{spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet'",
    fields='files(id, name)'
    ).execute()
    return spreadsheet_file
    

def get_spreadsheet_rows(sheets_service, spreadsheet_id: str, PAGE_NAME: str) -> list:
    result: dict = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=PAGE_NAME
    ).execute()
    rows = result.get('values', [])
    return [row[:12] for row in rows[1:]]


def handle(drive_service, sheets_service, spreadsheet_name:str) -> List[List[str]]:
    spreadsheet_file = find_spreadsheet_file_by_name(drive_service, spreadsheet_name)
    if len(spreadsheet_file['files']) == 0: 
        raise Exception(f"Spreadsheet '{spreadsheet_name}' not found.")
    return get_spreadsheet_rows(sheets_service, spreadsheet_file['files'][0]['id'], PAGE_NAME)

