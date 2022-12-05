
import numpy as np
from employee import Employee
import customer
from order import Order
from logger import Logger
from product import Product


"""
This is the main driver for the simulation. The amount of state 
variables may make things a little difficult to follow, so I'll provide 
a more general overview. 

The idea is to break a day into some amount of timesteps, controlled by the 'seconds_per_timestep' variable. 
Basically all timing is based on this value. Then, we advance the simulation on each timestep and record
the results. 

The simulation loop is as follows: 
    1) Initialize state variables (things like the price of goods and the number of customers)
    2) Loop through all the timesteps for one day
        a) Update the employees (see employee.py for more info as to what that means)
        b) If there are free employees, and orders in the queue, assign an employee with an order 
        c) Calculate the chance that a customer will arrive 
            i) Depends on the likelyhood of a customer showing up that hour, 
                the length of the queue, and the price of the drinks 
        d) If a customer arrives, choose an order for them and add it to the queue 
    3) Save any statistics generated
    4) Repeat for however many days we are simulating

"""


class Store:
    def __init__(self, drink_price: float, num_employees: int, expected_daily: int) -> None:

        if num_employees < 1: raise Exception("Number of employees must be >= 1")

        self.logger = Logger([
            "Average Hourly Customers",
            "Max Hourly Queue Length",
            "Total Daily Customers",
            "Daily Walkout Customers",
            "Market Milk Price",
            "Market Coffee Price",
            "Market Sugar Price", 
            "Daily Milk Cost",
            "Daily Coffee Cost", 
            "Daily Sugar Cost",
            "Daily Employee Cost",
            "Daily Walkout Customers",
            "Gross Daily Income",
            "Net Daily Income",
            "Gross Daily Expense",
        ])
        
        # How many customers we expect, total
        self.expected_daily_customers: int = expected_daily
        # The hour where the most customers should show up
        self.mean_visiting_hour: float = 2.5

        self.employees: list[Employee] = [Employee() for _ in range(num_employees)]
        self.queue: list[Order] = []

        #~18c per cup of milk 
        self.milk = Product(0.003, 0.18)
        #~4c per gram of roast coffee
        self.coffee = Product(0.002, 0.04)
        #.2c per gram of sugar 
        self.sugar = Product(0.0002, 0.002)

        #Drink prize per oz 
        self.drink_price_oz: float = drink_price
        
        self.seconds_per_timestep: int = 10
        self.timesteps_per_hour: int = (int)(60 * 60 / self.seconds_per_timestep)
        self.hours_per_day: int = 8

        self.daily_revenue: float = 0

        self.avg_hourly_customers: list[float] = [0] * self.hours_per_day
        self.avg_hourly_queue: list[float] = [0] * self.hours_per_day
       
    def simulate(self, num_days: int, log: bool = True, write_fname: str = 'output.csv') -> float:
        """Simulate a given number of days and return total revenue"""

        income: float = 0

        for _ in range(num_days):
            self.simulate_day()
            income += self.daily_revenue

        # This is an average, so it should be scaled by the number of days simulated
        self.avg_hourly_customers = [x / num_days for x in self.avg_hourly_customers]
        self.avg_hourly_queue = [x / num_days for x in self.avg_hourly_queue]
        for x in self.avg_hourly_customers: self.logger.add_data("Average Hourly Customers", x)
        for x in self.avg_hourly_queue: self.logger.add_data("Max Hourly Queue Length", x)

        if log: self.logger.write(write_fname)

        return income

    def simulate_day(self) -> None:
        """Simulate a single day"""

        total_timesteps: int = self.timesteps_per_hour * self.hours_per_day
        curr_hour: int = 0
        total_customers: int = 0
        total_walkouts: int = 0
        hourly_customers: float = 0
        hourly_queue: float = 0

        daily_milk_cost: float = 0
        daily_sugar_cost: float = 0 
        daily_coffee_cost: float = 0

        daily_total_expense: float = 0
        daily_total_income: float = 0


        milk_price = self.milk.gen_price()
        sugar_price = self.sugar.gen_price()
        coffee_price = self.coffee.gen_price()
        
        # This is the chance that a customer will come during a given timestep. 
        # The chance increases each time a timestep passes with no customer, 
        # until eventually a customer spawns. 
        chance_of_customer: float = 0

        #Loop through all timesteps
        for timestep in range(total_timesteps):

            hourly_queue += len(self.queue)

            #Loop through all employees and update them
            for employee in self.employees:
                employee.update(self.seconds_per_timestep)
                #If an employee is free, and there are drinks in the queue, have the employee make the drink
                if employee.is_free() and len(self.queue) > 0:
                    employee.accept_order()
                    
                    #The order being made
                    order = self.queue[0]
                    
                    #Add the expenses and revenue from the order
                    daily_milk_cost += order.milk_used_c * milk_price
                    daily_coffee_cost += order.coffee_used_g * coffee_price
                    daily_sugar_cost += order.sugar_used_g * sugar_price
                    daily_total_income += order.drink_price

                    # Remove the order from the list
                    self.queue.pop(0)

            #Calculate the chance that a customer will come during this timestep
            chance_of_customer += customer.timestep_spawn_chance(self.mean_visiting_hour, curr_hour, \
                    self.expected_daily_customers, self.timesteps_per_hour)
            #If the expected customers this timestep is > 1
            if chance_of_customer >= 1:
                # Reduce the chance back to where it was
                chance_of_customer -= 1
                
                # Create a random order from the list of options with average drink size = 16oz
                drink_size = np.random.normal(loc=16, scale=2)
                drink_cost = drink_size * self.drink_price_oz
                random_order = Order(drink_size, drink_cost)

                # Given the length of the queue and price of the drink, see if the customer will stay
                if customer.will_spawn(len(self.queue), random_order):
                    total_customers += 1 
                    hourly_customers += 1
                    # Add the customer's order to the queue
                    self.queue.append(random_order)

                else: total_walkouts += 1

            # If we are at an hour mark 
            if (timestep + 1) % self.timesteps_per_hour == 0: 
                # The hourly customers should be logged and then reset
                self.avg_hourly_customers[curr_hour] += hourly_customers
                self.avg_hourly_queue[curr_hour] += hourly_queue / self.timesteps_per_hour
                hourly_queue = 0
                hourly_customers = 0
                curr_hour += 1 
                tmp = 0


        # Min wage in MA is 14.25
        employee_cost = 14.25 * len(self.employees) * self.hours_per_day
        daily_total_expense = daily_milk_cost + daily_coffee_cost + daily_sugar_cost + employee_cost


        self.logger.add_data("Total Daily Customers", total_customers)
        self.logger.add_data("Daily Walkout Customers", total_walkouts)

        self.logger.add_data("Market Milk Price", milk_price)
        self.logger.add_data("Market Coffee Price", coffee_price)
        self.logger.add_data("Market Sugar Price", sugar_price)
        
        self.logger.add_data("Daily Milk Cost", daily_milk_cost)
        self.logger.add_data("Daily Coffee Cost", daily_coffee_cost)
        self.logger.add_data("Daily Sugar Cost", daily_sugar_cost)
        self.logger.add_data("Daily Employee Cost", employee_cost)

        self.logger.add_data("Gross Daily Income", daily_total_income)
        self.logger.add_data("Gross Daily Expense", daily_total_expense)
        self.logger.add_data("Net Daily Income", daily_total_income - daily_total_expense)
        self.daily_revenue = daily_total_income - daily_total_expense
