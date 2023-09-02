import json
import getpass
import os
from rich.console import Console

console = Console()

run_app = True

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []

def askUsernameAndPassword():
    username = console.input("Username: ")
    password = getpass.getpass("Password: ")
    o = dict();
    if username and password:
        o['uname'] = username
        o['password'] = password
        return o
    else:
        console.print("Please Enter Username and Password", style="red")
        askUsernameAndPassword()

def authenticate():
    users = load_data(USERS_FILE)
    for _ in range(3):
        ans = askUsernameAndPassword()
        uname = ans.get('uname')
        password = ans.get('password')

        for user in users:
            if user["username"] == uname and user["password"] == password:
                console.print("Sign In Successfull", style="green")
                return user
            else:
                console.print("Incorrect Username and Password Try again", style="red")
    console.print("You have tried 3 time now", style="red bold")
    creAcc = console.input("Do You want to create an Account [Y/N]: ")
    if creAcc == 'Y' or creAcc == 'y':
        console.print("creating account", style="green")
    else:
        exitapp = console.input("Do You want to Exit [Y/N]:")
        if exitapp == 'Y' or exitapp == 'y':
            run_app = False
        else:
            authenticate()

def main():
    while run_app == True:
        console.print("Accounting App By Vector INC.", style="blue bold")
        authenticate()
        break

if __name__ == "__main__":
    main()