from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct

physicalProduct1 = PhysicalProduct("P001", "Laptop", 1500.99, 10, 5.56)
physicalProduct2 = PhysicalProduct("P002", "Smartphone", 490.00, 20, 0.5)
digitalProduct = DigitalProduct("D003", "E-book", 29.99, 2, 300.17)
physicalProduct1.display_information()
physicalProduct2.display_information()
print()
digitalProduct.display_information()
print()
print(physicalProduct1.get_fulfilment_info())
print(physicalProduct2.get_fulfilment_info())
print(digitalProduct.get_fulfilment_info())
# Test calculate_shipping_cost method for PhysicalProduct
print(f"Shipping cost for {physicalProduct1.get_name()}: ${physicalProduct1.calculate_shipping_cost():.2f}")
print(f"Shipping cost for {physicalProduct2.get_name()}: ${physicalProduct2.calculate_shipping_cost():.2f}")