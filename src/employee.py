
import numpy

"""
This class, for all intents and purposes, is a timer. That is it. 

When we accept an order, the timer is set to a random normal value centered at 90 seconds. 
To decrement the timer, the 'update' method is called, and the timer is reduced by however many 
seconds have passed. 
Once the timer hits zero, the employee is free to make another drink. 
"""


class Employee:
    def __init__(self) -> None:
        self.seconds_until_free: float = 0
        self.median_drink_time_seconds: float = 90


    def accept_order(self):
        """Accept an order and have the employee begin working"""
        self.seconds_until_free = numpy.random.normal(loc=self.median_drink_time_seconds, scale=0.3)


    def update(self, elapsed_seconds: float): 
        """Decrement the amount of time needed to finish the order"""
        self.seconds_until_free -= elapsed_seconds

    def is_free(self) -> bool:
        return self.seconds_until_free <= 0







