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

def get_sales_data():
    """
    Get sales figures input from the user
    """

    while True:
        print("Please enter sales data from the last market>")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50,60")

        data_str = input("Enter your data here: ")
        print(f"The data probided is {data_str}")

        # Create a variable that stores the input split into single numbers divided by commas
        sales_data = data_str.split(",")
        print(sales_data) 

        # If validate-data returns true break the loop, otherwise the loop repeats itself
        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    Returns True when input data are correct.
    """
    try:
        # Converts input data (which are strings) into integers
        [int(value) for value in values]

        # Validate the number of input elements
        if len(values) != 6:
            raise ValueError( 
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False
    return True

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.

    Open connection to the worksheet.
    Get the last row of data in the sheet (stock[-1]). Index -1 
    is the first index counting from the last
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

    # Zip method allows us to interate dwo iterable structures at a time.
    # Here we iterate our stocklist and subtract the number of sold items 
    # Then we add remaining walue to the worksheet
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    print(surplus_data)



def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("Welcome to Love Sandwiches Data Automation")
main()