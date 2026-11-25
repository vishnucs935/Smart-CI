from src.pricing import add_tax, apply_discount


class Cart:
    def __init__(self):
        self.items = []

    def add(self, name, price, qty=1):
        self.items.append((name, price, qty))

    def total(self, discount=0):
        subtotal = sum(price * qty for _, price, qty in self.items)
        return add_tax(apply_discount(subtotal, discount))
