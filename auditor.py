total_inventory = 0
failed_entries = 0
stock_quantity = input("Enter Stock Quantity:")

while stock_quantity.lower() != 'quit':
    if stock_quantity.lstrip('-').isdigit() == False:
        print('Error!')
        failed_entries += 1
    elif int(stock_quantity) < 0:
        print('Rejected negative numbers')
        failed_entries += 1
    elif total_inventory + int(stock_quantity) > 500:
        print('Alert! Inventory exceeded 500 units')
        failed_entries += 1
        break
    else:
        total_inventory += int(stock_quantity)
        print(total_inventory)

    stock_quantity = input("Enter Stock Quantity:")

print('Total Units Processed:', total_inventory)
print('Number of Failed/Rejected Entries:', failed_entries)