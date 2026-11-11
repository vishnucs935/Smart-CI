class Inventory:
    def __init__(self):
        self.stock = {}

    def add_stock(self, product, quantity):
        self.stock[product] = self.stock.get(product, 0) + quantity

    def remove_stock(self, product, quantity):
        if product not in self.stock:
            raise ValueError("Product not found")

        if quantity > self.stock[product]:
            raise ValueError("Not enough stock")

        self.stock[product] -= quantity

    def get_stock(self, product):
        return self.stock.get(product, 0)
