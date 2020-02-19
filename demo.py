# Import
import sys
sys.path.append("C:/gitrepo/payoff/")
from source import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Generate solutions
interest_cost = []
payment_schedule = []
for budget_rate in range(1200, 2500, 100):
    _solution = opt_pay_schedule(budget=budget_rate)
    interest_cost.append(_solution[0])
    payment_schedule.append(_solution[1])
    del(_solution)

# Plot budget vs total cost of interest
plt.plot(list(range(1200, 2500, 100)), interest_cost)
plt.axvline(1800, color='r', linestyle='dashed')
plt.xlabel('Budget')
plt.ylabel('Interest Cost Total')
plt.show()

# Print payment schedule for $1800 budget
paysched = pd.DataFrame(payment_schedule[6])
print(paysched)

# Plot payment schedule for $1800 budget
plt.plot(np.transpose(np.array(paysched)))
plt.show()
