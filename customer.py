from math import exp, factorial
from order import Order
import random


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


