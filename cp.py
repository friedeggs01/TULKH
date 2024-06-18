# import os
# import time
# from collections import deque
# import queue
# def readData(path2input='E:/src code 2/python 2/tulkh/TULKH/input.txt'):
#     with open(path2input,'r') as f:
#         data = f.read().split('\n')
#         N, K = map(lambda x: int(x), data[0].split(' '))
#         d = list(map(lambda x: int(x), data[1].split(' ')[:N]))
#         t = [list(map(lambda x: int(x), i.split(' ')[:N+1])) for i in data[2:N+3]]
#     return N, K, d, t
# def creat_cost(N, d, t):
#     for i in range(N + 1):
#         for j in range(1, N + 1):
#             if i != j:
#                 t[i][j] += d[j - 1] 

#     return t
# import numpy as np




# Q_k = 1e9
# maxStep = None
# N, K, d, t = None, None, None, None



# def ac3(vars, domains, constraints):
#     queue = deque(constraints)
    
#     while queue:
#         constraint = queue.popleft()
#         var1, var2 = constraint
#         revised = False
        
#         for val1 in domains[var1][:]:  # Iterate over a copy of the list
#             satisfy = False
#             for val2 in domains[var2]:
#                 if val1 + val2 < 2:
#                     satisfy = True
#                     break
#             if not satisfy:
#                 domains[var1].remove(val1)
#                 revised = True
        
#         if revised:
#             if len(domains[var1]) == 0:
#                 return False
#             for cons in constraints:
#                 if cons[1] == var1:
#                     queue.append((cons[0], cons[1]))
    
#     return True

# def forward(variables, domains):
#     # print('pre domains',domains)
#     # Khởi tạo các ràng buộc
#     constraints = [] #list(combinations([i for i in range(1, N)], 3))

#     for i in range(1, N + 1):
#         for j1 in range(1, N + 1):
#             for j2 in range(j1 + 1, N + 1):
#                 if i != j1 and i != j2:
#                     constraints.append((ij2vertex(i,j1), ij2vertex(i,j2)))
#                     # print(i,j1,i,j2)
#                     constraints.append((ij2vertex(i,j2), ij2vertex(i,j1)))
#     for i in range(1, N + 1):
#         for j1 in range(1, N + 1):
#             for j2 in range(j1 + 1, N + 1):
#                 if i != j1 and i != j2:
#                     constraints.append((ij2vertex(j1, i), ij2vertex(j2, i)))
#                     constraints.append((ij2vertex(j2, i), ij2vertex(j1, i)))
#                     # print(j1,i,j2,i)
    
#     pre = domains.copy()
#     # Áp dụng AC3 cho bài toán của bạn
#     if ac3(variables, domains, constraints):
#         post = domains.copy()
#         if post != pre:
#             print('pre  domains', pre)
#             print('post domains',post)
#         # exit(0)
#         return True
#         print("Found consistent assignments:")
#         print(domains)
#     else:
#         return False
#         print("No consistent assignments found.")

# def vertex2ij(v):
#     return v // (N + 1), v % (N+1)
# def ij2vertex(i, j):
#     return i * (N + 1) + j 



# from collections import defaultdict, deque

# def has_eulerian_cycle(graph, N):
#     in_degree = [0] * (N + 1)
#     out_degree = [0] * (N + 1)
    
#     for u in range(N + 1):
#         for v in graph[u]:
#             out_degree[u] += 1
#             in_degree[v] += 1
    
#     for i in range(N + 1):
#         if in_degree[i] != out_degree[i]:
#             return False
    
#     return True

# def check_conditions(graph):

#     for l in graph[1:]:
#         if len(l) != 1:
#             return False
        
#     if len(graph[0]) > K:
#         return False
#     print('graph', graph)

#     num_in_visit = [0] * (N+1)
#     num_out_visit = [len(list_v) for list_v in graph]
#     for o in num_out_visit[1:]:
#         if o != 1:
#             return False

#     for i in range(N+1):
#         for v in graph[i]:
#             if v == 0:
#                 continue
#             if num_in_visit[v]:
#                 return False
#             num_in_visit[v] += 1
#     for i, o in zip(num_in_visit, num_out_visit):
#         if i != o:
#             return False
#     my_queue = queue.Queue()
#     for e in graph[0]:
#         my_queue.put(e)
#     while not my_queue.empty():
#         v = my_queue.get()
#         if len(graph[v]) != 1:
#             return False
#         if graph[v][0] != 0:
#             my_queue.put(graph[v][0])
#     print('graph',graph)
#     return True
# def check_solution(domains):
#     if domains[1:5] == [[1]*4]:
 
#         print(domains)
#     graph = [[] for i in range(N + 1)]
#     for v, d in enumerate(domains):
#         if d[0] == 1:
#             i,j = vertex2ij(v)
#             graph[i].append(j)
#     return check_conditions(graph)
# # mark = [0]*10000
# def solve(variables, domains, step, cost):
#     # print(domains, step, cost)
#     global Q_k
#     if step > maxStep or cost > Q_k:
#         return
#     if not forward(variables, domains):
#         return
#     # print(domains)
    
#     # print(variables)
#     for v in variables:

#         if len(domains[v]) == 0:
#             print("error"*100)
#             return
#         if len(domains[v]) == 2:
#             # print(v)
#             # exit(0)
#             # if mark[v]:
#             #     print(v)
#             #     exit(0)
#             # mark[v] = 1
#             # print(v)
#             i,j = vertex2ij(v)
#             new_domains = domains.copy()
#             new_domains[v] = [1]
#             solve(variables, new_domains, step + 1, cost + t[i][j])
#             new_domains = domains.copy()
#             new_domains[v] = [0] 
#             solve(variables, new_domains, step, cost)  
#             return
#     if check_solution(domains):
#         Q_k = cost
             



# def cp():
#     variables = [i for i in range((N + 1)**2)] # cạnh từ đỉnh i tới j i * (N + 1) + j  
#     global maxStep
#     maxStep = N + K + K
#     domains = []
#     for v in variables:
#         i, j = vertex2ij(v)
#         if i == j:
#             domains.append([0])
#         else:
#             domains.append([0,1])
#     solve(variables, domains, 0, 0) # var, D, step, cost
    

# for inp in ['data_5_2.txt']:#os.listdir('data'):, 'data_10_5.txt', 'data_20_10.txt', 'data_50_25.txt'
#     inp = os.path.join('data',inp)
#     with open('log_output.txt', 'a+') as f:
#         f.write(f"{inp}\n")
#     with open('output.txt','a') as f:
#         f.write(f"{inp}\n")
#     start_time = time.time()

#     N, K, d, t = readData(inp)

#     t = creat_cost(N, d, t)
#     num_costoms_of_worker = [0] * K

#     best = cp()
#     print(Q_k)
#     for id, val in best[0].items():
#         max_time = -1
#         path = val.copy()
#         path.append(0)
#         total_time = 0
#         total_time += t[0][path[0]]
#         print(t[0][path[0]])
#         for i in range(len(path) - 1):
#             total_time += t[path[i]][path[i + 1]]
#             print(t[path[i]][path[i + 1]])
#         print('total_time',total_time)
#         max_time = max(max_time, total_time)
#     print(max_time)
#     end_time = time.time()
#     with open('output.txt','a') as f:
#         f.write(str(end_time - start_time)+"\n")
#         for key, value in best[0].items():
#             f.write(f'{key}: {value}\n')
#         f.write('total time:' + str(best[1])+"\n")


import os
import time
from collections import deque
import queue
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
import numpy as np




N, K, d, t = None, None, None, None


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model(distance_matrix = t, num_vehicles = K):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = distance_matrix
    data["num_vehicles"] = num_vehicles
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    # print(f"Objective: {solution.ObjectiveValue()}")
    max_route_distance = 0
    plan_output = f""
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f"{manager.IndexToNode(index)} "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        # plan_output += f"Distance of the route: {route_distance}m\n"
        
        max_route_distance = max(route_distance, max_route_distance)
    return max_route_distance, plan_output
    print(f"Objective: {max_route_distance}")
    print(plan_output)



def cp(t, K):
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
        10000000,  # vehicle maximum travel distance
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
        return print_solution(data, manager, routing, solution)
    else:
        print("No solution found !")
        return None




for file in ['data_5_3.txt',
 'data_5_2.txt',
 'data_10_3.txt',
 'data_20_3.txt',
 'data_50_7.txt',
 'data_20_7.txt',
 'data_50_5.txt',
 'data_20_5.txt',
 'data_10_5.txt',
 'data_10_2.txt',
 'data_20_10.txt',
 'data_50_20.txt',
 'data_50_10.txt',
 'data_50_25.txt',
 'data_500_20.txt',
 'data_100_50.txt',
 'data_200_20.txt',
 'data_100_10.txt',
 'data_700_70.txt',
 'data_200_50.txt',
 'data_700_50.txt',
 'data_500_50.txt',
 'data_1000_50.txt',
 'data_1000_100.txt']:#os.listdir('data'):, 'data_10_5.txt', 'data_20_10.txt', 'data_50_25.txt'
    inp = os.path.join('data',file)
    start_time = time.time()

    N, K, d, t = readData(inp)

    t = creat_cost(N, d, t)
    st = time.time()
    max_route_distance, plan_output = cp(t, K)
    tt_time = time.time() - st
    with open("result/result_cp/"+file,'w') as f:
        f.write(f'Objective: {max_route_distance}\nRunning time : {tt_time}\nSolution : \n{plan_output}')