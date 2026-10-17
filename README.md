# PM2.5 Monitoring Sensor Maintenance Routing — Gurobi Model

This repository contains the **core Gurobi model listing** associated with the paper *A Vehicle Routing Optimization Model for Maintenance Planning of Urban PM2.5 Monitoring Sensors*.

## Contents

- `PM25_VRP_Gurobi.py`: annotated implementation corresponding to Equations (1)–(10).
- `PM25_VRP_Gurobi.txt`: plain-text copy of the same code.
- `requirements.txt`: Gurobi Python dependency.

## Important: not a standalone reproduction package

The code listing is **not independently executable** without the original preprocessing and input data. It requires `gp`, `GRB`, `NODES`, `CUSTOMERS`, `VEHICLES`, `ARCS`, `DEPOT`, `COST`, `B`, `MAXTIME`, `TIME_LIMIT`, and `MIP_GAP` to be defined beforehand. In particular, `COST` is a precomputed arc-time matrix; this package does not include the restricted origin–destination travel-time matrix or preprocessing scripts. Accordingly, the published case-study numerical results cannot be reproduced from this listing alone.

## Model assumptions

- Each selected arc has time `COST[i,j] = t_ij + s_j`, where `t_ij` is travel time and `s_j` is maintenance time at destination `j`.
- Each of the 22 monitoring locations in the reported case study requires 15 minutes of maintenance.
- The depot requires zero maintenance time, so a return-to-depot arc includes travel time only.
- Two vehicles are used; each must leave and return to the depot once.
- The scenarios limit each vehicle's operating time to 420, 360, 300, or 240 minutes.
- The formulation minimizes **total** operating time, not maximum workload or workload imbalance.

## Dependencies

Install a compatible Python version and `gurobipy` (see `requirements.txt`). A valid Gurobi license may be required for the case-study model size.

## Data availability

The complete origin–destination matrix is not included because of organizational data-sharing restrictions. Requests for additional materials can be considered by the corresponding author, subject to applicable permissions and restrictions.

## Citation

Boonmee, C., Wanichdee, Y., Arimura, M., Kongpul, S., Koohathongsumrit, N., and Phutthanawong, K. (2026). A Vehicle Routing Optimization Model for Maintenance Planning of Urban PM2.5 Monitoring Sensors. DASA 2026.

## License

The source code is publicly available for academic and research purposes. Researchers are permitted to use, modify, and adapt the code, provided that the original paper associated with this repository is appropriately cited. Commercial use requires prior written permission from the copyright holders.
