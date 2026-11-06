import json
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct

INVENTORY_FILE = "inventory.json"

# Product type identifiers
PHYSICAL_PRODUCT_TYPE = "physical"
DIGITAL_PRODUCT_TYPE = "digital"

# Converting JSON data to appropriate Product child classes
def product_from_json(product_id, info):
    product_type = info["Type"]
    name = info["Name"]
    price = float(info["Price"])
    stock = int(info["Stock"])

    if product_type == PHYSICAL_PRODUCT_TYPE:
        return PhysicalProduct(product_id, name, price, stock, float(info["Weight"]))
    elif product_type == DIGITAL_PRODUCT_TYPE:
        return DigitalProduct(product_id, name, price, stock, float(info["Download Size"]))
    else:
        raise ValueError(f"Unknown product type: {product_type}")

# Converting Product child classes to JSON-compatible dictionaries
def product_to_json(product):
    if isinstance(product, PhysicalProduct):
        return {
            "Type": PHYSICAL_PRODUCT_TYPE,
            "Name": product.get_name(),
            "Price": product.get_price(),
            "Stock": product.get_stock(),
            "Weight": product.get_weight()
        }
    elif isinstance(product, DigitalProduct):
        return {
            "Type": DIGITAL_PRODUCT_TYPE,
            "Name": product.get_name(),
            "Price": product.get_price(),
            "Stock": product.get_stock(),
            "Download Size": product.get_download_size()
        }
    else:
        raise ValueError(f"Unknown product type for {product.get_product_id()}")

# Loading the inventory from a JSON file into Inventory object
def load_inventory(filename=INVENTORY_FILE):
    inventory = Inventory()
    try:
        with open(filename, "r") as file:
            data = json.load(file)

        skipped_ids = []
        for product_id, info in data.items():
            try:
                product = product_from_json(product_id, info)
            except (KeyError, TypeError, ValueError):
                skipped_ids.append(product_id)
                continue
            inventory.add_product(product)

        print(f"{filename} found.")
        if skipped_ids:
            print(f"Inventory loaded. Skipped invalid product(s): {', '.join(skipped_ids)}\n")
        else:
            print("Inventory loaded successfully.\n")
        return inventory

    except FileNotFoundError:
        print(f"{filename} not found. Starting with empty inventory.\n")
        return Inventory()
    except (json.JSONDecodeError, AttributeError):
        print(f"Error reading {filename}. Starting fresh with empty inventory.\n")
        return Inventory()


# Saving the Inventory object to a JSON file
def save_inventory(inventory, filename=INVENTORY_FILE):
    try:
        data_to_save = {}
        for product in inventory.get_all_products():
            data_to_save[product.get_product_id()] = product_to_json(product)

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

    print("\nProduct Type")
    print("1. Physical Product")
    print("2. Digital Product")
    select_type = input("Choose product type (1 or 2): ").strip()
    if select_type not in ("1", "2"):
        print("Invalid product type. Cancelled Adding Product.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product Name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if select_type == "1":
            extra_input = float(input("Weight (kg): "))
        else:
            extra_input = float(input("Download Size (MB): "))
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    if price < 0 or stock < 0 or extra_input < 0:
        print("Price, Stock Quantity and Weight/Download Size cannot be negative.")
        return

    if select_type == "1":
        product = PhysicalProduct(product_id, name, price, stock, extra_input)
    else:
        product = DigitalProduct(product_id, name, price, stock, extra_input)

    inventory.add_product(product)
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
    product.display_information()
    print(product.get_fulfilment_info())
    if isinstance(product, PhysicalProduct):
        print(f"Total Shipping Cost: ${product.calculate_shipping_cost():.2f}")


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