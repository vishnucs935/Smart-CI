import sys


def calculate_total(price, tax_rate):
    if "--fixed" in sys.argv:
        return price + (price * tax_rate / 100)

    # Intentional bug: tax is not added.
    return price


price = 100
tax_rate = 18
expected = 118

actual = calculate_total(price, tax_rate)

print(f"Expected total: {expected}")
print(f"Actual total:   {actual}")

if actual == expected:
    print("BUILD PASSED")
    sys.exit(0)
else:
    print("BUILD FAILED: Incorrect total")
    sys.exit(1)
