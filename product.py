
import numpy as np
import math 


"""
This class provides the code to simulate random market prices. 
The class is given a volatility (how large the random movement can be) 
and mean price (the median line that the price will generally adhere to). 
Genuine randomness would not suit our purposes here, which is why 
we're not using geometric brownian motion. The overview for generating prices is as follows:
    1) Add a random movement to the current price (sample from a normal distribution)
"""

class Product:
    """Class to simulate the market price of a product"""
    def __init__(self, volatility: float, mean_price: float) -> None:
        self.volatility: float = volatility
        self.mean_price: float = mean_price
        #Drift is used in case the price strays too far from the median, so we
        #can 'drift' it back towards the center line
        self.drift: float = 0
        #The price should just start at the mean
        self.price = mean_price

    def gen_price(self) -> float:
        #Add a random increase or decrease to the price
        self.price += np.random.normal(0, self.volatility) + self.drift

        #Drift is set to the distance between the mean and current price, 
        #then scaled with the volatility so the change is not too drastic
        self.drift = (self.mean_price - self.price) * 0.05
        return self.price







