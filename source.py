# Import libraries -------------------
import sys
sys.path.append("C:/gitrepo/or-tools")
from ortools.linear_solver import pywraplp
import numpy as np

# Declare variables -------------------
num_loans = 4   # 4 separate loans
term_months = 36   # three-year loan term
rate_yearly = np.array([0.01, 0.05, 0.10, 0.15], dtype="float")   # interest rate is fixed
rate_monthly = rate_yearly / 12
decision_min = [200, 175, 150, 125]   # minimum payment per term
principal_initial = [20000, 17500, 15000, 12500]   # starting principal at time 0
budget = 3250   # maximum payment possible per time period

# Declare solver ---------------------------
solver = pywraplp.Solver("payoff", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# Declare objective -----------------------------------
objective = solver.Objective()
# objective.SetMinimization
decision = \
    np.array(
        [[solver.NumVar(0, solver.infinity(), 'd_i'+str(i)+'_t_'+str(t))
            for t in range(0, term_months)]
            for i in range(0, num_loans)])

principal = \
    np.array(
        [[solver.NumVar(0, solver.infinity(), 'p_i'+str(i)+'_t_'+str(t))
            for t in range(0, term_months)]
            for i in range(0, num_loans)])

solver.Minimize(
    sum(
        sum(decision[i,:]) for i in range(0, num_loans)))

# Set constraints ---------------------------------------
## Starting principal is nonzero
constraint_principal_init = [solver.Constraint(principal_initial[i], principal_initial[i]) for i in range(0, num_loans)]
for i in range(0, num_loans):
    constraint_principal_init[i].SetCoefficient(principal[i,0], 1)

## Principal is zero at end of term
constraint_payoff_tmax = \
    np.array([solver.Add(principal[i, term_months-1] <= 0) for i in range(0, num_loans)])

## Principal in each period is equal to principal of previous period, interest, and payment
constraint_principal_rolling = \
    np.array(
        [[solver.Add(
            (principal[i, t] == (1+rate_monthly[i]) * principal[i, t-1] - decision[i, t-1]))
            for t in range(1, term_months)]
            for i in range(0, num_loans)])

## Sum of payments must not exceed budget
constraint_budget = \
    np.array([
        solver.Add(
            sum(decision[0:, t]) <= budget) for t in range(0, term_months)])

## Montly payment must meet minimum
constraint_min_payment = \
    np.array(
        [[solver.Add(
            decision[i,t] >= decision_min[i])
            for t in range(0, term_months)]
            for i in range(0, num_loans)])

# Solve ----------------------
status = solver.Solve()
decision_solution = np.array([[decision[i,t].solution_value() for t in range(0, term_months)] for i in range(0, num_loans)])
print(decision_solution)
payments = np.array([sum(decision_solution[:,t]) for t in range(0, term_months)])
print(payments)
principal_solution = np.array([[principal[i,t].solution_value() for t in range(0, term_months)] for i in range(0, num_loans)])
print(principal_solution)
solver.Objective().Value()

# Lp file ----------------------
solver_debug_file = solver.ExportModelAsLpFormat(False)
f = open('debug.txt', 'a')
f.write(solver_debug_file)
f.close()