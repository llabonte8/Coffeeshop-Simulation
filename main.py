
import store
import visualize
import model


print(model.optimal_for(300))

#For context, Starbucks regular coffee is ~0.13$/oz
s = store.Store(drink_price=.26, num_employees=2, expected_daily=500)
#Simulate 50 days
s.simulate(100)

visualize.run()

