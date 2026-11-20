from DiscountStrategy import DiscountStrategy

# Strategy that gives students a 5% discount
class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total - (total * 5 / 100)