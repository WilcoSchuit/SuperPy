# Imports
import argparse
import csv
import datetime
import pandas as pd
from pandas import read_csv
import os
import os.path
from tabulate import tabulate
from rich import print

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.


# Function to generate parser:
def generate_parser():
    # Parsers:
    parser = argparse.ArgumentParser(
        description="Keep track of your inventory.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # advance time argument:
    parser.add_argument(
        "--advance-time", type=int, help="advance time by inserted amount of days"
    )

    # Buy Parser:
    buy_parser = subparsers.add_parser("buy", help="register purchased product")
    buy_parser.add_argument("--product-name", help="insert product name")
    buy_parser.add_argument("--price", type=float, help="insert buy price in euros")
    buy_parser.add_argument(
        "--expiration-date",
        type=datetime.date.fromisoformat,
        help="insert date as: YYYY-MM-DD",
    )

    # Sell Parser:
    sell_parser = subparsers.add_parser("sell", help="register sold product")
    sell_parser.add_argument("--product-name", help="insert product name")
    sell_parser.add_argument("--price", type=float, help="insert sell price in euros")

    # Report Parser:
    report = subparsers.add_parser("report", help="report transactions")
    report_subparsers = report.add_subparsers(dest="parser_report")
    inventory = report_subparsers.add_parser("inventory", help="show inventory")
    revenue = report_subparsers.add_parser("revenue", help="show revenue in euros")
    profit = report_subparsers.add_parser("profit", help="show profit in euros")
    inventory.add_argument("--now", action="store_true", help="show current inventory")
    inventory.add_argument("--yesterday", action="store_true", help="show yesterday's inventory")
    revenue.add_argument(
        "--yesterday", action="store_true", help="show yesterday's revenue in euros"
    )
    revenue.add_argument("--today", action="store_true", help="show today's revenue in euros")
    revenue.add_argument(
        "--date", help="show revenue from given date: insert date as: YYYY-MM"
    )
    profit.add_argument("--today", action="store_true", help="show today's profit/loss in euros")
    profit.add_argument("--yesterday", action="store_true", help="show yesterday's profit/loss in euros")

    return parser


def create_csv_file(filename, headers):
    """Create csv files if they don't exist
    
    Keyword Arguments:
    filename -- filename.csv
    headers -- [headers]"""

    if not os.path.exists(filename):
        with open(filename, "a") as file_handle:
            writer = csv.DictWriter(
                file_handle, delimiter=",", lineterminator="\n", fieldnames=headers
            )
            writer.writeheader()


def create_csv_files():
    """Create bought.csv and sold.csv files"""

    create_csv_file("bought.csv", ["id", "product_name", "buy_date", "buy_price", "expiration_date"])
    create_csv_file("sold.csv", ["bought_id", "sell_date", "sell_price"])


def create_date_txt():
    """Save date to .txt file"""

    if os.path.exists('date.txt') == False:
        date = str(datetime.datetime.today().strftime(DATE_FORMAT_STRING))
        file = open('date.txt', 'w')
        file.write(date)
        file.close()


def get_date():
    """Retrieve current date from date.txt"""

    with open('date.txt') as file:
        lines = file.readlines()
        current_date = datetime.datetime.strptime(lines[0], DATE_FORMAT_STRING).date()
        return current_date


def advance_time(days):
    """Advance time by inserted amount of days in command line 

    Keyword Argument:
    days -- amount of days to be advanced"""

    current_date = get_date()
    new_date = str(current_date + datetime.timedelta(days=days))
    file = open('date.txt', 'w')
    file.write(new_date)
    file.close()
    print(f"[bright_green]Time advanced by {days} days, current date is {new_date}[/bright_green]")


def get_last_id(csv_file):
    """Retrieve last id number within a csv file
    
    Keyword Argument:
    csv_file -- filename.csv 

    Output: last id number"""
    
    with open(csv_file, "r", newline="") as file_handle:
        lines = file_handle.readlines()
        last_line = lines[-1]
        last_id = last_line.split(",")[0]
        if last_id == "id":
            return 0
        return int(last_id)


def buy_product():
    """Write product data to bought.csv"""

    product_name = args.product_name
    buy_price = args.price
    expiration_date = args.expiration_date
    buy_date = get_date()
    with open("bought.csv", "a", newline="") as bought_file:
        writer = csv.writer(bought_file)
        row = [
            get_last_id("bought.csv") + 1,
            product_name,
            buy_date,
            buy_price,
            expiration_date,
        ]
        writer.writerow(row)

    print(f"[bright_green]Bought one {product_name}, added to bought.csv[/bright_green]")


def sell_product(inventory, product, price):
    """Write product data to sold.csv

    Keyword Arguments:
    inventory -- inventory generated by generate_inventory()
    product -- args.product_name
    price -- args.price in euros"""

    # We always sell exactly one item.
    if not product_is_available(inventory, product):
        print("[bright_red]Product not in stock or expired[/bright_red]")
        return
    print(f"[bright_green]Sold one {product}, added to sold.csv[/bright_green]")

    # Theoretically could produce None, but as we check it above that's
    # theoretical.
    product_id = find_product_id(inventory, product)
    sell_price = args.price
    sell_date = get_date()
    with open("sold.csv", "a", newline="") as sold_file:
        writer = csv.writer(sold_file)
        row = [
            product_id,
            sell_date,
            sell_price,
        ]
        writer.writerow(row)


def product_is_available(inventory, product):
    """Check if product is available 

    Keyword Arguments:
    inventory -- inventory generated by generate_inventory()
    product -- args.product_name"""

    for row in inventory:
        if product == row[1]:
            return True
    return False


def parse_date_string(date_string):
    """Parse given date string to YYYY-MM-DD
    
    Keyword Argument:
    date_string -- date string 
    
    Output: datetime date in format YYYY-MM-DD"""
    
    # input = "YYYY-MM-DD"
    return datetime.datetime.strptime(date_string, DATE_FORMAT_STRING)


def find_product_id(inventory, product):
    """Find product id in inventory

    Keyword Arguments:
    inventory -- inventory generated by generate_inventory()
    product -- args.product_name"""

    for row in inventory:
        if row[1] == product:
            return row[0]
    return None


def revenue(day):
    """Calculate revenue on given day

    Keyword Argument:
    day -- args.date, args.today, args.yesterday
    
    Output: revenue in euros"""

    sold_csv = read_csv(os.getcwd() + "\\sold.csv")
    revenue = sold_csv.loc[sold_csv["sell_date"] == day, "sell_price"].sum()
    return revenue


def costs(day):
    """Calculate costs on given day

    Keyword Argument:
    day -- args.date, args.today, args.yesterday
    
    Output: costs in euros"""

    bought_csv = read_csv(os.getcwd() + "\\bought.csv")
    costs = bought_csv.loc[bought_csv["buy_date"] == day, "buy_price"].sum()
    return costs


def read_csv_file(filename):
    """Read csv file

    Keyword Argument:
    filename -- filename.csv"""

    content = []
    with open(filename, "r") as file_handle:
        lines = file_handle.readlines()
        lines = lines[1:]
        for line in lines:
            content.append(line.strip().split(","))
    return content


def remove_from_inventory(inventory, product_id):
    """Remove a product from inventory list

    Keyword Arguments:
    inventory -- inventory generated by generate_inventory()
    product_id -- product id

    Output: new inventory"""

    new_inventory = []
    for row in inventory:
        if product_id == row[0]:
            continue
        new_inventory.append(row)
    return new_inventory


def generate_inventory(bought_csv, sold_csv, day):
    """Generate inventory list from bought.csv and sold csv

    Keyword Arguments:
    bought_csv -- bought.csv
    sold_csv -- sold.csv
    day -- args.date, args.today, args.yesterday

    Output: inventory"""

    bought = read_csv_file(bought_csv)
    sold = read_csv_file(sold_csv)
    inventory = []
    for row in bought:
        product_id = row[0]
        product_name = row[1]
        buy_date = row[2]
        expiration_date = row[4]
        # We don't need expired items in our inventory
        # We throw them away every day.
        if parse_date_string(buy_date) <= parse_date_string(day):
            if parse_date_string(day) < parse_date_string(expiration_date):
                inventory.append([product_id, product_name, expiration_date])

    for row in sold:
        product_id = row[0]
        sell_date = row[1]
        if parse_date_string(sell_date) <= parse_date_string(day):
            inventory = remove_from_inventory(inventory, product_id)

    return inventory


def update_inventory(inventory, day):
    """Update inventory

    Keyword arguments: 
    inventory -- inventory generated by generate_inventory()
    day -- args.date, args.today, args.yesterday

    Output: updated inventory"""

    inventory = generate_inventory("bought.csv", "sold.csv", day)
    temp_inventory = []
    temp_updated_inventory = []
    updated_inventory = []
    for product in inventory:
        product_name = product[1].capitalize()
        expiration_date = product[2]
        temp_inventory.append([product_name, expiration_date])
    for product in temp_inventory:
        product_name = product[0].capitalize()
        expiration_date = product[1]
        count = temp_inventory.count(product)
        temp_updated_inventory.append([product_name, count, expiration_date])
    for product in temp_updated_inventory:
        if product not in updated_inventory:
            updated_inventory.append(product)
    return updated_inventory


def generate_inventory_table(inventory):
    """Generate inventory table

    Keyword Argument:
    inventory -- inventory generated by generate_inventory()

    Output: inventory table"""
    return tabulate(inventory, headers=['Product Name', 'Count', 'Expiration Date'], tablefmt='grid')


def create_inventory_csv(inventory, day):
    """Create csv file from inventory list

    Keyword Arguments:
    inventory -- inventory generated by update_inventory()
    """
    header = ['Product Name', 'Count', 'Expiration Date']
    with open(f'inventory_{day}.csv', "w", newline='') as inventory_file:
            writer = csv.writer(inventory_file)
            writer.writerow(header)
            writer.writerows(inventory)


def export_inventory_to_excel(inventory, day):
    """Export inventory list to Excel file

    Keyword Arguments:
    inventory -- inventory generated by update_inventory()
    day -- args.date, args.today, args.yesterday"""

    df = pd.DataFrame(inventory)
    writer = pd.ExcelWriter(f'inventory_{day}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    header = ['Product Name', 'Count', 'Expiration Date']
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})
    for col_num, value in enumerate(header):
        worksheet.write(0, col_num + 1, value, header_format)
    writer.save()


if __name__ == "__main__":
    # String format for date variables:
    DATE_FORMAT_STRING = "%Y-%m-%d"

    # Create files:
    create_csv_files()
    create_date_txt()

    # Generate parser:
    parser = generate_parser()
    args = parser.parse_args()

    # Store current date in variable today:
    today = str(get_date())

    # Generate inventory:
    inventory = generate_inventory("bought.csv", "sold.csv", today)

    if args.advance_time:
        advance_time(args.advance_time)
        today = str(get_date())

    if args.command == "buy":
        buy_product()

    if args.command == "sell":
        sell_product(inventory, args.product_name, args.price)

    if args.command == "report":
        yesterday = str(get_date() - datetime.timedelta(days=1))
        if args.parser_report == 'inventory':
            if args.now:
                inventory = generate_inventory("bought.csv", "sold.csv", today)
                new_inventory = update_inventory(inventory, today)
                inventory_table = generate_inventory_table(new_inventory)
                print(inventory_table)
                export_inventory_to_excel(new_inventory, today)
                create_inventory_csv(new_inventory, today)
                print(f"[bright_green]Current inventory exported to inventory_{today}.xlsx and inventory_{today}.csv[/bright_green]")
            if args.yesterday:
                inventory = generate_inventory("bought.csv", "sold.csv", yesterday)
                new_inventory = update_inventory(inventory, yesterday)
                inventory_table = generate_inventory_table(new_inventory)
                print(inventory_table)
                export_inventory_to_excel(new_inventory, yesterday)
                create_inventory_csv(new_inventory, yesterday)
                print(f"[bright_green]Yesterday's inventory exported to inventory_{yesterday}.xlsx and inventory_{yesterday}.csv[/bright_green]")
        if args.parser_report == "revenue":
            if args.today:
                revenue = revenue(today)
                print(f"[bright_blue]Today's revenue so far: {revenue}[/bright_blue]")
            elif args.yesterday:
                revenue = revenue(yesterday)
                print(f"[bright_blue]Yesterday's revenue: {revenue}[/bright_blue]")
            elif args.date:
                sold_csv_path = os.getcwd() + "\\sold.csv"
                sold_csv = read_csv(os.getcwd() + "\\sold.csv")
                date = args.date
                set_date = datetime.datetime.strptime(date, "%Y-%m")
                sold_csv.sell_date = pd.to_datetime(sold_csv.sell_date).dt.to_period("m")  # convert dates in sell_date column to YYYY-MM only
                year = datetime.datetime.strftime(set_date, "%Y")
                month_name = set_date.strftime("%B")
                revenue = sold_csv.loc[sold_csv["sell_date"] == date, "sell_price"].sum()
                print(f"[bright_blue]Revenue from {month_name} {year}: {revenue}[bright_blue]")

        if args.parser_report == "profit":
            if args.today:
                costs = costs(today)
                revenue = revenue(today)
                profit = revenue - costs
                if profit >= 0:
                    print(f"[bright_green]Today's profit: {profit}[/bright_green]")
                else:
                    print(f"[bright_red]Today's loss: {profit}[/bright_red]")
            if args.yesterday:
                costs = costs(yesterday)
                revenue = revenue(yesterday)
                profit = revenue - costs
                if profit >= 0:
                    print(f"[bright_green]Yesterday's profit: {profit}[/bright_green]")
                else:
                    print(f"[bright_red]Yesterday's loss: {profit}[/bright_red]")
