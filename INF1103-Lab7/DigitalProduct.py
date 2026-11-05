from Product import Product

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
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


# Testing to ensure that the DigitalProduct class is working correctly
if __name__ == "__main__":
    digitalProduct1 = DigitalProduct("D003", "E-book", 29.99, 2, 300.17)
    digitalProduct2 = DigitalProduct("D004", "Software", 49.99, 5, 600.28)
    digitalProduct1.display_information()
    digitalProduct2.display_information()
    print(digitalProduct1.get_fulfilment_info())
    print(digitalProduct2.get_fulfilment_info())
    print(f"Download Size of {digitalProduct1.get_name()}: {digitalProduct1.get_download_size():.2f} MB")
    print(f"Download Size of {digitalProduct2.get_name()}: {digitalProduct2.get_download_size():.2f} MB")