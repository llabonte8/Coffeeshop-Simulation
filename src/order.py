
import numpy as np

"""
The entire purpose of this class is just to hold information regarding an order. 
In theory, we could just use a tuple or something, but for the sake of 
readability and scalability I think it is best to use a class. 
There is not much explaining to do here -- it should be fairly self-explanatory.
"""

class Order:
    """A class to hold information about an order."""
    def __init__(self, drink_size_oz: float, drink_price: float) -> None:
        
        # ~1.5g coffee per oz of drink
        self.coffee_used_g = max(0, np.random.normal(loc=1.5, scale=0.13)) * drink_size_oz

        # ~1g sugar per oz of drink 
        self.sugar_used_g = max(0, np.random.normal(loc=1, scale=0.25)) * drink_size_oz

        # ~.16c milk per oz of drink
        self.milk_used_c = max(0, np.random.normal(loc=0.16, scale=0.04)) * drink_size_oz

        self.drink_price = drink_price
        self.drink_size_oz = drink_size_oz





