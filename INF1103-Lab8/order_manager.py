import json
from typing import Callable, cast

from Inventory import Inventory
from Order import Order

ORDERS_FILE: str = "orders.json"


# Convert input to a positive whole-number order quantity.
def _as_positive_quantity(value: object) -> int:
    if isinstance(value, bool):
        raise ValueError("Quantity must be a whole number.")
    if isinstance(value, int):
        quantity = value
    elif isinstance(value, str):
        try:
            quantity = int(value.strip())
        except ValueError as error:
            raise ValueError("Quantity must be a whole number.") from error
    elif isinstance(value, float) and value.is_integer():
        quantity = int(value)
    else:
        raise ValueError("Quantity must be a whole number.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    return quantity


# Load Orders and reconnect each OrderLine to the Product in Inventory.
def load_orders(inventory: Inventory, filename: str = ORDERS_FILE) -> dict[str, Order]:
    orders: dict[str, Order] = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_data: object = json.load(file)
        if not isinstance(raw_data, dict):
            raise ValueError("The orders file must contain a JSON object.")

        data = cast(dict[str, object], raw_data)
        skipped_orders: list[str] = []
        skipped_lines: int = 0

        for order_id, raw_order in data.items():
            try:
                if not isinstance(order_id, str) or not order_id.strip():
                    raise ValueError("Invalid order ID.")
                if not isinstance(raw_order, dict):
                    raise ValueError("Invalid order record.")
                order_data = cast(dict[str, object], raw_order)
                raw_lines = order_data.get("Order Lines", [])
                if not isinstance(raw_lines, list):
                    raise ValueError("Order Lines must be a list.")

                order = Order(order_id)
                for raw_line in raw_lines:
                    if not isinstance(raw_line, dict):
                        skipped_lines += 1
                        continue
                    line_data = cast(dict[str, object], raw_line)
                    product_id = line_data.get("Product ID")
                    if not isinstance(product_id, str):
                        skipped_lines += 1
                        continue
                    try:
                        quantity = _as_positive_quantity(line_data.get("Quantity"))
                    except ValueError:
                        skipped_lines += 1
                        continue

                    product = inventory.search_product(product_id)
                    if product is None:
                        skipped_lines += 1
                        continue
                    # Order creates its own OrderLine and retains the Inventory Product.
                    order.add_order_line(product, quantity)

                orders[order_id] = order
            except (KeyError, TypeError, ValueError):
                skipped_orders.append(str(order_id))

        print(f"{filename} found.")
        print(f"Loaded {len(orders)} order(s).")
        if skipped_orders:
            print(f"Skipped invalid order(s): {', '.join(skipped_orders)}")
        if skipped_lines:
            print(f"Skipped {skipped_lines} invalid or unavailable order line(s).")
        print()

    except FileNotFoundError:
        print(f"{filename} not found. Starting with no saved orders.\n")
    except (json.JSONDecodeError, OSError, UnicodeDecodeError, ValueError) as error:
        print(f"Error reading {filename}: {error}. Starting with no saved orders.\n")
    return orders


# Save each Order ID and its Product ID/quantity lines to JSON.
def save_orders(orders: dict[str, Order], filename: str = ORDERS_FILE) -> bool:
    try:
        data_to_save: dict[str, dict[str, object]] = {}
        for order_id, order in orders.items():
            order_lines: list[dict[str, object]] = []
            for order_line in order.get_order_lines():
                order_lines.append(
                    {
                        "Product ID": order_line.product.get_product_id(),
                        "Quantity": order_line.quantity,
                    }
                )
            data_to_save[order_id] = {
                "Order ID": order.get_order_id(),
                "Order Lines": order_lines,
            }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4)
        return True
    except (OSError, TypeError, ValueError) as error:
        print(f"Error saving {filename}: {error}")
        return False


# Display OrderLine details and the total for one Order.
def display_order_details(order: Order) -> None:
    print(f"\nOrder ID: {order.get_order_id()}")
    print("=" * 60)
    if not order.get_order_lines():
        print("No order lines in this order.")
    else:
        for line_number, order_line in enumerate(order.get_order_lines(), start=1):
            product = order_line.product
            print(f"\nOrder Line {line_number}")
            print(f"Product: {product.get_name()} ({product.get_product_id()})")
            print(f"Supplier: {product.supplier.get_name()}")
            print(f"Quantity: {order_line.quantity}")
            print(f"Unit Price: ${product.get_price():.2f}")
            print(f"Subtotal: ${order_line.calculate_subtotal():.2f}")
    print(f"\nOrder Total: ${order.calculate_total():.2f}")
    print("=" * 60)


# Create a new Order with a unique order ID.
def prompt_create_order(orders: dict[str, Order]) -> None:
    print("\nCreate New Order")
    order_id = input("Enter Order ID: ").strip()
    if not order_id:
        print("Order ID cannot be empty.")
        return
    if order_id in orders:
        print("Order ID already exists.")
        return
    orders[order_id] = Order(order_id)
    print(f"Order {order_id} created successfully.")


# Find and display one Order by its ID.
def prompt_display_order(orders: dict[str, Order]) -> None:
    print("\nDisplay Order")
    order_id = input("Enter Order ID: ").strip()
    order = orders.get(order_id)
    if order is None:
        print("Order not found.")
        return
    display_order_details(order)


# Display every Order in the application.
def display_all_orders(orders: dict[str, Order]) -> None:
    if not orders:
        print("No orders available.")
        return
    print("\nAll Orders")
    for order in orders.values():
        display_order_details(order)


# Add a Product from Inventory to an Order using Order.add_order_line().
def prompt_add_order_line(orders: dict[str, Order], inventory: Inventory) -> None:
    print("\nAdd Order Line to Order")
    order_id = input("Enter Order ID: ").strip()
    order = orders.get(order_id)
    if order is None:
        print("Order not found.")
        return

    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found in Inventory.")
        return

    try:
        quantity = _as_positive_quantity(input("Enter Quantity: ").strip())
    except ValueError as error:
        print(f"Invalid quantity: {error}")
        return

    # Do not construct OrderLine here. The Order creates and owns it internally.
    order.add_order_line(product, quantity)
    print(f"Added {product.get_name()} (x{quantity}) to Order {order_id}.")
    print(f"Updated Order Total: ${order.calculate_total():.2f}")


# Remove one OrderLine by its associated Product ID.
def prompt_remove_order_line(orders: dict[str, Order]) -> None:
    print("\nRemove Order Line from Order")
    order_id = input("Enter Order ID: ").strip()
    order = orders.get(order_id)
    if order is None:
        print("Order not found.")
        return

    product_id = input("Enter Product ID to remove: ").strip()
    if order.remove_order_line(product_id):
        print("Order line removed successfully.")
        print(f"Updated Order Total: ${order.calculate_total():.2f}")
    else:
        print("Matching order line not found.")


# Remove an Order from the application's Order collection.
def prompt_remove_order(orders: dict[str, Order]) -> None:
    print("\nRemove Order")
    order_id = input("Enter Order ID: ").strip()
    if order_id not in orders:
        print("Order not found.")
        return
    del orders[order_id]
    print(f"Order {order_id} removed successfully.")


# Run Order submenu; option 7 saves and returns to Main Menu.
def order_management_menu(inventory: Inventory, orders: dict[str, Order], save_callback: Callable[[], bool]) -> None:
    while True:
        print("\n========== ORDER MANAGEMENT ==========")
        print("1. Create New Order")
        print("2. Display Order")
        print("3. Display All Orders")
        print("4. Add Order Line to Order")
        print("5. Remove Order Line from Order")
        print("6. Remove Order")
        print("7. Back to Main Menu")

        option = input("Select an option (1-7): ").strip()
        if option == "1":
            prompt_create_order(orders)
        elif option == "2":
            prompt_display_order(orders)
        elif option == "3":
            display_all_orders(orders)
        elif option == "4":
            prompt_add_order_line(orders, inventory)
        elif option == "5":
            prompt_remove_order_line(orders)
        elif option == "6":
            prompt_remove_order(orders)
        elif option == "7":
            print("\nSaving application data before returning to Main Menu...")
            save_callback()
            return
        else:
            print("Invalid option. Please enter a number between 1 and 7.")
