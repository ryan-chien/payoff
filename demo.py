import sys
sys.path.append("C:/gitrepo/payoff/")
from source import *
import matplotlib.pyplot as plt

interest_cost = []
for budget_rate in range(1200, 2200, 10):
    interest_cost.append(opt_pay_schedule(budget=budget_rate))

print(interest_cost)

plt.plot(list(range(1200, 2200, 10)), interest_cost)
plt.axhline(10000, color='r', linestyle='.')
plt.xlabel('Budget')
plt.ylabel('Interest Cost Total')
plt.show()
