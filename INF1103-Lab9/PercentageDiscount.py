from DiscountStrategy import DiscountStrategy

# Strategy that takes a fixed percentage off the order total
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        # check if percentage is be more than or equal to 0 and less than or equal to 100
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    # Getter method
    def get_percentage(self) -> float:
        return self.__percentage

    # Return the total with the percentage taken off
    def apply(self, total: float) -> float:
        return total - (total * self.__percentage / 100)