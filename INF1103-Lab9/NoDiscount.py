from DiscountStrategy import DiscountStrategy

# Strategy that leaves the order total unchanged
class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total