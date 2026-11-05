from Product import Product
from CanBeShipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    # Getter method
    def get_weight(self):
        return self.__weight

    # Display product information
    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    # Fulfilment information for physical products
    def get_fulfilment_info(self):
        return f"{self.get_name()} (Product ID: {self.get_product_id()}) requires physical shipping."

    # Calculate shipping cost based on weight
    def calculate_shipping_cost(self):
        base_shipment_cost = 5.00
        cost_per_kg = 1.00
        total_shipping_cost = base_shipment_cost + (self.__weight * cost_per_kg)
        return total_shipping_cost

    
# Testing to ensure that the PhysicalProduct class is working correctly
if __name__ == "__main__":
    physicalProduct1 = PhysicalProduct("P001", "Laptop", 1500.99, 10, 3.67)
    physicalProduct2 = PhysicalProduct("P002", "Smartphone", 499.99, 20, 0.2)
    physicalProduct1.display_information()
    physicalProduct2.display_information()
    print(physicalProduct1.get_fulfilment_info())
    print(physicalProduct2.get_fulfilment_info())
    print(f"Weight of {physicalProduct1.get_name()}: {physicalProduct1.get_weight():.2f} kg")
    print(f"Weight of {physicalProduct2.get_name()}: {physicalProduct2.get_weight():.2f} kg")
