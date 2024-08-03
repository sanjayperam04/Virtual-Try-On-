import random
import time

class Product:
    def __init__(self, base_price):
        self.base_price = base_price
        self.current_price = base_price
        self.demand_level = "Normal"
        self.competitor_prices = []
        self.purchase_counter = 0
        self.last_purchase_time = 0
        self.price_increase_percentage = 0.01
        self.max_price_increase = 0.05
        self.price_decrease_percentage = 0.01
        self.max_price_decrease = 0.05
        self.no_purchase_counter = 0

    def adjust_price(self, competitor_prices):
        if self.demand_level == "High" and self.price_increase_percentage < self.max_price_increase:
            next_price = self.current_price + self.current_price * self.price_increase_percentage
            if next_price <= self.base_price * (1 + self.max_price_increase):
                self.current_price = next_price
                self.price_increase_percentage = min(self.price_increase_percentage + 0.001, self.max_price_increase)
        elif self.demand_level == "Low" and self.price_decrease_percentage < self.max_price_decrease:
            next_price = self.current_price - self.current_price * self.price_decrease_percentage
            self.current_price = max(next_price, self.base_price * (1 - self.max_price_decrease))
            self.price_decrease_percentage = min(self.price_decrease_percentage + 0.001, self.max_price_decrease)

        avg_competitor_price = sum(competitor_prices) / len(competitor_prices)
        price_difference = self.current_price - avg_competitor_price
        adjustment_factor = 0.1
        adjusted_price = self.current_price - adjustment_factor * price_difference
        self.current_price = max(adjusted_price, 0.01)

class DynamicPricingSystem:
    def __init__(self, products):
        self.products = products

    def update_prices(self):
        for product in self.products:
            product.adjust_price(product.competitor_prices)

# Example Usage:
product1 = Product(base_price=50)
product2 = Product(base_price=100)
product1.competitor_prices = [45, 48, 52, 47, 50]
product2.competitor_prices = [90, 95, 105, 98, 100]
dynamic_pricing_system = DynamicPricingSystem(products=[product1, product2])

while True:
    dynamic_pricing_system.update_prices()
    print(f"Price of Prod 1: {product1.current_price}")
    print(f"Price of Prod 2: {product2.current_price}")

    print("Which prod do you want to buy? (Enter choice 1 or 2, or 3 to exit): ")
    choice = input()

    if choice == "3":
        print("Exiting the program. Thank you!")
        break
    elif choice == "1" or choice == "2":
        product = product1 if choice == "1" else product2
        print(f"Prod bought! Thank you for shopping with us.")
        product.purchase_counter += 1
        product.no_purchase_counter = 0

        if product.purchase_counter >= 3:
            current_time = time.time()
            time_difference = current_time - getattr(product, 'last_purchase_time', 0)
            
            if time_difference < 60 * 10:
                product.demand_level = "High"
            else:
                product.demand_level = "Normal"
                product.price_increase_percentage = 0.01
                
            product.last_purchase_time = current_time

        print(f"Adjusted Price for Prod {choice}: {product.current_price}")
        print(f"Current Demand Level for Prod {choice}: {product.demand_level}")
        print("------")
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

    # Simulate no purchase scenario
    for product in [product1, product2]:
        if product.purchase_counter == 0:
            product.no_purchase_counter += 1
            if product.no_purchase_counter >= 3 and product.demand_level == "Normal":
                product.demand_level = "Low"
                product.price_decrease_percentage = 0.01
