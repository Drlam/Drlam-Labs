from Supplier import Supplier
from DigitalProduct import DigitalProduct
from PhysicalProduct import PhysicalProduct
from Inventory import Inventory
from Order import Order

print("\nTesting Association")
# Create a supplier object
supplier = Supplier(1, "Tech Pte Ltd", "abc@gmail.com")
# Create a physical and digital product object
physical_product = PhysicalProduct("P001", "Laptop", 1200.00, 10, 5.66, supplier)
digital_product = DigitalProduct("D001", "E-book", 19.9, 50, 300.17, supplier)
# Check product object association
print(physical_product is supplier)
print(digital_product is supplier)
# Display product supplier information
physical_product.supplier.display_information()
digital_product.supplier.display_information()
# check after deleting supplier variable
del supplier
print("\nAfter deleting the supplier object:")
physical_product.supplier.display_information()
digital_product.supplier.display_information()

print("\nTesting Aggregation")
# Create product and add it to Inventory A
supplier2 = Supplier(2, "Phone Pte Ltd", "efg@gmail.com")
product = PhysicalProduct("P002", "Smartphone", 490, 20, 0.55, supplier2)
inventoryA = Inventory()
inventoryA.add_product(product)
print(inventoryA.search_product("P002").get_product_id())

# Remove product from Inventory A
print(inventoryA.remove_product("P002"))

# Check if product can still be used
product.display_information()

# Create Inventory B and add the same product to it
inventoryB = Inventory()
inventoryB.add_product(product)
print(inventoryB.search_product("P002").get_product_id())
print(inventoryB.search_product("P002") is product)

# Remove product from Inventory B
print(inventoryB.remove_product("P002"))

# Check if product doesn't get destroyed after being removed from Inventory B
product.display_information()

print("\nTesting Composition")
# Create an Order and add order lines to it
order1 = Order("O001")
order1.add_order_line(physical_product, 5)
order1.add_order_line(digital_product, 10)

# Display order1 information and calculate total value
print("Order 1 Details:")
for order_line in order1.order_lines:
    print(f"Product: {order_line.product.get_name()}, Quantity: {order_line.quantity}, "
          f"Subtotal: ${order_line.calculate_subtotal():.2f}")
print(f"Total Order Value: ${order1.calculate_total():.2f}")

# Create a second Order
order2 = Order("O002")
order2.add_order_line(physical_product, 2)

# Check if each object has its own OrderLine
print("\nChecking if order1 and order2 have their own OrderLine objects:")
print(order1.order_lines[0] is order2.order_lines[0])
print(order1.order_lines[0].product is order2.order_lines[0].product)

# Display order2 information and calculate total value
print("\nOrder 2 Details:")
for order_line in order2.order_lines:
    print(f"Product: {order_line.product.get_name()}, Quantity: {order_line.quantity}, "
          f"Subtotal: ${order_line.calculate_subtotal():.2f}")
print(f"Total Order Value: ${order2.calculate_total():.2f}")

# Removing order line from order2
print("\nRemoving order line from order2:")
print(order2.remove_order_line("P001"))
print(f"Order 2 total value after removing: ${order2.calculate_total():.2f}")

# Check if physical_product still exists
print("\nChecking if physical_product still exists after removing from order2:")
physical_product.display_information()