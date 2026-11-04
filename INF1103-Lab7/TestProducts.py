from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct

physical1 = PhysicalProduct("P001", "Laptop", 1500.99, 10, 3.67)
digital1 = DigitalProduct("P002", "TV", 2999, 2, 150.17)
physical1.display_information()
print()
digital1.display_information()