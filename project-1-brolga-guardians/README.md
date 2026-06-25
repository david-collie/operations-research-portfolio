# Brolga Guardians — Operations Research Optimisation Model

## Overview
Multi-period supply chain optimisation model for resource allocation across a network of sites and warehouses. The system minimises total cost while satisfying demand constraints under capacity and transport limitations.

## Problem Type
- Multi-commodity flow network
- Multi-period inventory optimisation
- Constrained linear programming (Gurobi)

## Model Structure

### Decision Variables
- X[s, r, t]: resource purchased at location s
- Y[e, r, t]: flow on transport edge e
- Z[s, r, t]: inventory stored at site s

### Objective
Minimise:
- procurement cost
- transport cost
- (implicit) storage effects

### Constraints
- demand satisfaction
- warehouse capacity limits
- road capacity constraints
- flow conservation
- inventory balance over time

## Tools
- Python
- Gurobi Optimizer

## Files
- `code/model.py` → optimisation model
- `code/solve.py` → execution & reporting
- `data/data.py` → dataset & parameters

## Full Report
A detailed technical report including:
- mathematical formulation
- model derivation
- assumptions
- solution interpretation
📄 See: `docs/report.pdf`