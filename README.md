# Payoff: Optimal Loan Payoff Calculator

## Background
Payoff is a mixed integer linear program that minimizes the total interest cost of a loan by optimizing the payoff schedule. In other words, payoff answers, "How much should I pay each loan each month, given a budget and minimum payments?

First, payoff takes the following as inputs:
```
1. The homogenous term of all loans (integer),
2. Starting principal loan amounts (1xN float array)
3. Yearly loan interest rates (1xN float array),
4. Minimum monthly payments by loan (1xN float array),
4. Budget (float)
```
Then, payoff returns the following:
```
1. The total interest cost given the optimal payment schedule (float),
2. The payment schedule (NxT array where T is the homogenous term length)
```

## Dependencies
Payoff is dependent on the following Python libraries:
```
  1. ortools (https://developers.google.com/optimization/install)
  2. numpy
```

Nice to haves are:
```
  3. pandas
  4. matplotlib
```

## Example
```{python}
import sys
sys.path.append("C:/gitrepo/payoff/")
from source import *
>>> optimal_schedule = \
...     opt_pay_schedule(
...         term_months = 60,
...         principal_initial=[9871.59, 11040.71, 20879.70, 15600.74],
...         rate_yearly=[0.0531, 0.10, 0.0584, 0.10],
...         decision_min=[86.12, 70.54, 186.60, 204.72],
...         budget=1500)
Optimal payoff interest cost = 7501.183628129096
```

```{python}
>>> print(optimal_schedule[0])   # print total interest cost given optimal schedule
7501.183628129096
```

```{python}
import pandas as pd
>>> print(pd.DataFrame(optimal_schedule[1])[list(range(0, 12))])
           0        1        2        3        4        5        6        7        8        9        10       11
0   86.120000    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12
1  427.232604  1022.56  1022.56  1022.56  1022.56  1022.56  1022.56  1022.56  1022.56  1022.56  1022.56  1022.56
2  186.600000   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60
3  800.047396   204.72   204.72   204.72   204.72   204.72   204.72   204.72   204.72   204.72   204.72   204.72
[4 rows x 60 columns]

>>> print(pd.DataFrame(optimal_schedule[1])[list(range(12, 24))])
        12       13       14       15       16       17       18       19       20       21       22          23
0    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12000
1     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00000
2   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   334.41361
3  1227.28  1227.28  1227.28  1227.28  1227.28  1227.28  1227.28  1227.28  1227.28  1227.28  1227.28  1079.46639

>>> print(pd.DataFrame(optimal_schedule[1])[list(range(24, 36))])
        24       25       26       27       28       29       30       31       32       33       34       35
0    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12
1     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00
2  1209.16  1413.88  1413.88  1413.88  1413.88  1413.88  1413.88  1413.88  1413.88  1413.88  1413.88  1413.88
3   204.72     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00

>>> print(pd.DataFrame(optimal_schedule[1])[list(range(36, 48))])
        36           37      38      39      40      41      42          43   44   45   46   47
0    86.12   420.670798  1500.0  1500.0  1500.0  1500.0  1500.0  393.923628  0.0  0.0  0.0  0.0
1     0.00     0.000000     0.0     0.0     0.0     0.0     0.0    0.000000  0.0  0.0  0.0  0.0
2  1413.88  1079.329202     0.0     0.0     0.0     0.0     0.0    0.000000  0.0  0.0  0.0  0.0
3     0.00     0.000000     0.0     0.0     0.0     0.0     0.0    0.000000  0.0  0.0  0.0  0.0
```
Note: the x-axis represents the time period (month), and the y-axis represents the loan index. Each cell-value represents the optimal payment amount.

## Formulation
Objective:
![min\sum_{i=0}^{N}\sum_{t=0}^{Z}D_i,_t + M_i,_t](https://render.githubusercontent.com/render/math?math=min%5Csum_%7Bi%3D0%7D%5E%7BN%7D%5Csum_%7Bt%3D0%7D%5E%7BZ%7DD_i%2C_t%20%2B%20M_i%2C_t)

Subject To:
![P_i,_0 = P^*](https://render.githubusercontent.com/render/math?math=P_i%2C_0%20%3D%20P%5E*)

![P_i,_Z=0 \forall i](https://render.githubusercontent.com/render/math?math=P_i%2C_Z%3D0%20%5Cforall%20i)

![P_i,_t = (1+\frac{1}{12}R_i)P_i,_{t-1} - D_i,_{t-1}\forall i,t](https://render.githubusercontent.com/render/math?math=P_i%2C_t%20%3D%20(1%2B%5Cfrac%7B1%7D%7B12%7DR_i)P_i%2C_%7Bt-1%7D%20-%20D_i%2C_%7Bt-1%7D%5Cforall%20i%2Ct)

![\sum_{i=0}^{N}D_i,_t \leq B \forall t](https://render.githubusercontent.com/render/math?math=%5Csum_%7Bi%3D0%7D%5E%7BN%7DD_i%2C_t%20%5Cleq%20B%20%5Cforall%20t)

![M_i,_t \geq \frac{P_i,_t}{P_i,_0} \forall i,t](https://render.githubusercontent.com/render/math?math=M_i%2C_t%20%5Cgeq%20%5Cfrac%7BP_i%2C_t%7D%7BP_i%2C_0%7D%20%5Cforall%20i%2Ct)

![D_i,_t \geq F_iM_i,_t \forall i,t](https://render.githubusercontent.com/render/math?math=D_i%2C_t%20%5Cgeq%20F_iM_i%2C_t%20%5Cforall%20i%2Ct)

Where D is the payment decision variable, M is a binary 'remnant' variable which is zero if the loan is paid off, P is the principal, R is the yearly interest, B is the budget (i.e. maximum monthly payment), and F is the minimum monthly payment.