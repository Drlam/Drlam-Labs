from OrderLine import OrderLine
from Product import Product

class Order:
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

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
        total: float = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total