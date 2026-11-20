from OrderLine import OrderLine
from Product import Product
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount

class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = (discount if discount is not None else NoDiscount())

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    # Add an order line to the order
    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    # Remove an order line from the order
    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.product.get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    # Calculate total value of the order by asking OrderLine to calculate subtotal
    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)