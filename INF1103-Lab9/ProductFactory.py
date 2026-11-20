from DigitalProduct import DigitalProduct
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier

# Factory that centralises product creation; callers only need to know about Product
class ProductFactory:
    # Build the right Product for product_type ("physical" or "digital").
    # extra_value is the weight in kg for a physical product, or the download size in MB for a digital one.
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, extra_value: float) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, extra_value, supplier)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, extra_value, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")