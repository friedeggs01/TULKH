import time
import random



def init_population(num_customs, num_employees, population_size):
    population = []
    for _ in range(population_size):
        assign = {i : [] for i in range(num_employees)}
        isAssigned = [False]*(num_customs + 1)
        start_work = random.sample(range(1, num_customs + 1), num_employees)
        for  i in range(num_employees):
            assign[i].append(start_work[i])
            isAssigned[start_work[i]] = True

       
        for i in range(1, num_customs + 1):
            if isAssigned[i]:
                continue
            assign[random.randint(0, num_employees - 1)].append(i)
        population.append(assign)
    # print('init_population(num_customs, num_employees, population_size)', population)
    return population


def cal_max_time(times, assign):
    max_time = -1
    for key, val in assign.items():
        path = val.copy()
        path.append(0)
        total_time = 0
        total_time += times[0][path[0]]
        for i in range(len(path) - 1):
            total_time += times[path[i]][path[i + 1]]
        max_time = max(max_time, total_time)
    return max_time

def selection(population, fitness_scores):
    """
    Chọn các cá thể từ quần thể dựa trên điểm thích nghi của chúng.

    Tham số:
        - population (list): Danh sách các cá thể trong quần thể.
        - fitness_scores (list): Danh sách điểm thích nghi tương ứng với từng cá thể trong quần thể.

    Trả về:
        - selected (dict): Cá thể được chọn.
    """
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected = random.choices(population, probabilities)[0]
    # print('selection(population, fitness_scores):', population, selected)
    return selected

# times = [[1] * 11] * 11
# print(cal_max_time(times, init_population(10,3,10)[0]))




def ox_crossover(parent1, parent2):
    # print('ox_crossover(parent1, parent2):', parent1, parent2)
    child_routes = {k: v[:] for k, v in parent2.items()}
    
    # Randomly choose a subroute from a random route in parent1
    #print(parent1)
    parent1_route_keys = list(parent1.keys())
    parent1_route_idx = random.randint(0, len(parent1_route_keys) - 1)
    parent1_route = parent1[parent1_route_keys[parent1_route_idx]]
    if not parent1_route:
        return child_routes
    start = random.randint(0, len(parent1_route) - 1)
    end = random.randint(start, len(parent1_route) - 1)
    subroute = parent1_route[start:end+1]
    
    # Find a random position to insert the subroute in the child
    child_route_keys = list(child_routes.keys())
    child_route_idx = random.randint(0, len(child_route_keys) - 1)
    insert_pos = random.randint(0, len(child_routes[child_route_keys[child_route_idx]]))
    
    # Remove the customers in the subroute from the child routes
    for customer in subroute:
        for key, route in child_routes.items():
            if customer in route:
                child_routes[key].remove(customer)
    
    # Insert the subroute into the child
    child_routes[child_route_keys[child_route_idx]][insert_pos:insert_pos] = subroute
    # print('child_routes',child_routes)
    return child_routes

def mutation(assign, mutation_rate):
    mutated_assignments = assign.copy()

    for emp, tasks in mutated_assignments.items():
        if emp != 0 and random.random() < mutation_rate:
            # Select a random subsequence of tasks assigned to the employee
            if len(tasks) >= 2:
                start = random.randint(0, len(tasks) - 2)
                end = random.randint(start + 1, len(tasks))

                # Reverse the subsequence of tasks
                mutated_assignments[emp][start:end] = reversed(tasks[start:end])
    if random.random() < mutation_rate:
        cut_and_insert_longest_to_random(mutated_assignments)
    # print('def mutation(assign, mutation_rate):\n', assign, mutated_assignments)
    return mutated_assignments

def cut_and_insert_longest_to_random(routes):
    # Tìm chuỗi dài nhất và tạo danh sách các chuỗi khác
    longest_route_key, longest_route = max(routes.items(), key=lambda x: len(x[1]))
    other_routes = [(key, value) for key, value in routes.items() if key != longest_route_key]

    # Nếu không có đoạn nào trong chuỗi dài nhất, không thực hiện gì cả
    if not longest_route:
        return routes

    # Chọn một đoạn ngẫu nhiên từ chuỗi dài nhất
    start = random.randint(0, len(longest_route) - 2)
    end = random.randint(start + 1, len(longest_route) - 1)
    cut_segment = longest_route[start:end+1]

    # Chọn một chuỗi ngẫu nhiên để chèn đoạn đã cắt
    random_route_key, random_route = random.choice(other_routes)
    insert_index = random.randint(0, len(random_route))

    # Chèn đoạn đã cắt vào chuỗi ngẫu nhiên
    routes[longest_route_key] = longest_route[:start] + longest_route[end+1:]
    routes[random_route_key] = random_route[:insert_index] + cut_segment + random_route[insert_index:]

    return routes


# pop = init_population(10,3,10)
# print(pop[0])
# # print(pop[1])
# # print(ox_crossover(pop[0],pop[1]))
# print(mutation(pop[0], 0.4))


# # routes = {
# #     0: [4, 3, 5, 7, 8, 10],
# #     1: [9],
# #     2: [6, 1, 2]
# # }
# # print(cut_and_insert_longest_to_shortest(routes))
def ga(num_customs, num_employees, times, population_size, num_generations, mutation_rate):
    # print('def ga(num_customs, num_employees, times, population_size, num_generations, mutation_rate):', num_customs, num_employees, times, population_size, num_generations, mutation_rate)
    epsilon = 1e-2
    shortest_time = 1e9
    best_solution = None
    pops = init_population(num_customs, num_employees,population_size)
    # print('pops = init_population(num_customs, num_employees,population_size)', pops)
    for _ in range(num_generations):
        new_pops = [] 
        point_pops = []     
        fitness = []
        for pop in pops:
            time_tmp = cal_max_time(times, pop)
            if time_tmp < shortest_time:
                shortest_time = time_tmp
                best_solution = pop
            fitness.append(1/time_tmp + epsilon)
        for pop_id in range(population_size):
            p1 = selection(pops,fitness)
            p2 = selection(pops,fitness)
            # print('p1',p1,'p2',p2)

            c1 =  mutation(ox_crossover(p1,p2), mutation_rate)
            time_tmp = cal_max_time(times, c1)
            new_pops.append(c1)
            point_pops.append(time_tmp)
            if time_tmp < shortest_time:
                shortest_time = time_tmp
                best_solution = c1

            c2 =  mutation(ox_crossover(p2,p1), mutation_rate)
            time_tmp = cal_max_time(times, c2)
            new_pops.append(c2)
            point_pops.append(time_tmp)
            if time_tmp < shortest_time:
                shortest_time = time_tmp
                best_solution = c2

        combined = list(zip(new_pops, point_pops))
        sorted_combined = sorted(combined, key=lambda x: x[1])
        top_k = sorted_combined[:population_size]
        pops = [pop for pop, point in top_k]       

    return best_solution, shortest_time


import os
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



#############################
#           config          #
#############################
population_size, num_generations, mutation_rate = 500, 500, 0.5







for inp in ['data_5_2.txt']:#os.listdir('data'):, 'data_10_5.txt', 'data_20_10.txt', 'data_50_25.txt'
    inp = os.path.join('data',inp)
    with open('output.txt','a') as f:
        f.write(f"{inp}\n")
    start_time = time.time()
    N, K, d, t = readData(inp)
    t = creat_cost(N, d, t)
    best = ga(num_customs = N, num_employees=K, times=t,  population_size=population_size, num_generations=num_generations, mutation_rate=mutation_rate)
    end_time = time.time()
    print(best)
    with open('result/ga.txt','a') as f:
        f.write(str(end_time - start_time)+"\n")
        for key, value in best[0].items():
            f.write(f'{key}: {value}\n')
        f.write('total time:' + str(best[1])+"\n")