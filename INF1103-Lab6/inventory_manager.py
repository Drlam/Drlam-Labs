import json
from Product import Product
from Inventory import Inventory

INVENTORY_FILE = "inventory.json"

# Loading the inventory from a JSON file into Inventory object
def load_inventory(filename=INVENTORY_FILE):
    inventory = Inventory()
    try:
        with open(filename, "r") as file:
            data = json.load(file)
 
        for product_id, info in data.items():
            product = Product(
                product_id=product_id,
                name=info["Name"],
                price=float(info["Price"]),
                stock=int(info["Stock"])
            )
            inventory.add_product(product)
 
        print(f"{filename} found.")
        print("Inventory loaded successfully.\n")
        return inventory
 
    except FileNotFoundError:
        print(f"{filename} not found. Starting with empty inventory.\n")
        return Inventory()
    except (json.JSONDecodeError, AttributeError, KeyError, TypeError, ValueError):
        print(f"Error reading {filename}. Starting fresh with empty inventory.\n")
        return Inventory()
 
 
# Saving the Inventory object to a JSON file
def save_inventory(inventory, filename=INVENTORY_FILE):
    try:
        data_to_save = {}
        for product in inventory.get_all_products():
            data_to_save[product.get_product_id()] = {
                "Name": product.get_name(),
                "Price": product.get_price(),
                "Stock": product.get_stock(),
            }
 
        with open(filename, "w") as file:
            json.dump(data_to_save, file, indent=4)
        return True
    except Exception as error:
        print(f"Error saving inventory: {error}")
        return False
 
 
# Prompt user to add new product
def prompt_add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
 
    if not product_id:
        print("Product ID cannot be empty.")
        return
 
    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return
 
    name = input("Product Name: ").strip()
    if not name:
        print("Product Name cannot be empty.")
        return
 
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid input. Please enter valid numbers for price and quantity.")
        return
 
    if price < 0 or stock < 0:
        print("Price and Stock Quantity cannot be negative.")
        return
 
    inventory.add_product(Product(product_id, name, price, stock))
    print(f"Product added successfully: {name}")
 
 
# Prompt user to update inventory stock
def prompt_update_stock(inventory):
    print("\nUpdate Stock Quantity")
    product_id = input("Enter Product ID: ").strip()
 
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
 
    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")
 
    try:
        quantity = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid quantity. Stock update cancelled.")
        return
 
    if not product.update_stock(quantity):
        print("Stock quantity cannot be negative. Update cancelled.")
        return
 
    print("\nStock updated successfully!")
 
 
# Prompt user to search for a product using its ID
def prompt_search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
 
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
 
    print("\nProduct Found:")
    print(f"Product ID: {product.get_product_id()}")
    print(f"Name: {product.get_name()}")
    print(f"Price: ${product.get_price():.2f}")
    print(f"Stock: {product.get_stock()}\n")
 
 
# Menu options of Inventory Management System
def menu_options(option, inventory):
    if option == "1":
        inventory.display_all()
    elif option == "2":
        prompt_add_product(inventory)
    elif option == "3":
        prompt_update_stock(inventory)
    elif option == "4":
        prompt_search_product(inventory)
    elif option == "5":
        print("\nSaving inventory...")
        if save_inventory(inventory):
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
    elif option == "6":
        print("\nSaving inventory before exit...")
        if save_inventory(inventory):
            print("Inventory saved successfully.")
        print("\nThank you for using Inventory Management System.")
        print("Program terminated.")
        return False
    else:
        print("Invalid option. Please enter a number between 1 and 6.")
    return True
 
 
# Main code
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