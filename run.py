import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# In the course Love_sandwiches file is writen as love_sandwiches (lowercase letter). Keep that in mind.
SHEET = GSPREAD_CLIENT.open('Love_sandwiches') 

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)