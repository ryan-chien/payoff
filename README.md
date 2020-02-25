# Payoff: Optimal Loan Payoff Calculator

## Background
Payoff is a mixed integer linear program (MILP) that minimizes the total interest cost of a loan by optimizing the payoff schedule. In other words, ***payoff answers, "How much should I pay each loan each month, given a budget and minimum payments?***

First, payoff takes the following as inputs:
```
1. The term of each loan in months (1xN int array),
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

## Mathematical Formulation
The following system of equations defines the MILP.

Objective:

![min\sum_{i=0}^{N}\sum_{t=0}^{Z}D_i,_t + M_i,_t](https://render.githubusercontent.com/render/math?math=min%5Csum_%7Bi%3D0%7D%5E%7BN%7D%5Csum_%7Bt%3D0%7D%5E%7BZ%7DD_i%2C_t%20%2B%20M_i%2C_t)

Subject To:

(1)   ![P_i,_0 = P^*](https://render.githubusercontent.com/render/math?math=P_i%2C_0%20%3D%20P%5E*)

(2)   ![P_i,_Z=0 \forall i](https://render.githubusercontent.com/render/math?math=P_i%2C_Z%3D0%20%5Cforall%20i)

(3)   ![P_i,_t = (1+\frac{1}{12}R_i)P_i,_{t-1} - D_i,_{t-1}\forall i,t](https://render.githubusercontent.com/render/math?math=P_i%2C_t%20%3D%20(1%2B%5Cfrac%7B1%7D%7B12%7DR_i)P_i%2C_%7Bt-1%7D%20-%20D_i%2C_%7Bt-1%7D%5Cforall%20i%2Ct)

(4)   ![\sum_{i=0}^{N}D_i,_t \leq B \forall t](https://render.githubusercontent.com/render/math?math=%5Csum_%7Bi%3D0%7D%5E%7BN%7DD_i%2C_t%20%5Cleq%20B%20%5Cforall%20t)

(5)   ![M_i,_t \geq \frac{P_i,_t}{P_i,_0} \forall i,t](https://render.githubusercontent.com/render/math?math=M_i%2C_t%20%5Cgeq%20%5Cfrac%7BP_i%2C_t%7D%7BP_i%2C_0%7D%20%5Cforall%20i%2Ct)

(6)   ![D_i,_t \geq F_iM_i,_t \forall i,t](https://render.githubusercontent.com/render/math?math=D_i%2C_t%20%5Cgeq%20F_iM_i%2C_t%20%5Cforall%20i%2Ct)

Where D is the payment decision variable, M is a binary 'remnant' variable which is zero if the loan is paid off, P is the principal, P* is the starting principal, R is the yearly interest rate, B is the budget (i.e. maximum monthly payment), and F is the minimum monthly payment. The loan index ranges from i=0 to N, and the time-period index ranges from t=0 to Z.

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
...         term_months=[80, 120, 100, 100],
...         principal_initial=[9871.59, 11040.71, 20879.70, 19940.74],
...         rate_yearly=[0.0531, 0.0631, 0.0584, 0.0684],   
...         decision_min=[86.12, 70.54, 186.60, 204.72],  
...         budget=1800)
Optimal payoff interest cost = 6055.7417295947525
```


```{python}
import pandas as pd
import itertools
paysched = pd.DataFrame(__ for __ in itertools.zip_longest(*optimal_schedule[1])).transpose()

>>> print(paysched[list(range(0,20))])
        0        1        2        3        4        5        6        7        8        9        10       11       12       13           14       15       16       17       18       19
0    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.120000    86.12    86.12    86.12    86.12    86.12
1    70.54    70.54    70.54    70.54    70.54    70.54    70.54    70.54    70.54    70.54    70.54    70.54    70.54    70.54  1099.997247  1527.28  1527.28  1527.28  1527.28  1527.28
2   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.60   186.600000   186.60   186.60   186.60   186.60   186.60
3  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74  1456.74   427.282753     0.00     0.00     0.00     0.00     0.00

>>> print(paysched[list(range(20,40))])
        20          21       22       23       24       25       26       27       28       29       30       31           32      33      34      35      36          37   38   39
0    86.12   86.120000    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12    86.12   169.826579  1800.0  1800.0  1800.0  1800.0  1188.48173  0.0  0.0
1  1527.28  850.216092     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.000000     0.0     0.0     0.0     0.0     0.00000  0.0  0.0
2   186.60  863.663908  1713.88  1713.88  1713.88  1713.88  1713.88  1713.88  1713.88  1713.88  1713.88  1713.88  1630.173421     0.0     0.0     0.0     0.0     0.00000  0.0  0.0
3     0.00    0.000000     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.000000     0.0     0.0     0.0     0.0     0.00000  0.0  0.0

>>> print(paysched[list(range(40,60))])
    40   41   42   43   44   45   46   47   48   49   50   51   52   53   54   55   56   57   58   59
0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
2  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
3  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0

```
Note: the matrix columns represents the time period (month), and the rows represents the loan index. Each cell-value represents the optimal payment amount.