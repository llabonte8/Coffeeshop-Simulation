
import numpy as np
import math 

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
        #Limit the price to mean/1.5 <= price <= mean*1.5
        self.price = max(self.mean_price / 1.5, self.price)
        self.price = min(self.mean_price * 1.5, self.price)

        #Drift is set to the distance between the mean and current price, 
        #then scaled with the volatility so the change is not too drastic
        self.drift = (self.mean_price - self.price) * self.volatility * 0.6
        return self.price







