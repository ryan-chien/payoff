from ortools.linear_solver import pywraplp
import numpy as np

# Declare variables
num_loans = 4   # 4 separate loans
term_months = 120   # ten-year loan term
principal = np.zeros(shape=(num_loans, term_months), dtype="float")
principal_initial = [20000, 17500, 15000, 12500]   # starting principal at time 0
principal[0:, 0] = principal_initial
rate_yearly = np.array([0.01, 0.05, 0.10, 0.15], dtype="float")   # interest rate is fixed
rate_monthly = rate_yearly / 12
decision_min = np.zeros(shape=(num_loans, term_months), dtype="float")   # minimum payment
decision_min_initial = [200, 175, 150, 125]   # starting minimum payment at time 0
decision_min[0:, 0] = decision_min_initial
budget = 1200   # maximum payment possible per time period

# Declare solver
solver = pywraplp.Solver("payoff", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# Declare objective
objective = solver.Objective()
objective.SetMinimization
decision = \
    np.array(
        [[solver.NumVar(0, solver.infinity(), 'd_i'+str(i)+'_j_'+str(j))
            for j in range(0, num_loans)]
            for i in range(0, term_months)])

# Set constraints
constraint_payoff = \
    solver.Add(
        sum(principal_initial)
        + sum(np.dot(rate_monthly, principal))
        - sum(decision.flatten())
        == 0)
