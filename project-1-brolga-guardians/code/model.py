from gurobipy import *
import data.data as d

m = Model("Brolga")

# -------------------------
# Sets
# -------------------------
S = range(len(d.Sites))
E = range(len(d.Roads))
R = range(len(d.costs))
T = range(len(d.years))

FROM_SITE = d.FROM_SITE
TO_SITE = d.TO_SITE
DISTANCE = d.DISTANCE
CAPACITY = d.CAPACITY

# -------------------------
# Variables
# -------------------------
X = {(s, r, t): m.addVar() for s in S for r in R for t in T}
Y = {(e, r, t): m.addVar() for e in E for r in R for t in T}
Z = {(s, r, t): m.addVar() for s in S for r in R for t in T}

m.update()

# -------------------------
# Objective
# -------------------------
m.setObjective(
    quicksum(d.costs[r][s] * X[s, r, t]
             for s in d.warehouses
             for r in R
             for t in T)
    +
    quicksum(d.transport_costs[t] * d.Roads[e][DISTANCE] * Y[e, r, t]
             for e in E
             for r in R
             for t in T),
    GRB.MINIMIZE
)

# -------------------------
# Constraints
# -------------------------
for t in T:

    # Road capacity
    for e in E:
        m.addConstr(
            quicksum(Y[e, r, t] for r in R)
            <= d.Roads[e][CAPACITY]
        )

    for s in S:
        for r in R:

            # Availability + storage
            if s in d.availability[r]:
                m.addConstr(X[s, r, t] <= d.availability[r][s])
                m.addConstr(Z[s, r, t] <= 0)
            else:
                m.addConstr(X[s, r, t] <= 0)
                m.addConstr(quicksum(Z[s, r, t] for r in R) <= d.max_store)

            # Flow balance
            inflow = quicksum(
                (1 - d.evaporation_cost[r] * d.Roads[e][DISTANCE]) * Y[e, r, t]
                for e in E if d.Roads[e][TO_SITE] == s
            )

            outflow = quicksum(
                Y[e, r, t]
                for e in E if d.Roads[e][FROM_SITE] == s
            )

            if t > 0:
                m.addConstr(
                    X[s, r, t]
                    + Z[s, r, t-1]
                    + inflow
                    == d.demand[r][s][t]
                    + outflow
                    + Z[s, r, t]
                )
            else:
                m.addConstr(
                    X[s, r, t]
                    + inflow
                    == d.demand[r][s][t]
                    + outflow
                    + Z[s, r, t]
                )

S = S
E = E
R = R
T = T
X = X
Y = Y
Z = Z
m = m
d = d
DISTANCE = DISTANCE