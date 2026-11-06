from Product import Product
from CanBeShipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
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

    # Calculate shipping cost based on weight and a base shipping cost
    def calculate_shipping_cost(self):
        base_shipping_cost = 5.00
        cost_per_kg = 1.00
        total_shipping_cost = base_shipping_cost + (self.__weight * cost_per_kg)
        return total_shipping_cost