from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False): #prompt allows user to input before date is entered, default date will choose today's date when pressing enter
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT) #Convert date to string and get date in the specified format 
    #Validate date and convert it to the specified format
    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT) #if the date is valid it will return the valid date in the specified format
    except ValueError:
        print("Invalid Date Format. Please Enter date in the dd-mm-yyyy format!!")
        return get_date(prompt, allow_default) #recursive case will call function until date is valid

def get_amount():
    try:
        amount = float(input("Enter The amount: "))
        if amount <=0:
            raise ValueError("Amount must be a number greater than zero")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input("Enter the Category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid Category. Please Enter 'I' for Income or 'E' for Expense.")
    return get_category()

def get_description():
    return input("Enter a description (Optional): ")
