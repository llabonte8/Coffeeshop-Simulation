
import store
import visualize


s = store.Store()
#Simulate 50 days
s.simulate(150)

visualize.run()

