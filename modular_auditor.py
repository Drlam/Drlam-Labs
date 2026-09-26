def get_valid_input():
    stock_quantity = input("Enter stock quantity (or type quit to exit the auditor):")
    if stock_quantity.lower() == 'quit':
          return 'Quit'
    elif stock_quantity.lstrip('-').isdigit() == False:
            print("Error!")
            return None
    elif int(stock_quantity) < 0:
            print("Rejected negative numbers")
            return None
    else:
            return int(stock_quantity)

def process_delivery(current_total, new_value):
      return current_total + new_value

def calculate_tax(amount):
      return amount * 0.10

def generate_report(total_units, failed_attempts):
      print('Total Units Processed:', total_units)
      print('Number of Failed/Rejected Entries:', failed_attempts)

# Start of my main code
total_inventory = 0
failed_entries = 0

while True:
    stock = get_valid_input()
    if stock == 'Quit':
        break
    elif stock is None:
        failed_entries += 1
    else:
        if total_inventory + stock > 500:
            print('Alert! Inventory exceeded 500 units')
            failed_entries += 1
        else:
            total_inventory = process_delivery(total_inventory, stock)
            tax = calculate_tax(stock)
            print(f"Processed {stock} units. Tax for this delivery: {tax:.2f}")
            print(f"Total inventory: {total_inventory}")

generate_report(total_inventory, failed_entries)