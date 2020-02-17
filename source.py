# Import libraries -------------------
import sys
sys.path.append("C:/gitrepo/or-tools")
from ortools.linear_solver import pywraplp
import numpy as np

# Declare variables -------------------
num_loans = 4   # 4 separate loans
term_months = 120   # ten-year loan term
rate_yearly = np.array([0.01, 0.05, 0.10, 0.15], dtype="float")   # interest rate is fixed
rate_monthly = rate_yearly / 12
decision_min = np.zeros(shape=(num_loans, term_months), dtype="float")   # minimum payment
decision_min_initial = [200, 175, 150, 125]   # starting minimum payment at time 0
decision_min[0:, 0] = decision_min_initial
budget = 1200   # maximum payment possible per time period

# Declare solver ---------------------------
solver = pywraplp.Solver("payoff", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# Declare objective -----------------------------------
objective = solver.Objective()
objective.SetMinimization
decision = \
    np.array(
        [[solver.NumVar(0, solver.infinity(), 'd_i'+str(i)+'_i_'+str(t))
            for t in range(0, term_months)]
            for i in range(0, num_loans)])

principal = \
    np.array(
        [[solver.NumVar(0, solver.infinity(), 'p_i'+str(i)+'_i_'+str(t))
            for t in range(0, term_months)]
            for i in range(0, num_loans)])

# Set constraints ---------------------------------------
## Starting principal is nonzero
principal_initial = [20000, 17500, 15000, 12500]   # starting principal at time 0
constraint_principal_init = [solver.Constraint(principal_initial[i], principal_initial[i]) for i in range(0, num_loans)]
for i in range(0, num_loans):
    constraint_principal_init[i].SetCoefficient(principal[i,0], 1)

## Principal is zero at end of term
constraint_payoff_tmax = solver.Constraint(0, 0)
constraint_payoff_tmax.SetCoefficient(decision[0, term_months-1], 1)

## Principal in each period is equal to principal of previous period, interest, and payment
constraint_principal_rolling = \
    np.array(
        [[solver.Add(
            (principal[i, t] == (1+rate_monthly[i]) * principal[i, t-1] - decision[i, t-1]))
            for t in range(1, term_months-1)]
            for i in range(0, num_loans)])
            
# Solve ----------------------
status = solver.Solve()
decision_solution = [[decision[i,t].solution_value() for t in range(0, term_months)] for i in range(0, num_loans)]
principal_solution = [[principal[i,t].solution_value() for t in range(0, term_months)] for i in range(0, num_loans)]
solver_debug_file = solver.ExportModelAsLpFormat(False)