def apply_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")

    final_price = price - (price * discount_percent / 100)
    return round(final_price, 2)


def add_tax(price, tax_rate=18):
    final_price = price + (price * tax_rate / 100)
    return round(final_price, 2)

