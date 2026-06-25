from gurobipy import *
import code.model as m

# Run optimisation
m.m.optimize()

print()
print(f"Total cost: ${round(m.m.ObjVal, 2)}")

# -------------------------
# Yearly reporting
# -------------------------
for t in m.T:
    print("----- Year:", m.d.years[t], "-----")

    print(
        "Total cost:",
        round(
            sum(m.d.costs[r][s] * m.X[s, r, t].X for r in m.R for s in m.d.warehouses)
            + sum(
                m.d.transport_costs[t] * m.Y[e, r, t].X * m.d.Roads[e][m.DISTANCE]
                for r in m.R for e in m.E
            ),
            2
        )
    )

    print(
        "Burn Fuel total purchase:",
        round(sum(m.X[s, 0, t].X for s in m.d.warehouses), 2),
        "L"
    )

    print(
        "Fire suppressant total purchase:",
        round(sum(m.X[s, 1, t].X for s in m.d.warehouses), 2),
        "L"
    )

    print(
        "Transport:",
        round(sum(m.Y[e, r, t].X for e in m.E for r in m.R), 2),
        "L"
    )

    print(
        "Stored Fuel:",
        round(sum(m.Z[s, 0, t].X for s in m.S), 2),
        "L"
    )

    print(
        "Stored Suppressant:",
        round(sum(m.Z[s, 1, t].X for s in m.S), 2),
        "L"
    )