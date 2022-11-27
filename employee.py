
import numpy



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







