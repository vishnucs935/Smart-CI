from src.pricing import apply_discount, add_tax


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity=1):
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def total(self, discount_percent=0):
        subtotal = sum(
            item["price"] * item["quantity"]
            for item in self.items
        )

        discounted_price = apply_discount(subtotal, discount_percent)
        return add_tax(discounted_price)
