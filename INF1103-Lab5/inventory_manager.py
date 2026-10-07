import json

INVENTORY_FILE = "inventory.json"

# Loading the inventory from a JSON file
def load_inventory(filename=INVENTORY_FILE):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            print(f"{filename} found.")
            print("Inventory loaded successfully.\n")
            return data
    except FileNotFoundError:
        print(f"{filename} not found. Starting with empty inventory.\n")
        return {}
    except (json.JSONDecodeError, AttributeError):
        print(f"Error reading {filename}. Starting fresh with empty inventory.\n")
        return {}

# Saving the inventory to a JSON file
def save_inventory(inventory, filename=INVENTORY_FILE):
    try:
        with open(filename, "w") as file:
            json.dump(inventory, file, indent=4)
        return True
    except Exception as error:
        print(f"Error saving inventory: {error}")
        return False

# Displaying all products in the inventory
def display_all(inventory):
    if not inventory:
        print("No inventory data available.")
        return

    print("Current Inventory:")
    for product_id, product_details in inventory.items():
        product_name = product_details.get("Name", "N/A")
        price = product_details.get("Price", 0.00)
        stock_quantity = product_details.get("Stock", 0)
        print(f"Product ID: {product_id}, Name: {product_name}, Price: ${price:.2f}, Stock: {stock_quantity}")

# Adding a new product to a new or existing inventory
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if product_id in inventory:
        print("Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()
    if not product_name:
        print("Product Name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock_quantity = int(input("Stock Quantity: "))
        
        if price < 0 or stock_quantity < 0:
            print("Price and Stock Quantity cannot be negative.")
            return
            
    except ValueError:
        print("Invalid input. Please enter valid numbers for price and quantity.")
        return

    inventory[product_id] = {
        "Name": product_name,
        "Price": price,
        "Stock": stock_quantity
    }
    print(f"Product added successfully: {product_name}")

# Updating the stock quantity of an existing product
def update_stock(inventory):
    print("\nUpdate Stock Quantity")
    product_id = input("Enter Product ID: ").strip()

    if product_id not in inventory:
        print("Product not found.")
        return

    product = inventory[product_id]
    print(f"\nProduct Found:")
    print(f"Name: {product['Name']}")
    print(f"Current Stock: {product['Stock']}\n")

    try:
        new_stock = int(input("New Stock Quantity: "))
        if new_stock < 0:
            print("Stock quantity cannot be negative. Update cancelled.")
            return
            
        product['Stock'] = new_stock
        print("\nStock updated successfully!")
    except ValueError:
        print("Invalid quantity. Stock update cancelled.")

# Searching a product by its ID and displaying its details if found
def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    if product_id in inventory:
        product = inventory[product_id]
        print(f"\nProduct Found:")
        print(f"Product ID: {product_id}")
        print(f"Name: {product['Name']}")
        print(f"Price: ${product['Price']:.2f}")
        print(f"Stock: {product['Stock']}\n")
    else:
        print("Product not found.")

# Menu options for the inventory management system
def menu_options(option, inventory):
    if option == '1':
        display_all(inventory)
    elif option == '2':
        add_product(inventory)
    elif option == '3':
        update_stock(inventory)
    elif option == '4':
        search_product(inventory)
    elif option == '5':
        print("\nSaving inventory...")
        if save_inventory(inventory):
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
    elif option == '6':
        print("\nSaving inventory before exit...")
        if save_inventory(inventory):
            print("Inventory saved successfully.")
        print("\nThank you for using Inventory Management System.")
        print("Program terminated.")
        return False
    else:
        print("Invalid option. Please enter a number between 1 and 6.")
    return True

# Main function to run the inventory management system
def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = load_inventory()

    running = True
    while running:
        print("\nMENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit\n")

        option = input("Enter option: ").strip()
        running = menu_options(option, inventory)

if __name__ == "__main__":
    main()




