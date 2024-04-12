import gspread


class SheetsWriter:
    
    def __init__(self, sheets_url) -> None:
        self.url = sheets_url
        self.spreadsheet_id = ""
        self.sheet_name = ""

    def write_to_sheets(self, data: dict):
        pass

    def confirm_write(self):
        pass