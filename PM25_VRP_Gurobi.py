"""Core Gurobi model for PM2.5 monitoring-site maintenance routing.

This is a model excerpt, NOT a standalone executable script.
Required upstream objects: gp, GRB, NODES, CUSTOMERS, VEHICLES, ARCS,
DEPOT, COST, B, MAXTIME, TIME_LIMIT, MIP_GAP.

Paper correspondence: Eqs. (1)-(10).
"""

# Preprocessing assumption: COST[i, j] = travel_time[i, j] + service_time[j].
# For serviced monitoring locations, service_time[j] = 15 minutes;
# for the depot, service_time[DEPOT] = 0 minutes. Thus, returning to
# the depot incurs travel time only. Service time is NOT added again below.
# ARCS must contain the permissible (i, j) pairs with i != j.
# B[i-1] assumes consecutively numbered monitoring nodes and a matching
# zero-indexed maintenance-requirement array; in the study all B entries are 1.

# Model initialization and decision variables: Eqs. (9)-(10)
model = gp.Model('PM25_student_original_clean')
x = model.addVars([(i, j, k) for i, j in ARCS for k in VEHICLES],
                  vtype=GRB.BINARY, name='x')  # Eq. (10): arc selection
u = model.addVars(CUSTOMERS, lb=1, ub=len(CUSTOMERS),
                  vtype=GRB.CONTINUOUS, name='u')  # Eq. (9): MTZ bounds

# Eq. (1): minimize total travel plus on-site maintenance time.
model.setObjective(
    gp.quicksum(COST[i, j] * x[i, j, k]
                for i, j in ARCS for k in VEHICLES),
    GRB.MINIMIZE
)

# Eq. (2): each vehicle departs from the depot exactly once.
model.addConstrs(
    (gp.quicksum(x[DEPOT, j, k] for j in CUSTOMERS) == 1
     for k in VEHICLES), name='DepotDeparture'
)

# Eq. (3): each vehicle returns to the depot exactly once.
model.addConstrs(
    (gp.quicksum(x[i, DEPOT, k] for i in CUSTOMERS) == 1
     for k in VEHICLES), name='DepotReturn'
)

# Eq. (4): one outgoing arc for each location requiring service.
model.addConstrs(
    (gp.quicksum(x[i, j, k] for j in NODES if i != j
                 for k in VEHICLES) == B[i-1]
     for i in CUSTOMERS), name='CustomerOut'
)

# Eq. (5): one incoming arc for each location requiring service.
model.addConstrs(
    (gp.quicksum(x[j, i, k] for j in NODES if i != j
                 for k in VEHICLES) == B[i-1]
     for i in CUSTOMERS), name='CustomerIn'
)

# Eq. (6): vehicle-specific flow conservation at each node.
model.addConstrs(
    (gp.quicksum(x[i, j, k] for i in NODES if i != j) ==
     gp.quicksum(x[j, i, k] for i in NODES if i != j)
     for j in NODES for k in VEHICLES), name='FlowBalance'
)

# Eq. (7): maximum operating time per vehicle, including service times.
# The case-study scenarios use MAXTIME = 420, 360, 300, or 240 minutes.
model.addConstrs(
    (gp.quicksum(COST[i, j] * x[i, j, k] for i, j in ARCS) <= MAXTIME
     for k in VEHICLES), name='MaxTime'
)

# Eq. (8): MTZ subtour elimination; Eq. (9) bounds are set above.
n = len(NODES)
model.addConstrs(
    (u[i] - u[j] + n * gp.quicksum(x[i, j, k] for k in VEHICLES) <= n-1
     for i in CUSTOMERS for j in CUSTOMERS if i != j), name='MTZ'
)

# Solver controls: supplied by the upstream experiment configuration.
# In the reported experiments: TIME_LIMIT = 600 seconds; MIP_GAP = 0.001.
model.Params.TimeLimit = TIME_LIMIT
model.Params.MIPGap = MIP_GAP
model.optimize()

# Results: distinguish a feasible solution from proven optimality.
print('Solver status:', model.Status)
if model.SolCount == 0:
    raise RuntimeError('Gurobi did not find a feasible solution; no routes can be reported.')
print('Objective ETIME15:', round(model.ObjVal, 3), 'minutes')
print('Best bound:', round(model.ObjBound, 3), 'minutes')
print('MIP gap:', round(model.MIPGap * 100, 4), '%')
if model.Status != GRB.OPTIMAL:
    print('Warning: feasible incumbent found, but global optimality was not proven.')
