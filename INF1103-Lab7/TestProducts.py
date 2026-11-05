from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Product import Product

physicalProduct = PhysicalProduct("P001", "Laptop", 1500.99, 10, 3.67)
digitalProduct = DigitalProduct("P002", "TV", 2999, 2, 150.17)
physicalProduct.display_information()
print()
digitalProduct.display_information()
print()
physicalProduct.get_fulfilment_info()
digitalProduct.get_fulfilment_info()
# This will fail as Product is an abstract class and cannot be instantiated directly.
failedProduct = Product("P005", "Gloves", 12.50, 50)
print(failedProduct.get_fulfilment_info())