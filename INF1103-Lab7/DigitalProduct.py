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


# Testing to ensure that the DigitalProduct class is working correctly
if __name__ == "__main__":
    digital1 = DigitalProduct("P003", "TV", 2999, 2, 150.17)
    digital2 = DigitalProduct("P004", "Earpiece", 10.9, 40, 15)
    digital1.display_information()
    digital2.display_information()
    print(f"Download Size of {digital1.get_name()}: {digital1.get_download_size():.2f} MB")
    print(f"Download Size of {digital2.get_name()}: {digital2.get_download_size():.2f} MB")