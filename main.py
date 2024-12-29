import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finanace_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    

    
    # A @classmethod is a method that is bound to the class rather than the instance of the class. It can access and modify the class state but cannot directly modify instance-specific data.
    # A @classmethod is a method that is bound to the class and not the instance of the class. It receives the class itself as the first argument, conventionally named cls.

    # to initialze the csv file
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    # add a new entry
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # comvert all the date insaide the date column to a date object  to filter by transaction
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # apply mask
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("no transcations in the given date")
        else:
            print(f'transaction frm {start_date.strftime(CSV.FORMAT)} - {end_date.strftime(CSV.FORMAT)}')
            print(filtered_df.to_string(index=False, formatters={"date":lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"] ["amount"].sum()
            print("/nSummary:")
            print(f"Total income: ${total_income:.2f}")
            print(f"Total expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        return filtered_df
        
# write a function that will call these functions in the order we want to collect our data
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter todays date", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()



# to use comnad line to interact instead of writing it here
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transaction and a summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3)")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date: ")
            end_date = get_date("Enter the end date: ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot graph? (y/n)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Existing...")
            break
        else:
            print("invalid choice: enter 1,2,3")

# Ensures that the main function is only executed when the script is run directly (e.g., python script.py).
# If the script is imported as a module in another Python file, the main function won't run automatically.
if __name__=="__main__":
    main()



# this was asssummig the add() was not in place
# CSV.initialize_csv()
# CSV.add_entry("20-27-24",102.00,"Income","salary")

CSV.get_transactions("01-01-2023", "30-07-2024")
# add()

    
    # A @staticmethod is a method that does not receive an implicit first argument like self or cls. It behaves like a regular function but belongs to the class's namespace.







# Instance Method:
# A method that belongs to the object of a class.
    
# Class Method:
# A method that belongs to the class, not the object.


# Static Method:
# A method that doesn’t belong to the object or the class.