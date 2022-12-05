from math import exp, factorial
from order import Order
import random

'''
The two functions here do distinctly different things. 
    1) timestep_spawn_chance
        This is the chance that a customer will come during some given timestep. 
        It will be less than 1. The probability is decided by a poisson distribution,
        but it is used in a discrete, not continuous, way. (We are using the height of the function,
        not the area up to some point). We use a poisson distribution because it is close to the 
        shape of the function giving how many customers show up per hour. (Go on google maps 
        and find a Dunkin Donuts, then look at the graph of busy times).
        The function itself contains more information on the math and values used. 

    2) will_spawn
        This is the chance that a customer will come, given by a boolean. As opposed to the first function,
        there is no range of possibility -- it is just a yes or no.
        The probability that of a customer coming is decided by two things: 
            a) The length of the queue
            b) The price per ounce of the drink 
        These probabilities are decided by a logistic curve (google logistic decay to get an idea 
        of what that is) where as the price or length increase, the chance the customer will come decreases. 
        These two probabilities are calculated separately, then multiplied together to get a final probability.
        This probability will be somewhere between 0 and 1. We then generate a random number and, if it is less
        than or equal to the probability, we spawn a customer. 
        For example, if the probability is 0.5, about 50% of random number will be <= the probability. Therefore, 
        we will return True ~50% of the time. 
        More details as to the math and values used are documented in the function itself.
'''


def timestep_spawn_chance (
        mean_visiting_hour: float, curr_hour: int, expected_daily_customers: int, timesteps_per_hour: int, \
    ) -> float:
    """Calculate the probability a customer will show up during this timestep"""

    # The function here is (m^x * e^-m) / (x!), or a poisson distribution. 
    # The shape of the function is close to how many customers should show up hourly.
    # This calculates the percentage of total customers that should come during a given hour.
    poisson = (mean_visiting_hour ** curr_hour * exp(-mean_visiting_hour)) / factorial(curr_hour)

    # We have the percentage of total customers that should come during a given hour. 
    # From there, we calculate how many customers that is (poisson * expected_daily_customers)
    # and then divide it by the number of timesteps per hour to get the expected number of customers per timestep
    return (poisson * expected_daily_customers) / timesteps_per_hour

def will_spawn (
        queue_len: int, order: Order, 
    ) -> bool:
    """Calculate the probability a customer will show up given the queue length and drink price"""
    m: float = 0.3 
    k: float = 20 
    p: float = order.drink_price / order.drink_size_oz

    # 1.0 / (1.0 + e ^ (k (p - m)))
    # k = curve steepness, m = median point, p = price per oz

    # Essentially saying a customer will buy a drink at 30c/oz 50% of the time
    # That equates to buying a 6$ large coffee 50% of the time
    prob = 1.0 / (1.0 + exp(k * (p - m)))

    
    m = 5.5 
    k = 2.25
    p = queue_len
    # Same equation as above, p is now the number of people in line 
    prob *= 1.0 / (1.0 + exp(k * (p - m)))
    
    return random.random() <= prob


