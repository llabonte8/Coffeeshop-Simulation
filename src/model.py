
import math
from logger import Logger
from store import Store
import os 


c_dir = os.path.dirname(__file__)

class Model:
    def __init__(self, expected_daily) -> None:

        # Initialize all constant variables. These should not need to chance.
        self.employee_throughput = 3600 / 90
        mean_visiting_hour = 2.5 
        expected_daily_customers = expected_daily
        self.hourly_customers = [(mean_visiting_hour ** x * math.exp(-mean_visiting_hour)) / math.factorial(x) * expected_daily_customers for x in range(8)]
        self.drink_size_oz = 16
        self.goods_cost = self.drink_size_oz * (1.5 * 0.04 + 1 * 0.002 + .16 * .18)
        

    def simulate(self, drink_price, employee_num) -> float:
        '''
            Calculate the revenue generated over the course of a day given drink price and the number of employees.
            The idea here is fairly simple -- it is essentially a deterministic version of the core of the agent-based simulation.
            While not exact, due to the determinism, it is pretty close to the actual results. 
        '''
        revenue: float = 0
            
        # Run simulation 
        for h in self.hourly_customers:
            l = lambda x, k, m: 1.0 / (1.0 + math.exp(k * (x - m)))

            percent_of_total = l(drink_price, 20, 0.3)
            n_customers = min(percent_of_total, (self.employee_throughput * employee_num) / h) * h

            revenue += ((n_customers * drink_price * self.drink_size_oz) - (self.goods_cost * n_customers) - (employee_num * 14.25))

        return revenue

    def run(self) -> tuple:
        '''
            Find the best combination of drink price and number of employees. 
            Finding the maximium of the function analytically is difficult (I tried). 
            However, finding the *bounds* of the inputs of the function is not quite as hard.
            Therefore, we just search through the entire domain of the function and find the maximum. 
            Yes, it is a brute-force approach, but given the relatively small domain size, its probably faster than other solutions.
        '''
        #How much we should increase the price for each iteration
        p_inc = 0.001
        #Minimum price
        p_min = 0.00
        #Maximum price
        p_max = 0.99
        #How much we should increase employee cost each iteration
        e_inc = 1
        # Minimum employees
        e_min = 1
        # Maximum employees
        e_max = 40

        best_price = 0
        best_e = 0
        max_rev = 0


        # Search through all combinations of price and employees and return the best one
        p = p_min
        while p < p_max:
            e = e_min
            while e < e_max:

                r = self.simulate(p, e)
                if r > max_rev:
                    best_price = p
                    best_e = e
                    max_rev = r

                e += e_inc

            p += p_inc

        return(best_price, best_e)


def gen_data():
    l = Logger(['Price per Ounce', 'Number of Employees', 'Daily Customers'])
    for x in range(300, 600, 25):
        m = Model(x)
        price, e_num = m.run()
        l.add_data('Price per Ounce', price)
        l.add_data('Number of Employees', e_num)
        l.add_data('Daily Customers', x)
    l.write(os.path.join(c_dir, '../data/optimize.csv'))

def optimal_for(expected_daily: int) -> tuple:
    return Model(expected_daily).run()


def test_model():
    l = Logger(['Functional Revenue', 'Agent Revenue', 'Drink Price'])
    m = Model(150)
    s = Store(0, 1, 150)

    x = 0.06
    while x < 0.5:
        l.add_data('Functional Revenue', m.simulate(x, 1))
        s.drink_price_oz = x 
        l.add_data('Agent Revenue', s.simulate(1, '', False))
        l.add_data('Drink Price', x)
        x += 0.01
    l.write(os.path.join(c_dir, '../data/test_model.csv'))

