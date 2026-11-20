from Order import Order
from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from BulkDiscount import BulkDiscount
from PercentageDiscount import PercentageDiscount
from StudentDiscount import StudentDiscount
from ProductFactory import ProductFactory


# Create a new Supplier for testing
supplier = Supplier(1, "Test Supplier", "test@example.com")


# ==========================================
# TEST 1: PRODUCT FACTORY
# ==========================================

print("\n========== PRODUCT FACTORY TESTS ==========")

# Test physical product creation
product = ProductFactory.create(
    "physical", "TEST001", "Discount Test Product",
    125.00, 10, supplier, 1.0
)

assert isinstance(product, PhysicalProduct)
print("Physical product factory test passed.")

# Test digital product creation
digital_product = ProductFactory.create(
    "digital", "TEST002", "Test Ebook",
    9.90, 20, supplier, 25.0
)

assert isinstance(digital_product, DigitalProduct)
print("Digital product factory test passed.")

# Test unknown product type
try:
    ProductFactory.create(
        "service", "TEST003", "Installation",
        30.00, 5, supplier, 0
    )
except ValueError as error:
    assert str(error) == "Unknown product type: service"
    print("Unknown product type test passed.")
else:
    raise AssertionError(
        "Expected ValueError for unknown product type."
    )


# ==========================================
# TEST 2: STRATEGY PATTERN
# ==========================================

print("\n========== DISCOUNT STRATEGY TESTS ==========")

# TEST 1: Default NoDiscount
default_order = Order("TEST001")
default_order.add_order_line(product, 2)

print(
    "Default Discount:",
    f"${default_order.calculate_total():.2f}"
)

# TEST 2: BulkDiscount
order = Order("TEST002", BulkDiscount(200, 20))
order.add_order_line(product, 2)

print(
    "Bulk Discount:",
    f"${order.calculate_total():.2f}"
)

# TEST 3: Change to PercentageDiscount
order.set_discount(PercentageDiscount(10))

print(
    "Percentage Discount:",
    f"${order.calculate_total():.2f}"
)

# TEST 4: StudentDiscount
student_order = Order("TEST004", StudentDiscount())
student_order.add_order_line(product, 2)

print(
    "Student Discount:",
    f"${student_order.calculate_total():.2f}"
)


# Test unknown product type without exception handling
print("\nTesting unknown product type without try/except:")

ProductFactory.create(
    "service",
    "TEST003",
    "Installation",
    30.00,
    5,
    supplier,
    0
)

print("Testing the code")