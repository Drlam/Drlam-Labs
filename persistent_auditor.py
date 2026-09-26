def load_inventory(filename="inventory.txt"):
    orders = []
    total = 0
    try:
        with open(filename, "r") as f:
            print("Current Orders:\n")
            for line in f:
                line = line.strip()
                if line:
                    print(line)
                    parts = line.split(",")
                    if len(parts) == 3:
                        order_id = int(parts[0].strip())
                        product_name = parts[1].strip()
                        inv_quantity = int(parts[2].strip())
                        orders.append((order_id, product_name, inv_quantity))
                        total += inv_quantity
            print()
    except FileNotFoundError:
        print("No prior inventory file found. Starting fresh.\n")
    return total, orders


def save_inventory(orders, filename="inventory.txt"):
    """Saves updated orders list back to inventory.txt."""
    try:
        with open(filename, "w") as f:
            for order_id, product_name, inv_quantity in orders:
                f.write(f"{order_id}, {product_name}, {inv_quantity}\n")
        print(f"Order successfully saved to {filename}")
    except Exception as error:
        print(f"Error saving to file: {error}")

def get_valid_input():
    product_name = input("Enter Product Name: ")
    if product_name.lower() == 'quit':
        return 'Quit', None
    
    stock_quantity = input("Enter stock quantity (or type quit to exit the auditor):")
    if stock_quantity.lower() == 'quit':
        return 'Quit', None
    elif stock_quantity.lstrip('-').isdigit() == False:
        print("Error!")
        return None, None
    elif int(stock_quantity) < 0:
        print("Rejected negative numbers")
        return None, None
    else:
        return product_name, int(stock_quantity)

def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print('Total Units Processed:', total_units)
    print('Number of Failed/Rejected Entries:', failed_attempts)

#Start of main code
total_inventory, orders = load_inventory("inventory.txt")
failed_entries = 0
product_id = orders[-1][0] + 1 if orders else 1001

while True:
    product_name, inv_quantity = get_valid_input()
    
    if product_name == 'Quit':
        break
    elif inv_quantity is None:
        failed_entries += 1
    else:
        if total_inventory + inv_quantity > 500:
            print('Alert! Inventory exceeded 500 units')
            failed_entries += 1
            break
        else:
            total_inventory = process_delivery(total_inventory, inv_quantity)
            orders.append((product_id, product_name, inv_quantity))
            
            tax = calculate_tax(inv_quantity)
            print("\nNew Order Added:")
            print(f"{product_id}, {product_name}, {inv_quantity}\n")
            
            product_id += 1

generate_report(total_inventory, failed_entries)
save_inventory(orders, "inventory.txt")