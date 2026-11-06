from Product import Product

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    # Getter for download size
    def get_download_size(self):
        return self.__download_size

    # Display product information
    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")

    # Fulfilment information for digital products
    def get_fulfilment_info(self):    
        return f"{self.get_name()} (Product ID: {self.get_product_id()}) is delivered digitally."