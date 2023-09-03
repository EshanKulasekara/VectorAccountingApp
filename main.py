import json
import getpass
import os
from rich.console import Console
from rich.table import Table
import inquirer
from datetime import datetime

console = Console()

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
ACCOUNTS_FILE = os.path.join(DATA_DIR, 'accounts.json')

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []

def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def askUsernameAndPassword():
    o = dict();
    while True:
        username = console.input("Username: ")
        password = getpass.getpass("Password: ")
        if username and password:
            o['uname'] = username
            o['password'] = password
            print(o)
            return o
        else:
            console.print("Please Enter Username and Password", style="red")
            print(o)

def authenticate():
    users = load_data(USERS_FILE)
    accounts = load_data(ACCOUNTS_FILE)
    active_user = False
    for _ in range(3):
        ans = askUsernameAndPassword()
        print("in authenticate", ans)
        uname = ans.get('uname')
        password = ans.get('password')

        for user in users:
            if user["username"] == uname and user["password"] == password:
                console.print("Sign In Successfull", style="green")
                active_user = True
                return user
        if active_user == False:
            console.print("Incorrect Username and Password Try again", style="red")
    console.print("You have tried 3 time now", style="red bold")
    creAcc = console.input("Do You want to create an Account [Y/N]: ")
    if creAcc == 'Y' or creAcc == 'y':
        while True:
            nuname = console.input("New Username:")
            npassword = console.input("New Password:")
            if uname and npassword:
                new_user = {"username": nuname, "password": npassword}
                new_account = {"owner": uname, "amount": 0}
                accounts.append(new_account)
                users.append(new_user)
                save_data(users, USERS_FILE)
                save_data(accounts, ACCOUNTS_FILE)
                console.print("New User Created", style="green")
                return new_user
            else:
                console.print("Please Enter new Username and Password")
    else:
        exitapp = console.input("Do You want to Exit [Y/N]:")
        if exitapp == 'Y' or exitapp == 'y':
            run_app = False
        else:
            authenticate()

def menu():
    questions = [
        inquirer.List('menu_option',
                              message="Hello There, What do you want to do?",
                              choices=['Add Expenses', 'Add Income', 'Show Balance', 'Budget', 'History', 'Logout', 'Exit'],
                              ),
    ]
    answers = inquirer.prompt(questions)
    print(answers)
    match answers.get('menu_option'):
        case "Exit":
            console.print("Exiting App", style="red")
            return 'e'
        case "Logout":
            console.print("Logging user Out", style="red")
            return 'l'
        case "Add Income":
            return 'i'
        case "Add Expenses":
            return 'ex'
        case "History":
            return 'his'
        case "Show Balance":
            return 'b'

def Add_Income(user):
    accounts = load_data(ACCOUNTS_FILE)
    amount_added = False
    while user:
        amount = console.input("What is your amount? ")
        if amount:
            try:
                amount = int(amount)
                break 
            except ValueError:
                console.print("Please enter a number", style="red") 
        elif not amount:
            console.print("Please Enter an amount", style="red")
    for account in accounts:
        if account["owner"] == user.get("username"):
            console.print("Added amount:" ,amount)
            account["amount"] += int(amount)
            console.print("full acount amount:", account["amount"])
            income_log = {"amount": amount, "type": "Income", "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S")} #
            account["history"].append(income_log)                                                                        # Logging history
            print(income_log)
            save_data(accounts, ACCOUNTS_FILE)
            amount_added = True
            break
    if amount_added == False:
        new_account = {"owner": user.get("username"), "amount": int(amount), "history": []}
        accounts.append(new_account)
        console.print("Added amount:" ,amount)
        console.print("full acount amount:", amount)
        income_log = {"amount": amount, "type": "Expense", "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S")} #
        account["history"].append(income_log)                                                                        # Logging history
        print(income_log)
        save_data(accounts, ACCOUNTS_FILE)
        amount_added = True

def Add_Expense(user):
    accounts = load_data(ACCOUNTS_FILE)
    amount_removed = False
    while user:
        amount = console.input("What is your amount? ")
        if amount:
            try:
                amount = int(amount)
                break 
            except ValueError:
                console.print("Please enter a number", style="red") 
        elif not amount:
            console.print("Please Enter an amount", style="red")
    for account in accounts:
        if account["owner"] == user.get("username"):
            console.print("Removed amount:" ,amount)                #
            account["amount"] -= int(amount)                        #  Amount updating
            console.print("full acount amount:", account["amount"]) #
            expense_log = {"amount": amount, "type": "Expense", "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S")} #
            account["history"].append(expense_log)                                                                        # Logging history
            print(expense_log)                                                                                            #
            save_data(accounts, ACCOUNTS_FILE)
            amount_removed = True
            break
    if amount_removed == False:
        new_account = {"owner": user.get("username"), "amount": int(amount), "history": []}
        accounts.append(new_account)
        console.print("Added amount:" ,amount)
        console.print("full acount amount:", amount)
        expense_log = {"amount": amount, "type": "Expense", "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S")} #
        account["history"].append(expense_log)                                                                        # Logging history
        print(expense_log)
        save_data(accounts, ACCOUNTS_FILE)
        amount_added = True

def History(user, func, data = None):
    accounts = load_data(ACCOUNTS_FILE)
    table = Table(title="Transaction history")
    table.add_column("Date", justify="right", no_wrap=True)
    table.add_column("Type")
    table.add_column("Amount", justify="right",)
    if func == 'r':
        for account in accounts:
            if account["owner"] == user.get("username"):
                his = account["history"]
                for record in his:
                    if record.get("type") == "Income":
                        table.add_row(record.get("datetime"), record.get("type"), str(record.get("amount")), style="green")
                    else:
                        table.add_row(record.get("datetime"), record.get("type"), str(record.get("amount")), style="red")
                console.print(table)
    elif func == 'w':
        for account in accounts:
            if account["owner"] == user.get("username"):
                account["history"].append(data)
                save_data(account, ACCOUNTS_FILE)


def main():    
    run_app = True
    console.print("Accounting App By Vector INC.", style="blue bold")
    accounts = load_data(ACCOUNTS_FILE)
    while run_app == True:
        user = authenticate()
        while user:
            opt = menu()
            match opt:
                case 'e':
                    user = None
                    run_app = False
                case 'l':
                    user = None
                case 'i':
                    Add_Income(user)
                case 'ex':
                    Add_Expense(user)
                case 'his':
                    History(user, 'r', data=None)
                case 'b':
                    for account in accounts:
                        if account["owner"] == user.get("username"):
                            console.print(account["amount"])

        #else:
        #    user = authenticate()

if __name__ == "__main__":
    main()