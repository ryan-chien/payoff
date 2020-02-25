# Import
import sys
sys.path.append("C:/gitrepo/payoff/")
from source import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools

# Generate solutions
start_budget = 1000
end_budget = 2500
interest_cost = []
payment_schedule = []
for budget_rate in range(start_budget, end_budget, 100):
    _solution = \
        opt_pay_schedule(
            term_months=[60, 120, 100, 100],
            principal_initial=[9871.59, 11040.71, 20879.70, 15600.74],
            rate_yearly=[0.0531, 0.10, 0.0584, 0.10],
            decision_min=[86.12, 70.54, 186.60, 204.72],
            budget=budget_rate)
    interest_cost.append(_solution[0])
    payment_schedule.append(_solution[1])
    del(_solution)

# Plot budget vs total cost of interest
plt.plot(list(range(start_budget, end_budget, 100)), interest_cost)
plt.axvline(1800, color='r', linestyle='dashed')
plt.xlabel('Budget')
plt.ylabel('Interest Cost Total')
plt.show()

# Print payment schedule for $1800 budget
paysched = pd.DataFrame(__ for __ in itertools.zip_longest(*payment_schedule[9])).transpose()
print(paysched)

# Plot payment schedule for $1800 budget
plt.plot(np.transpose(np.array(paysched)))
plt.show()