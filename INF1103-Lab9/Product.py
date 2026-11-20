from abc import ABC, abstractmethod
from Supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
         # Validate product price
        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        # Validate product stock
        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.supplier: Supplier = supplier # association with Supplier class

    # Getters for private attributes
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    # Update stock quantity of the product
    def update_stock(self, quantity: int) -> bool:
        if quantity < 0:
            return False

        self.__stock = quantity
        return True

    # Display product information
    def display_information(self) -> None:
        print(f"Product ID: {self.__product_id}, Name: {self.__name}, "
              f"Price: ${self.__price:.2f}, Stock: {self.__stock}")

    # Abstract method to be implemented by PhysicalProduct and DigitalProduct classes
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass