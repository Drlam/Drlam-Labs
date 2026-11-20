import csv
from typing import Callable

from Inventory import Inventory
from Order import Order


ORDERS_FILE: str = "orders.csv"

# CSV columns used to save and load orders.
ORDERS_HEADERS: tuple[str, ...] = (
    "order_id",
    "product_id",
    "quantity",
)


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
            raise ValueError(
                "Quantity must be a whole number."
            ) from error

    elif isinstance(value, float) and value.is_integer():
        quantity = int(value)

    else:
        raise ValueError("Quantity must be a whole number.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    return quantity


# Load Orders and reconnect each OrderLine to the Product in Inventory.
def load_orders(
    inventory: Inventory,
    filename: str = ORDERS_FILE
) -> dict[str, Order]:

    orders: dict[str, Order] = {}

    try:
        with open(
            filename, "r", newline="", encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            # Check that the CSV contains a header row.
            if reader.fieldnames is None:
                raise ValueError("The orders CSV file is empty.")

            # Check that all required columns exist.
            missing_headers = [
                header
                for header in ORDERS_HEADERS
                if header not in reader.fieldnames
            ]

            if missing_headers:
                raise ValueError(
                    "Missing CSV column(s): "
                    + ", ".join(missing_headers)
                )

            skipped_rows = 0

            for row in reader:

                try:
                    # Detect rows containing extra values.
                    if None in row:
                        raise ValueError(
                            "CSV row contains more values than expected."
                        )

                    order_id = row.get("order_id")

                    if not isinstance(order_id, str) or not order_id.strip():
                        raise ValueError("Order ID cannot be empty.")

                    order_id = order_id.strip()

                    # Create an Order only once, even when it has multiple lines.
                    if order_id not in orders:
                        orders[order_id] = Order(order_id)

                    product_id = row.get("product_id")
                    quantity_text = row.get("quantity")

                    # An empty Product ID and quantity represent an empty Order.
                    if (
                        not product_id or not product_id.strip()
                    ) and (
                        not quantity_text or not quantity_text.strip()
                    ):
                        continue

                    # Both Product ID and quantity are required for an OrderLine.
                    if not isinstance(product_id, str) or not product_id.strip():
                        raise ValueError("Product ID cannot be empty.")

                    if not isinstance(quantity_text, str) or not quantity_text.strip():
                        raise ValueError("Quantity cannot be empty.")

                    product_id = product_id.strip()

                    # Validate the OrderLine quantity.
                    quantity = _as_positive_quantity(quantity_text)

                    # Reconnect the OrderLine to the Product in Inventory.
                    product = inventory.search_product(product_id)

                    if product is None:
                        raise ValueError(
                            f"Product '{product_id}' not found in Inventory."
                        )

                    # Order creates and owns its OrderLine internally.
                    orders[order_id].add_order_line(product, quantity)

                except (KeyError, TypeError, ValueError, OverflowError) as error:
                    skipped_rows += 1
                    print(f"Skipping row {reader.line_num}: {error}")

        # Display loading results.
        print(f"{filename} found.")
        print(f"Loaded {len(orders)} order(s).")

        if skipped_rows:
            print(
                f"Skipped {skipped_rows} invalid order row(s)."
            )

        print()

    except FileNotFoundError:
        print(
            f"{filename} not found. Starting with no saved orders.\n"
        )

    except (
        csv.Error,
        OSError,
        UnicodeDecodeError,
        ValueError
    ) as error:

        # Discard partially loaded orders after a file-level error.
        orders = {}

        print(
            f"Error reading {filename}: {error}. "
            "Starting with no saved orders.\n"
        )

    return orders


# Save each Order ID and its Product ID/quantity lines to CSV.
def save_orders(
    orders: dict[str, Order],
    filename: str = ORDERS_FILE
) -> bool:

    try:
        data_to_save: list[dict[str, object]] = []

        for order_id, order in orders.items():

            order_lines = order.get_order_lines()

            # Preserve Orders that do not contain any OrderLines.
            if not order_lines:
                data_to_save.append(
                    {
                        "order_id": order_id,
                        "product_id": "",
                        "quantity": "",
                    }
                )

                continue

            # Save each OrderLine as a separate CSV row.
            for order_line in order_lines:

                data_to_save.append(
                    {
                        "order_id": order_id,
                        "product_id": order_line.product.get_product_id(),
                        "quantity": order_line.quantity,
                    }
                )

        with open(
            filename, "w", newline="", encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=ORDERS_HEADERS
            )

            # Write the CSV header.
            writer.writeheader()

            # Write all Order and OrderLine records.
            writer.writerows(data_to_save)

        return True

    except (OSError, TypeError, ValueError, csv.Error) as error:
        print(f"Error saving {filename}: {error}")
        return False


# Display OrderLine details and the total for one Order.
def display_order_details(order: Order) -> None:

    print(f"\nOrder ID: {order.get_order_id()}")
    print("=" * 60)

    if not order.get_order_lines():
        print("No order lines in this order.")

    else:
        for line_number, order_line in enumerate(
            order.get_order_lines(), start=1
        ):

            product = order_line.product

            print(f"\nOrder Line {line_number}")
            print(
                f"Product: {product.get_name()} "
                f"({product.get_product_id()})"
            )
            print(f"Supplier: {product.supplier.get_name()}")
            print(f"Quantity: {order_line.quantity}")
            print(f"Unit Price: ${product.get_price():.2f}")
            print(
                f"Subtotal: ${order_line.calculate_subtotal():.2f}"
            )

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
def prompt_add_order_line(
    orders: dict[str, Order],
    inventory: Inventory
) -> None:

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
        quantity = _as_positive_quantity(
            input("Enter Quantity: ").strip()
        )

    except ValueError as error:
        print(f"Invalid quantity: {error}")
        return

    # Do not construct OrderLine here.
    # The Order creates and owns it internally.
    order.add_order_line(product, quantity)

    print(
        f"Added {product.get_name()} (x{quantity}) "
        f"to Order {order_id}."
    )
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


# Run the Order submenu; option 7 saves and returns to Main Menu.
def order_management_menu(
    inventory: Inventory,
    orders: dict[str, Order],
    save_callback: Callable[[], bool]
) -> None:

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
            print(
                "\nSaving application data before returning to Main Menu..."
            )
            save_callback()
            return

        else:
            print("Invalid option. Please enter a number between 1 and 7.")