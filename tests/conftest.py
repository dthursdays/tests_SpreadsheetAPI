import pytest
from ss import SpreadsheetAPI


CREDS_FILE = 'creds.json'
SPREADSHEET_ID = '1uRuwSNBwgPXXeemF2GVtYIm_zJu4qUexnozqLa-2PkU'
APIS = ['https://www.googleapis.com/auth/spreadsheets']

test_spreadsheet = SpreadsheetAPI(
    SPREADSHEET_ID, 'Лист1', 0, CREDS_FILE, APIS
)


@pytest.fixture()
def clear_data():
    """Очистка данных с листа 2 после теста."""

    yield

    test_spreadsheet.service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range='Лист2'
    ).execute()
