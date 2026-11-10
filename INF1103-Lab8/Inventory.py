from Product import Product

class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    # Adding a new product
    def add_product(self, product: Product) -> bool:
        for existing_product in self.__products:
            if existing_product.get_product_id() == product.get_product_id():
                return False
            
        self.__products.append(product)
        return True

    # Delete an existing product
    def remove_product(self, product_id: str) -> bool:
        for product in self.__products:
            if product.get_product_id() == product_id:
                self.__products.remove(product)
                return True
        return False

    # Searching for a product by its ID
    def search_product(self, product_id: str) -> Product | None:
        for existing_product in self.__products:
            if existing_product.get_product_id() == product_id:
                return existing_product
        return None

    # Displaying all products in the inventory
    def display_all(self) -> None:
        if not self.__products:
            print("No inventory data available.")
            return

        for product in self.__products:
            product.display_information()

    # Returning a list of products
    def get_all_products(self) -> list[Product]:
        return list(self.__products)