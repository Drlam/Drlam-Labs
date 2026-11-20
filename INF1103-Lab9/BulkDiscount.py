from DiscountStrategy import DiscountStrategy

# Strategy that takes a fixed amount off totals at or above a threshold
class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        # Validation: neither the threshold nor the amount can be negative
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    # Getter methods
    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    # Take the amount off when the total reaches the threshold (never below zero)
    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)
        return total