from Supplier import Supplier
from DigitalProduct import DigitalProduct
from PhysicalProduct import PhysicalProduct

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