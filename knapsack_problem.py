from ortools.algorithms.python import knapsack_solver

import json



def main():
    # Create the solver.
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )
    
    with open('./artists.json', 'r') as f:
        data = json.load(f)

    print(data)
    
    values = [f['value_snai'] for f in data]
    print("")
    print(values)
    print(type(values))
    
    weights = [[f['weight'] for f in data],]
    print("")
    print(weights)
    print(type(weights))
    
    capacities = [100] #baudi

    solver.init(values, weights, capacities)
    print(solver)
    computed_value = solver.solve()

    packed_items = []
    packed_weights = []
    total_weight = 0
    print("Total value =", computed_value)
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(data[i]["name"])
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print("Total weight:", total_weight)
    print("Packed items:", packed_items)
    print("Packed_weights:", packed_weights)


if __name__ == "__main__":
    main()