from rich.console import Console
from rich.table import Table

data = [
    {"date": "2003-08-31", "type": "expense", "amount": 1000},
    {"date": "2003-08-31", "type": "expense", "amount": 1000},
    {"date": "2003-08-31", "type": "income", "amount": 1000},
    {"date": "2003-08-31", "type": "income", "amount": 1000},
    {"date": "2003-08-31", "type": "income", "amount": 1000},
    {"date": "2003-08-31", "type": "expense", "amount": 1000},
]

table = Table(title="Star Wars Movies")

table.add_column("Date", justify="right", no_wrap=True)
table.add_column("Type")
table.add_column("Amount", justify="right", style="green")

for tra in data:
    if tra.get("type") == "income":
        table.add_row(tra.get("date"), tra.get("type"), str(tra.get("amount")), style="green")
    else:
        table.add_row(tra.get("date"), tra.get("type"), str(tra.get("amount")), style="red")

#table.add_row("Dec 20, 2019", "Expense", "$952,110,690", style="red" )
#table.add_row("May 25, 2018", "Income", "$393,151,347")
#table.add_row("Dec 15, 2017", "Expense", "$1,332,539,889")
#table.add_row("Dec 16, 2016", "Income", "$1,332,439,889")

console = Console()
console.print(table)