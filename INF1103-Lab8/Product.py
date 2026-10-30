# Product Class
class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Getters for private attributes
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # Update stock quantity of the product
    def update_stock(self, quantity):
        if quantity < 0:
            return False

        self.__stock = quantity
        return True

    # Display product information
    def display_information(self):
        print(f"Product ID: {self.__product_id}, Name: {self.__name}, "
              f"Price: ${self.__price:.2f}, Stock: {self.__stock}")