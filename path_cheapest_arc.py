"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""
def readData(path2input='E:/src code 2/python 2/tulkh/TULKH/input.txt'):
    with open(path2input,'r') as f:
        data = f.read().split('\n')
        N, K = map(lambda x: int(x), data[0].split(' '))
        d = list(map(lambda x: int(x), data[1].split(' ')[:N]))
        t = [list(map(lambda x: int(x), i.split(' ')[:N+1])) for i in data[2:N+3]]
    return N, K, d, t
def creat_cost(N, d, t):
    for i in range(N + 1):
        for j in range(1, N + 1):
            if i != j:
                t[i][j] += d[j - 1] 

    return t
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model(t, K):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = t
    data["num_vehicles"] = K
    data["depot"] = 0
    return data


# def print_solution(data, manager, routing, solution):
#     """Prints solution on console."""
#     print(data["num_vehicles"])
#     for vehicle_id in range(data["num_vehicles"]):
#         index = routing.Start(vehicle_id)
#         plan_output = ""
#         Lk = 1
#         while not routing.IsEnd(index):
#             Lk += 1
#             plan_output += f"{manager.IndexToNode(index)} "
#             index = solution.Value(routing.NextVar(index))
#         plan_output += f"{manager.IndexToNode(index)}"
#         print(Lk)
#         print(plan_output)
#log output
def print_solution(data, manager, routing, solution):
    with open('log_output.txt', 'a+') as f:
        """Prints solution on console."""
        print(data["num_vehicles"])
        f.write(str(data["num_vehicles"]) + "\n")
        for vehicle_id in range(data["num_vehicles"]):
            index = routing.Start(vehicle_id)
            plan_output = ""
            Lk = 1
            while not routing.IsEnd(index):
                Lk += 1
                plan_output += f"{manager.IndexToNode(index)} "
                index = solution.Value(routing.NextVar(index))
            plan_output += f"{manager.IndexToNode(index)}"
            f.write(str(Lk) + "\n")
            print(Lk)
            f.write(plan_output + "\n")
            print(plan_output)

def solve(t, K):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(t, K)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("No solution found !")


import time 
import os
for inp in ['data_5_2.txt', 'data_10_5.txt', 'data_20_10.txt', 'data_50_25.txt']:#os.listdir('data'):
    inp = os.path.join('data',inp)
    with open('log_output.txt', 'a+') as f:
        f.write(f"{inp}\n")
    with open('output.txt','a') as f:
        f.write(f"{inp}\n")
    start_time = time.time()
    N, K, d, t = readData(inp)
    t = creat_cost(N, d, t)
    solve(t, K)
    end_time = time.time()
    with open('output.txt','a') as f:
        f.write(str(end_time - start_time)+"\n")