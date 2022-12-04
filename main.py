
import store
import visualize
import model


# print(model.optimal_for(150))

#For context, Starbucks regular coffee is ~0.13$/oz
s = store.Store(drink_price=.258, num_employees=1, expected_daily=250)
#Simulate 50 days
s.simulate(100)

visualize.run()

