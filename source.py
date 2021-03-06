# Optimal Multi-Loan Payment Scheduler with Minimum Payment Constraints
# Ryan Chien
# 2/19/2020

# Main --------------------------
def opt_pay_schedule(
    term_months=[80, 120, 100, 100],                             # loan term in months
    principal_initial=[9871.59, 11040.71, 20879.70, 19940.74],   # starting principal at time 0
    rate_yearly=[0.0531, 0.0631, 0.0584, 0.0684],                # yearly interest rate
    decision_min=[86.12, 70.54, 186.60, 204.72],                 # minimum payment per term
    budget=1800,                                                 # maximum possible payment
    verbose=[True, 50]):   # If verbose is true, query solver for intermediate results for given time interval                                             
    
    # Import libraries -------------------
    import sys
    sys.path.append("C:/gitrepo/or-tools")
    from ortools.linear_solver import pywraplp
    import numpy as np

    # Declare variables -------------------
    rate_monthly = np.array(rate_yearly) / 12
    num_loans = principal_initial.__len__()
    max_term_months = max(term_months)

    # Declare solver ---------------------------
    try:
        solver = pywraplp.Solver("payoff", pywraplp.Solver.CPLEX_MIXED_INTEGER_PROGRAMMING)
    except:
        solver = pywraplp.Solver("payoff", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # If verbose is true, query solver for intermediate results ------------
    if verbose[0]==True:
        time_limit_milliseconds = verbose[1]
        solver.set_time_limit(time_limit_milliseconds)

    # Declare solver variables -----------------------------------
    ## Pyment is the decision variable
    decision = \
        np.array(
            [[solver.NumVar(0, solver.infinity(), 'd_i'+str(i)+'_t_'+str(t))
                for t in range(0, max_term_months)]
                for i in range(0, num_loans)])

    ## Principal
    principal = \
        np.array(
            [[solver.NumVar(0, solver.infinity(), 'p_i'+str(i)+'_t_'+str(t))
                for t in range(0, max_term_months)]
                for i in range(0, num_loans)])

    ## Binary for whether loan is principal remains(1) or not(0), i.e. is loan paid off
    remnant = \
        np.array(
            [[solver.BoolVar('b_i'+str(i)+'_t_'+str(t))
                for t in range(0, max_term_months)]
                for i in range(0, num_loans)])

    ## Declare minimization objective
    solver.Minimize(
        sum(
            sum(decision[i,:]) + sum(remnant[i,:]) for i in range(0, num_loans)))

    # Set constraints ---------------------------------------
    ## Starting principal is nonzero
    constraint_principal_init = [solver.Constraint(principal_initial[i], principal_initial[i]) for i in range(0, num_loans)]
    for i in range(0, num_loans):
        constraint_principal_init[i].SetCoefficient(principal[i,0], 1)

    ## Principal is zero at end of term
    constraint_payoff_tmax = \
        np.array([solver.Add(principal[i, term_months[i]-1] <= 0) for i in range(0, num_loans)])

    ## Principal in each period is equal to principal of previous period, interest, and payment
    constraint_principal_rolling = \
        np.array(
            [[solver.Add(
                (principal[i, t] == (1+rate_monthly[i]) * principal[i, t-1] - decision[i, t-1]))
                for t in range(1, max_term_months)]
                for i in range(0, num_loans)])

    ## Sum of payments must not exceed budget
    constraint_budget = \
        np.array([
            solver.Add(
                sum(decision[0:, t]) <= budget) for t in range(0, max_term_months)])

    ## Remnant 
    constraint_remnant = \
            np.array(
            [[solver.Add(
                remnant[i, t] >= principal[i,t]/principal_initial[i])
                for t in range(0, max_term_months)]
                for i in range(0, num_loans)])

    ## Montly payment must meet minimum
    constraint_min_payment = \
        np.array(
            [[solver.Add(
                decision[i,t] >= decision_min[i]*remnant[i,t])
                for t in range(0, max_term_months)]
                for i in range(0, num_loans)])

    # Solve ----------------------
    if verbose[0]==True:
        status = solver.NOT_SOLVED   # set status flag to not solved
        i = 1   # set index flag
        while status != solver.OPTIMAL:
            status = solver.Solve()   # query solver status
            wall_time = solver.wall_time()  # query number of simplex iterations
            if status in (solver.FEASIBLE, solver.OPTIMAL):
                interest_cost = \
                    solver.Objective().Value() - sum(principal_initial) - sum(
                        [remnant[i,t].solution_value()
                            for i in range(0, num_loans)
                            for t in range(0, term_months[i])])    # interest cost w/ optimal schedule
            else:
                interest_cost = "__not_solved__"
            print("Optimal solution is: $" + str(interest_cost) 
                + " after " + str(wall_time/1000) + " milliseconds.")
            i = i+1   # update flag
            solver.set_time_limit(time_limit_milliseconds * i)   # update time limit
    else:
        status = solver.Solve()

    decision_solution = \
        np.array(
            [[decision[i,t].solution_value() for t in range(0, term_months[i])]
            for i in range(0, num_loans)])
    print(decision_solution)

    principal_solution = \
        np.array(
            [[principal[i,t].solution_value() for t in range(0, term_months[i])]
            for i in range(0, num_loans)])
    print(principal_solution)

    interest_cost = \
        solver.Objective().Value() - sum(principal_initial) - sum(
            [remnant[i,t].solution_value()
                for i in range(0, num_loans)
                for t in range(0, term_months[i])]) # interest cost w/ optimal schedule

    print("Optimal payoff interest cost = " + 
        str(interest_cost)) # interest cost w/ optimal schedule

    # Lp file ----------------------
    """ solver_debug_file = solver.ExportModelAsLpFormat(False)
    f = open('debug.txt', 'a')
    f.write(solver_debug_file)
    f.close() """

    # Return -------------------
    return([interest_cost, decision_solution])
