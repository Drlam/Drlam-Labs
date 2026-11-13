import json
import math
from typing import Callable, cast

from CanBeShipped import CanBeShipped
from DigitalProduct import DigitalProduct
from Inventory import Inventory
from Order import Order
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier

INVENTORY_FILE: str = "inventory.json"

# Product type identifiers
PHYSICAL_PRODUCT_TYPE: str = "physical"
DIGITAL_PRODUCT_TYPE: str = "digital"


# Convert input data to a finite float.
def _as_float(value: object, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError(f"Invalid numeric value for {field_name}.")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"Invalid numeric value for {field_name}.") from error
    if not math.isfinite(result):
        raise ValueError(f"{field_name} must be a finite number.")
    return result


# Convert input data to an integer without truncating decimals.
def _as_int(value: object, field_name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"Invalid integer value for {field_name}.")
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not value.is_integer():
            raise ValueError(f"{field_name} must be a whole number.")
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError as error:
            raise ValueError(f"Invalid integer value for {field_name}.") from error
    raise ValueError(f"Invalid integer value for {field_name}.")


# Create or reuse a Supplier, ensuring one object per Supplier ID.
def _supplier_from_json(supplier_data: object, supplier_registry: dict[int, Supplier]) -> Supplier:
    if not isinstance(supplier_data, dict):
        raise ValueError("Invalid supplier information.")

    data = cast(dict[str, object], supplier_data)
    supplier_id = _as_int(data.get("Supplier ID"), "Supplier ID")
    name = data.get("Name")
    contact_email = data.get("Contact Email")
    if not isinstance(name, str) or not isinstance(contact_email, str):
        raise ValueError("Supplier name and contact email must be strings.")

    existing = supplier_registry.get(supplier_id)
    if existing is not None:
        if existing.get_name() != name or existing.get_contact_email() != contact_email:
            raise ValueError(f"Conflicting details for Supplier ID {supplier_id}.")
        return existing

    supplier = Supplier(supplier_id, name, contact_email)
    supplier_registry[supplier_id] = supplier
    return supplier


# Reconstruct a Product and its Supplier association from JSON.
def product_from_json(product_id: str, info: dict[str, object], supplier_registry: dict[int, Supplier]) -> Product:
    product_type = info.get("Type")
    name = info.get("Name")
    if not isinstance(product_type, str) or not isinstance(name, str):
        raise ValueError("Product type and name must be strings.")

    price = _as_float(info.get("Price"), "Price")
    stock = _as_int(info.get("Stock"), "Stock")
    if price < 0 or stock < 0:
        raise ValueError("Price and stock cannot be negative.")

    # Older files may not contain Supplier information. Keep those products
    # loadable by associating them with one clearly labelled placeholder.
    if "Supplier" in info:
        supplier = _supplier_from_json(info["Supplier"], supplier_registry)
    else:
        supplier = supplier_registry.get(0)
        if supplier is None:
            supplier = Supplier(0, "Unassigned Supplier", "Not provided")
            supplier_registry[0] = supplier

    if product_type == PHYSICAL_PRODUCT_TYPE:
        weight = _as_float(info.get("Weight"), "Weight")
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        return PhysicalProduct(product_id, name, price, stock, weight, supplier)

    if product_type == DIGITAL_PRODUCT_TYPE:
        download_size = _as_float(info.get("Download Size"), "Download Size")
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        return DigitalProduct(product_id, name, price, stock, download_size, supplier)

    raise ValueError(f"Unknown product type: {product_type}")


# Convert a Product and its Supplier to JSON-compatible data.
def product_to_json(product: Product) -> dict[str, object]:
    common_data: dict[str, object] = {
        "Name": product.get_name(),
        "Price": product.get_price(),
        "Stock": product.get_stock(),
        "Supplier": {
            "Supplier ID": product.supplier.get_supplier_id(),
            "Name": product.supplier.get_name(),
            "Contact Email": product.supplier.get_contact_email(),
        },
    }

    # Subclass checks are used only to serialize subclass-specific fields.
    # Normal Inventory operations still work through the Product abstraction.
    if isinstance(product, PhysicalProduct):
        return {
            "Type": PHYSICAL_PRODUCT_TYPE,
            **common_data,
            "Weight": product.get_weight(),
        }
    if isinstance(product, DigitalProduct):
        return {
            "Type": DIGITAL_PRODUCT_TYPE,
            **common_data,
            "Download Size": product.get_download_size(),
        }
    raise ValueError(f"Unsupported Product type: {product.get_product_id()}")


# Load Products and their Supplier objects from a JSON file.
def load_inventory(filename: str = INVENTORY_FILE) -> Inventory:
    inventory = Inventory()
    supplier_registry: dict[int, Supplier] = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_data: object = json.load(file)
        if not isinstance(raw_data, dict):
            raise ValueError("The inventory file must contain a JSON object.")

        data = cast(dict[str, object], raw_data)
        skipped_ids: list[str] = []
        legacy_ids: list[str] = []

        for product_id, raw_info in data.items():
            try:
                if not isinstance(product_id, str) or not isinstance(raw_info, dict):
                    raise ValueError("Invalid product record.")
                info = cast(dict[str, object], raw_info)
                product = product_from_json(product_id, info, supplier_registry)
                if not inventory.add_product(product):
                    skipped_ids.append(product_id)
                    continue
                if "Supplier" not in info:
                    legacy_ids.append(product_id)
            except (KeyError, TypeError, ValueError, OverflowError):
                skipped_ids.append(str(product_id))

        print(f"{filename} found.")
        if legacy_ids:
            print(
                "Supplier information was missing from older record(s); "
                "an 'Unassigned Supplier' was assigned to: "
                f"{', '.join(legacy_ids)}."
            )
        if skipped_ids:
            print(f"Skipped invalid or duplicate product(s): {', '.join(skipped_ids)}")
        if not skipped_ids:
            print("Inventory loaded successfully.")
        print()
        return inventory

    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty inventory.\n")
    except (json.JSONDecodeError, OSError, UnicodeDecodeError, ValueError) as error:
        print(f"Error reading {filename}: {error}. Starting with an empty inventory.\n")
    return inventory


# Save Products and associated Supplier details.
def save_inventory(inventory: Inventory, filename: str = INVENTORY_FILE) -> bool:
    try:
        data_to_save: dict[str, dict[str, object]] = {}
        for product in inventory.get_all_products():
            data_to_save[product.get_product_id()] = product_to_json(product)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4)
        return True
    except (OSError, TypeError, ValueError) as error:
        print(f"Error saving {filename}: {error}")
        return False


# Reuse a matching Supplier ID or create a new Supplier object.
def _find_or_create_supplier(inventory: Inventory, supplier_id: int, name: str, contact_email: str) -> Supplier | None:
    for product in inventory.get_all_products():
        existing = product.supplier
        if existing.get_supplier_id() == supplier_id:
            if existing.get_name() == name and existing.get_contact_email() == contact_email:
                return existing
            print("That Supplier ID already exists with different details.")
            return None
    return Supplier(supplier_id, name, contact_email)


# Display a Product and its associated Supplier details.
def display_product_with_supplier(product: Product) -> None:
    product.display_information()
    print(f"Supplier ID: {product.supplier.get_supplier_id()}")
    print(f"Supplier Name: {product.supplier.get_name()}")
    print(f"Supplier Email: {product.supplier.get_contact_email()}")


# Display all Products, including their Supplier details.
def display_inventory(inventory: Inventory) -> None:
    products = inventory.get_all_products()
    if not products:
        print("No inventory data available.")
        return

    print("\nCurrent Inventory")
    print("=" * 60)
    for product in products:
        display_product_with_supplier(product)
        print("-" * 60)


# Prompt the user to create a Product with an associated Supplier.
def prompt_add_product(inventory: Inventory) -> None:
    print("\nAdd Product")
    product_id = input("Enter Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Enter Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = _as_float(input("Enter Price: ").strip(), "Price")
        stock = _as_int(input("Enter Stock Quantity: ").strip(), "Stock Quantity")
        supplier_id = _as_int(input("Enter Supplier ID: ").strip(), "Supplier ID")
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    if price < 0 or stock < 0 or supplier_id <= 0:
        print("Price and stock cannot be negative, and Supplier ID must be positive.")
        return

    supplier_name = input("Enter Supplier Name: ").strip()
    contact_email = input("Enter Supplier Email: ").strip()
    if not supplier_name or not contact_email:
        print("Supplier name and email cannot be empty.")
        return

    supplier = _find_or_create_supplier(inventory, supplier_id, supplier_name, contact_email)
    if supplier is None:
        return

    product_type = input("Product Type (P = Physical, D = Digital): ").strip().upper()
    try:
        if product_type in ("P", "PHYSICAL"):
            extra_value = _as_float(input("Enter Weight (kg): ").strip(), "Weight")
            if extra_value < 0:
                print("Weight cannot be negative.")
                return
            product: Product = PhysicalProduct(
                product_id, name, price, stock, extra_value, supplier
            )
        elif product_type in ("D", "DIGITAL"):
            extra_value = _as_float(
                input("Enter Download Size (MB): ").strip(), "Download Size"
            )
            if extra_value < 0:
                print("Download size cannot be negative.")
                return
            product = DigitalProduct(
                product_id, name, price, stock, extra_value, supplier
            )
        else:
            print("Invalid product type. Please enter P or D.")
            return
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    if not inventory.add_product(product):
        print("Product ID already exists. Product was not added.")
        return

    print("Product added successfully.")
    display_product_with_supplier(product)
    print(f"Fulfilment Information: {product.get_fulfilment_info()}")


# Prompt the user to update an existing Product's stock.
def prompt_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print(f"Product: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    try:
        quantity = _as_int(input("Enter New Stock Quantity: ").strip(), "Stock Quantity")
    except ValueError as error:
        print(f"Invalid quantity: {error}")
        return

    if not product.update_stock(quantity):
        print("Stock quantity cannot be negative. Update cancelled.")
        return
    print("Stock updated successfully.")


# Search for a Product and display fulfilment and Supplier details.
def prompt_search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    display_product_with_supplier(product)
    print(f"Fulfilment Information: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Total Shipping Cost: ${product.calculate_shipping_cost():.2f}")


# Remove a Product from Inventory when no saved OrderLine depends on it.
def prompt_remove_product(inventory: Inventory, orders: dict[str, Order]) -> None:
    print("\nRemove Product")
    product_id = input("Enter Product ID to remove: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    # Orders refer to the Product by ID when saved. Prevent removal if an order
    # still uses it, so those OrderLines can be reconstructed when the app reloads.
    for order in orders.values():
        for order_line in order.get_order_lines():
            if order_line.product.get_product_id() == product_id:
                print("Cannot remove this product because it is used in an existing order.")
                print("Remove the corresponding order line first, then try again.")
                return

    if inventory.remove_product(product_id):
        print(f"Product {product_id} removed from Inventory successfully.")
        print("The Product object itself is not destroyed.")
    else:
        print("Product could not be removed.")


# Run the Inventory submenu; option 7 saves and returns to Main Menu.
def inventory_management_menu(inventory: Inventory, orders: dict[str, Order], save_callback: Callable[[], bool]) -> None:
    while True:
        print("\n========== INVENTORY MANAGEMENT ==========")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Remove Product")
        print("6. Save Inventory")
        print("7. Back to Main Menu")

        option = input("Select an option (1-7): ").strip()
        if option == "1":
            display_inventory(inventory)
        elif option == "2":
            prompt_add_product(inventory)
        elif option == "3":
            prompt_update_stock(inventory)
        elif option == "4":
            prompt_search_product(inventory)
        elif option == "5":
            prompt_remove_product(inventory, orders)
        elif option == "6":
            if save_inventory(inventory):
                print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "7":
            print("\nSaving application data before returning to Main Menu...")
            save_callback()
            return
        else:
            print("Invalid option. Please enter a number between 1 and 7.")
