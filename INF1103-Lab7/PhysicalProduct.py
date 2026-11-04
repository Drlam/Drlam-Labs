from Product import Product

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    # Getter for weight
    def get_weight(self):
        return self.__weight

    # Display product information
    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")


# Testing to ensure that the PhysicalProduct class is working correctly
if __name__ == "__main__":
    physical1 = PhysicalProduct("P001", "Laptop", 1500.99, 10, 3.67)
    physical2 = PhysicalProduct("P002", "Smartphone", 499.99, 20, 0.2)
    physical1.display_information()
    physical2.display_information()
    print(f"Weight of {physical1.get_name()}: {physical1.get_weight():.2f} kg")
    print(f"Weight of {physical2.get_name()}: {physical2.get_weight():.2f} kg")
