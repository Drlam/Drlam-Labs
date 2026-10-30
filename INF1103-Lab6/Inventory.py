# Inventory Class
class Inventory:
    def __init__(self):
        self.__products = {}

    # Adding a new product
    def add_product(self, product):
        product_id = product.get_product_id()
        if product_id in self.__products:
            return False
        self.__products[product_id]= product
        return True

    # Searching for a product by its ID
    def search_product(self, product_id):
        return self.__products.get(product_id)

    # Displaying all products in the inventory
    def display_all(self):
        if not self.__products:
            print("No inventory data available.")
            return

        for product in self.__products.values():
            product.display_information()

    # Returning a list of products
    def get_all_products(self):
        return list(self.__products.values())