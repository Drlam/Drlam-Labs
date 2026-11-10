from Supplier import Supplier
from DigitalProduct import DigitalProduct
from PhysicalProduct import PhysicalProduct
from Inventory import Inventory

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