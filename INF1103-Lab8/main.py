from Inventory import Inventory
from inventory_manager import (
    INVENTORY_FILE,
    inventory_management_menu,
    load_inventory,
    save_inventory,
)
from order_manager import (
    ORDERS_FILE,
    load_orders,
    order_management_menu,
    save_orders,
)
from Order import Order


# Save both inventory and orders and report whether both succeeded.
def save_application_data(inventory: Inventory, orders: dict[str, Order]) -> bool:
    inventory_saved = save_inventory(inventory)
    orders_saved = save_orders(orders)

    if inventory_saved and orders_saved:
        print("Inventory and orders saved successfully.")
        return True
    if inventory_saved:
        print("Inventory saved, but orders could not be saved.")
    elif orders_saved:
        print("Orders saved, but inventory could not be saved.")
    else:
        print("Inventory and orders could not be saved.")
    return False


# Load saved data and navigate between the two management menus.
def main() -> None:
    print("========== INVENTORY AND ORDER MANAGEMENT SYSTEM ==========")
    inventory = load_inventory(INVENTORY_FILE)
    orders = load_orders(inventory, ORDERS_FILE)

    # Save the current inventory and orders together.
    def save_all() -> bool:
        return save_application_data(inventory, orders)

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Inventory Management")
        print("2. Order Management")
        print("3. Exit")

        option = input("Select an option (1-3): ").strip()
        if option == "1":
            inventory_management_menu(inventory, orders, save_all)
        elif option == "2":
            order_management_menu(inventory, orders, save_all)
        elif option == "3":
            print("\nSaving inventory and orders before exit...")
            if save_all():
                print("All application data saved successfully.")
            print("Thank you for using the Inventory and Order Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 3.")


if __name__ == "__main__":
    main()