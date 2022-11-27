
import numpy as np


class Order:
    """A class to hold information about an order."""
    def __init__( \
            self, milk_price_cup: float, coffee_price_g: float, \
            sugar_price_g: float, drink_size_oz: float, drink_price: float \
        ) -> None:
        
        # ~1.5g coffee per oz of drink
        self.coffee_used_g = max(0, np.random.normal(loc=1.5, scale=0.13)) * drink_size_oz

        # ~1g sugar per oz of drink 
        self.sugar_used_g = max(0, np.random.normal(loc=1, scale=0.25)) * drink_size_oz

        # ~.16c milk per oz of drink
        self.milk_used_c = max(0, np.random.normal(loc=0.16, scale=0.04)) * drink_size_oz

        self.drink_price = drink_price
        self.drink_size_oz = drink_size_oz





