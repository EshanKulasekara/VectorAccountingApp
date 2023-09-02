import json
import getpass
import os
from rich.console import Console

console = Console()

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []

def authenticate():
    users = load_data(USERS_FILE)
    uname = input("Username:")
    password = getpass.getpass("Password:")

    for user in users:
        if user["username"] == uname and user["password"] == password:
            console.print("Sign In Successfull", style="green")
            return user
        else:
            console.print("Incorrect Username and Password Try again", style="red")
            authenticate()


def main():
    while True:
        console.print("Accounting App By Vector INC.", style="blue bold")
        authenticate()
        break

if __name__ == "__main__":
    main()