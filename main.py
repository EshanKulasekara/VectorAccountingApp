import json
import getpass
import os
from rich.console import Console
import inquirer

console = Console()

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

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
                users.append(new_user)
                save_data(users, USERS_FILE)
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

def main():    
    run_app = True
    while run_app == True:
        console.print("Accounting App By Vector INC.", style="blue bold")
        user = authenticate()
        if user:
            opt = menu()
            match opt:
                case 'e':
                    run_app = False
                case 'l':
                    user = None
        else:
            user = authenticate()

if __name__ == "__main__":
    main()