import math
import csv
from typing import Callable, cast

from CanBeShipped import CanBeShipped
from DigitalProduct import DigitalProduct
from Inventory import Inventory
from Order import Order
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier
from ProductFactory import ProductFactory


INVENTORY_FILE: str = "inventory.csv"

# Product type identifiers
PHYSICAL_PRODUCT_TYPE: str = "physical"
DIGITAL_PRODUCT_TYPE: str = "digital"

# CSV columns used to save and load inventory.
INVENTORY_HEADERS: tuple[str, ...] = (
    "product_type",
    "product_id",
    "name",
    "price",
    "stock_quantity",
    "supplier_id",
    "supplier_name",
    "supplier_email",
    "weight",
    "download_size",
)


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
            raise ValueError(
                f"Invalid integer value for {field_name}."
            ) from error

    raise ValueError(f"Invalid integer value for {field_name}.")


# Validate required text values read from a CSV row.
def _required_csv_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")

    return value.strip()


# Create or reuse a Supplier, ensuring one object per Supplier ID.
def _supplier_from_csv(
    row: dict[str, str | None],
    supplier_registry: dict[int, Supplier]
) -> Supplier:

    supplier_id = _as_int(row.get("supplier_id"), "Supplier ID")

    name = _required_csv_text(
        row.get("supplier_name"), "Supplier name"
    )

    contact_email = _required_csv_text(
        row.get("supplier_email"), "Supplier email"
    )

    existing = supplier_registry.get(supplier_id)

    if existing is not None:
        if (
            existing.get_name() != name
            or existing.get_contact_email() != contact_email
        ):
            raise ValueError(
                f"Conflicting details for Supplier ID {supplier_id}."
            )

        return existing

    supplier = Supplier(supplier_id, name, contact_email)
    supplier_registry[supplier_id] = supplier

    return supplier


# Reconstruct a Product and its Supplier association from a CSV row.
def _product_from_csv_row(
    row: dict[str, str | None],
    supplier_registry: dict[int, Supplier]
) -> Product:

    product_type = _required_csv_text(
        row.get("product_type"), "Product type"
    ).lower()

    product_id = _required_csv_text(
        row.get("product_id"), "Product ID"
    )

    name = _required_csv_text(
        row.get("name"), "Product name"
    )

    price = _as_float(row.get("price"), "Price")
    stock = _as_int(row.get("stock_quantity"), "Stock Quantity")

    # Reconstruct the Supplier association.
    supplier = _supplier_from_csv(row, supplier_registry)

    # Read the product-specific information.
    if product_type == PHYSICAL_PRODUCT_TYPE:
        extra_value = _as_float(row.get("weight"), "Weight")

    elif product_type == DIGITAL_PRODUCT_TYPE:
        extra_value = _as_float(
            row.get("download_size"), "Download Size"
        )

    else:
        raise ValueError(f"Unknown product type: {product_type}")

    # Use ProductFactory to create the appropriate Product.
    return ProductFactory.create(
        product_type,
        product_id,
        name,
        price,
        stock,
        supplier,
        extra_value
    )


# Convert a Product and its Supplier details into a CSV-compatible row.
def _product_to_csv_row(product: Product) -> dict[str, object]:

    common_data: dict[str, object] = {
        "product_id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock_quantity": product.get_stock(),
        "supplier_id": product.supplier.get_supplier_id(),
        "supplier_name": product.supplier.get_name(),
        "supplier_email": product.supplier.get_contact_email(),
    }

    # Save PhysicalProduct-specific information.
    if isinstance(product, PhysicalProduct):
        return {
            "product_type": PHYSICAL_PRODUCT_TYPE,
            **common_data,
            "weight": product.get_weight(),
            "download_size": "",
        }

    # Save DigitalProduct-specific information.
    if isinstance(product, DigitalProduct):
        return {
            "product_type": DIGITAL_PRODUCT_TYPE,
            **common_data,
            "weight": "",
            "download_size": product.get_download_size(),
        }

    raise ValueError(
        f"Unsupported Product type: {product.get_product_id()}"
    )


# Keep asking until the user enters a finite number greater than zero.
def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))

            # Reject NaN and infinity.
            if not math.isfinite(value):
                raise ValueError("Not a finite number.")

            # Price must be greater than zero.
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


# Load products from a CSV file into Inventory.
# This function is used for the Section 5.2 CSV exercise.
def load_products(
    path: str,
    inventory: Inventory,
    supplier: Supplier
) -> None:

    loaded = 0

    try:
        file = open(path, newline="")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        with file:
            reader = csv.reader(file)

            # Skip the header row.
            next(reader, None)

            for row in reader:
                if not row:
                    continue

                try:
                    # Check that the row contains exactly 5 columns.
                    if len(row) != 5:
                        raise ValueError(
                            "Each row must contain exactly 5 columns."
                        )

                    # Extract product information.
                    product_type, product_id, name, price_text, stock_text = [
                        value.strip() for value in row
                    ]

                    # Convert price and stock into numeric values.
                    price = _as_float(price_text, "Price")
                    stock = _as_int(stock_text, "Stock Quantity")

                    # The CSV does not contain weight or download size.
                    # Use 1.0 as a placeholder for this exercise.
                    extra_value = 1.0

                    # Create the product using ProductFactory.
                    product = ProductFactory.create(
                        product_type.lower(),
                        product_id,
                        name,
                        price,
                        stock,
                        supplier,
                        extra_value
                    )

                    # Add the product to Inventory.
                    if not inventory.add_product(product):
                        raise ValueError(
                            f"Product ID '{product_id}' already exists."
                        )

                    loaded += 1

                except ValueError as error:
                    print(f"Skipping row {reader.line_num}: {error}")

        # Display the number of successfully loaded products.
        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")


# Load Products and their Supplier objects from a CSV file.
def load_inventory(filename: str = INVENTORY_FILE) -> Inventory:

    inventory = Inventory()
    supplier_registry: dict[int, Supplier] = {}

    try:
        with open(
            filename, "r", newline="", encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            # Check that the CSV contains a header row.
            if reader.fieldnames is None:
                raise ValueError("The inventory CSV file is empty.")

            # Check that all required columns exist.
            missing_headers = [
                header
                for header in INVENTORY_HEADERS
                if header not in reader.fieldnames
            ]

            if missing_headers:
                raise ValueError(
                    "Missing CSV column(s): "
                    + ", ".join(missing_headers)
                )

            skipped_ids: list[str] = []

            for row in reader:

                try:
                    # Skip completely empty rows.
                    if not row or all(
                        value is None or not value.strip()
                        for key, value in row.items()
                        if key is not None
                    ):
                        continue

                    # Detect rows containing extra values.
                    if None in row:
                        raise ValueError(
                            "CSV row contains more values than expected."
                        )

                    csv_row = cast(
                        dict[str, str | None], row
                    )

                    # Reconstruct the Product using the factory.
                    product = _product_from_csv_row(
                        csv_row, supplier_registry
                    )

                    # Add the Product to Inventory.
                    if not inventory.add_product(product):
                        raise ValueError(
                            f"Product ID '{product.get_product_id()}' "
                            "already exists."
                        )

                except (
                    KeyError,
                    TypeError,
                    ValueError,
                    OverflowError
                ) as error:

                    product_id = row.get("product_id")

                    if (
                        not isinstance(product_id, str)
                        or not product_id.strip()
                    ):
                        product_id = f"row {reader.line_num}"

                    skipped_ids.append(product_id)
                    print(f"Skipping {product_id}: {error}")

        # Report the loading results.
        print(f"{filename} found.")

        if skipped_ids:
            print(
                "Skipped invalid or duplicate product(s): "
                f"{', '.join(skipped_ids)}"
            )

        if not skipped_ids:
            print("Inventory loaded successfully.")

        print()
        return inventory

    except FileNotFoundError:
        print(
            f"{filename} not found. Starting with an empty inventory.\n"
        )

    except (
        csv.Error,
        OSError,
        UnicodeDecodeError,
        ValueError
    ) as error:

        # Discard partially loaded products after a file-level error.
        inventory = Inventory()

        print(
            f"Error reading {filename}: {error}. "
            "Starting with an empty inventory.\n"
        )

    return inventory


# Save Products and associated Supplier details to a CSV file.
def save_inventory(
    inventory: Inventory,
    filename: str = INVENTORY_FILE
) -> bool:

    try:
        # Convert all Products into CSV-compatible rows.
        data_to_save: list[dict[str, object]] = [
            _product_to_csv_row(product)
            for product in inventory.get_all_products()
        ]

        with open(
            filename, "w", newline="", encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=INVENTORY_HEADERS
            )

            # Write the CSV header.
            writer.writeheader()

            # Write all Product records.
            writer.writerows(data_to_save)

        return True

    except (
        OSError,
        TypeError,
        ValueError,
        csv.Error
    ) as error:

        print(f"Error saving {filename}: {error}")
        return False


# Reuse a matching Supplier ID or create a new Supplier object.
def _find_or_create_supplier(
    inventory: Inventory,
    supplier_id: int,
    name: str,
    contact_email: str
) -> Supplier | None:

    for product in inventory.get_all_products():
        existing = product.supplier

        if existing.get_supplier_id() == supplier_id:
            if (
                existing.get_name() == name
                and existing.get_contact_email() == contact_email
            ):
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

    # Keep asking until a valid positive price is entered.
    price = get_positive_float("Enter Price: ")

    try:
        stock = _as_int(
            input("Enter Stock Quantity: ").strip(),
            "Stock Quantity"
        )

        supplier_id = _as_int(
            input("Enter Supplier ID: ").strip(),
            "Supplier ID"
        )

    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    if supplier_id <= 0:
        print("Supplier ID must be positive.")
        return

    supplier_name = input("Enter Supplier Name: ").strip()
    contact_email = input("Enter Supplier Email: ").strip()

    if not supplier_name or not contact_email:
        print("Supplier name and email cannot be empty.")
        return

    supplier = _find_or_create_supplier(
        inventory,
        supplier_id,
        supplier_name,
        contact_email
    )

    if supplier is None:
        return

    product_type = input(
        "Product Type (P = Physical, D = Digital): "
    ).strip().upper()

    # Translate the menu choice into the type name the factory understands.
    if product_type in ("P", "PHYSICAL"):
        factory_type = PHYSICAL_PRODUCT_TYPE
        extra_prompt = "Enter Weight (kg): "
        extra_name = "Weight"

    elif product_type in ("D", "DIGITAL"):
        factory_type = DIGITAL_PRODUCT_TYPE
        extra_prompt = "Enter Download Size (MB): "
        extra_name = "Download Size"

    else:
        print("Invalid product type. Please enter P or D.")
        return

    try:
        extra_value = _as_float(
            input(extra_prompt).strip(),
            extra_name
        )

        # Product classes enforce price, stock and type-specific validation.
        product: Product = ProductFactory.create(
            factory_type,
            product_id,
            name,
            price,
            stock,
            supplier,
            extra_value
        )

    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    if not inventory.add_product(product):
        print("Product ID already exists. Product was not added.")
        return

    print("Product added successfully.")
    display_product_with_supplier(product)

    print(
        f"Fulfilment Information: "
        f"{product.get_fulfilment_info()}"
    )


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
        quantity = _as_int(
            input("Enter New Stock Quantity: ").strip(),
            "Stock Quantity"
        )

        if not product.update_stock(quantity):
            print("Stock quantity cannot be negative. Update cancelled.")
            return

    except ValueError as error:
        print(f"Invalid quantity: {error}")
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
        print(
            f"Total Shipping Cost: "
            f"${product.calculate_shipping_cost():.2f}"
        )


# Remove a Product from Inventory when no saved OrderLine depends on it.
def prompt_remove_product(
    inventory: Inventory,
    orders: dict[str, Order]
) -> None:

    print("\nRemove Product")

    product_id = input("Enter Product ID to remove: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    # Prevent removal if an existing OrderLine uses this Product.
    for order in orders.values():
        for order_line in order.get_order_lines():

            if order_line.product.get_product_id() == product_id:
                print(
                    "Cannot remove this product because "
                    "it is used in an existing order."
                )
                print(
                    "Remove the corresponding order line first, "
                    "then try again."
                )
                return

    if inventory.remove_product(product_id):
        print(
            f"Product {product_id} removed from Inventory successfully."
        )
        print("The Product object itself is not destroyed.")

    else:
        print("Product could not be removed.")


# Run the Inventory submenu; option 7 saves and returns to Main Menu.
def inventory_management_menu(
    inventory: Inventory,
    orders: dict[str, Order],
    save_callback: Callable[[], bool]
) -> None:

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
                print(
                    f"Inventory saved successfully to {INVENTORY_FILE}."
                )

        elif option == "7":
            print(
                "\nSaving application data before returning to Main Menu..."
            )
            save_callback()
            return

        else:
            print("Invalid option. Please enter a number between 1 and 7.")
