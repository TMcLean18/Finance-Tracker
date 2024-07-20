import pandas as pd
import csv
from datetime import datetime
from dataEntry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_info.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    @classmethod
    def csv_initialise(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:#Create CSV if not found
            df = pd.DataFrame(columns=cls.COLUMNS)#Columns for CSV
            df.to_csv(cls.CSV_FILE, index=False)#Takes the dataframe and converts it to CSV

     #Use a CSV writer to write to the file
    @classmethod
    def entry_add(cls, date, amount, category, description):
            #Create a dictionary for each entry
            new_entry = {
                 "date": date,
                 "amount": amount,
                 "category": category,
                 "description": description,
            }
            #CSV writer to write to the csv file using the dictionary
            with open(cls.CSV_FILE,"a", newline="") as csvfile: #Opening the csv file in "a"-APPEND MODE (ADDING TO THE FILE)(context manager-will close file and deal with memory leaks)
                 writer=csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)#Create a CSV write to write to the csvfile using the dictionary
                 writer.writerow(new_entry) #using the writer we created we will write a new row using the dictionary in entry_add
                 print("Entry Added Succesfully")
    
    #Function to get transactios sorted by date range
    @classmethod
    def get_transactions(cls, start_date, end_date):
         df = pd.read_csv(cls.CSV_FILE) #read CSV File, can access columns with panda dataframe
         df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT) #CONVERT DATE TO DATE FORMAT
         start_date = datetime.strptime(start_date, CSV.FORMAT) #Convert string start date to date format
         end_date = datetime.strptime(end_date, CSV.FORMAT) #Convert string endate date to date format
         #Mask - something to apply in rows in a data frame to see if those rows should be selected or not
         mask = (df["date"]>=start_date ) & (df["date"]<=end_date) #checking if the date is greater than or equal to start date and less than end_date (&-bitwise and use when workign on panda and mask)
         filtered_df = df.loc[mask] #will return a filtered dataframe that only contains the dates in the mask

         if filtered_df.empty:
              print("No transactions found in the given date range")
         else:
              print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)} ")
              print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
              total_income = filtered_df[filtered_df["category"]=="Income"]["amount"].sum() #get all incomes in filterd df and add all values in the amount column
              total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
              print("\n Summary:")
              print(f"Total Income: R{total_income:2f}") 
              print(f"Total Expense: R{total_expense: 2f}")
              print(f"Net Saving R{(total_income-total_expense):2f}")
          
         return filtered_df

def add():
     print("Welcome To Tyrique's Finance Manager")  
     CSV.csv_initialise()
     date = get_date("Enter the date of the Transaction (dd-mm-yyyy) or Enter for Today's Date: ", allow_default=True)
     amount = get_amount()
     category=get_category()
     description=get_description()
     CSV.entry_add(date, amount, category, description)

#function to plot graph
def plot_transaction(df): #passes data frames
     df.set_index("date", inplace=True) #find rows and columns using the date
     #create two data frames for income and expense
     df_income = df[df["category"]=="Income"].resample("D").sum().reindex(df.index, fill_value=0) #take filtered data frame and have a row for each day and aggregate values on each day
     df_expense = df[df["category"]=="Expense"].resample("D").sum().reindex(df.index, fill_value=0)
     plt.figure(figsize=(10,5))
     plt.plot(df_income.index, df_income["amount"], label="Income", color="g")
     plt.plot(df_expense.index, df_expense["amount"], label="Expense", color="r")
     plt.xlabel("Date")
     plt.ylabel("Amount")
     plt.title("Income and Expenses Over Time")
     plt.legend()
     plt.grid(True)
     plt.show()


#function to create a menu
def main():
     while True:
          print("\n 1. Add a new Transaction")
          print("\n 2. View Transactions and summary within a date range")
          print("\n 3. Exit")
          choice = int(input("Enter your choice between 1-3: "))
          if choice==1:
               add()
          elif choice==2:
               start_date = get_date("Enter start date in the format (dd-mm-yyy): ")
               end_date = get_date("Input end date in the format (dd-mm-yyy): ")
               df=CSV.get_transactions(start_date, end_date)
               if input("Do you want to see a plot? (y/n)").lower() == "y":
                    plot_transaction(df)
          elif choice==3:
               print("Exiting...")
               break
          else: 
               print("Invalid choice! Enter a 1, 2 or 3")

if __name__ == "__main__": # If we run this file directly it will call the function directly but if we import it will not run because the name will not be main 
     main()
