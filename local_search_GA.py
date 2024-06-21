import random
from time import time 

def calculate_total_time(assignments, repair_times, travel_times):
    max_time = 0
    for emp_assignments in assignments.values():
        total_time = 0
        for i in range(len(emp_assignments)):
            if i < len(emp_assignments)-1:
                total_time += travel_times[emp_assignments[i]][emp_assignments[i+1]] 
            total_time += repair_times[emp_assignments[i]]
        if len(emp_assignments)>0: 
            total_time += travel_times[0][emp_assignments[0]] 
            total_time += travel_times[emp_assignments[-1]][0] 
        max_time = max(max_time, total_time)
    return max_time


def generate_initial_population(customers, num_employees, population_size):
    population = []
    for _ in range(population_size):
        assignments = {i: [] for i in range(num_employees)}
        for customer in customers:
            emp = random.randint(0, num_employees - 1)
            assignments[emp].append(customer)
        population.append(assignments)
    return population

def generate_neighbors(assignments,num_employees):
    neighbors = []
    random.shuffle(assignments)
    for old_emp in assignments.keys():
        for old_cust in assignments[old_emp]: 
            for new_emp in range(num_employees):
                #if old_emp != new_emp:
                new_assignments ={emp :assignments[emp].copy() for emp in assignments.keys()} 
                new_assignments[old_emp].remove(old_cust)
                new_assignments[new_emp].append(old_cust)
                neighbors.append(new_assignments)
                if len(neighbors) > 5000: break 
            if len(neighbors) > 5000: break 
        if len(neighbors)> 5000: break 
    
    for old_emp in assignments.keys():
        for i in range(len(assignments[old_emp])):
            for j in range(i+1, len(assignments[old_emp])):
                new_assignments = {emp: assignments[emp].copy() for emp in assignments.keys()}
                new_assignments[old_emp] = new_assignments[old_emp][:i] + list(reversed(new_assignments[old_emp][i:j+1])) + new_assignments[old_emp][j+1:]
                neighbors.append(new_assignments)
                if len(neighbors) > 5000:
                    break
                if len(neighbors) > 5000:
                    break
            if len(neighbors) > 5000: break 
        if len(neighbors)> 5000: break 
    random.shuffle(neighbors) 
    
    return neighbors

def calculate_fitness(assignments, repair_times, travel_times):
    total_time = calculate_total_time(assignments, repair_times, travel_times)
    return 1 / (total_time + 1)  # Fitness is inversely proportional to total time

def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected = random.choices(population, probabilities)[0]
    return selected



def mutation(assignments, mutation_rate):
    mutated_assignments = assignments.copy()

    for emp, tasks in mutated_assignments.items():
        if emp != 0 and random.random() < mutation_rate:
            # Select a random subsequence of tasks assigned to the employee
            if len(tasks) >= 2:
                start = random.randint(0, len(tasks) - 2)
                end = random.randint(start + 1, len(tasks))

                # Reverse the subsequence of tasks
                mutated_assignments[emp][start:end] = reversed(tasks[start:end])

    return mutated_assignments

def ox_crossover(parent1, parent2):
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
    
    return child_routes

def local_search_with_ga(customers, repair_times, travel_times, num_employees, population_size, num_generations, mutation_rate):
    population = generate_initial_population(customers, num_employees, population_size)

    best_fitness = 0
    best_assignments = None

    for _ in range(num_generations):
        fitness_scores = []
        new_population = []

        for assignments in population:
            # Perform local search on each individual
            for _ in range(100):  # Local search iterations
                neighbors = generate_neighbors(assignments,num_employees)
                best_emp = None
                best_time_diff = float('inf')

                for neighbor in neighbors:
                    new_time = calculate_total_time(neighbor, repair_times, travel_times)
                    time_diff = new_time - calculate_total_time(assignments, repair_times, travel_times)
                    if time_diff < best_time_diff:
                        best_emp = neighbor
                        best_time_diff = time_diff

                if best_time_diff < 0:
                    assignments = best_emp
                else: break 

            fitness = calculate_fitness(assignments, repair_times, travel_times)
            fitness_scores.append(fitness)

            if fitness > best_fitness:
                best_fitness = fitness
                best_assignments = assignments

        while len(new_population) < population_size:
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)
            child1 = ox_crossover(parent1, parent2)
            child2 = ox_crossover(parent2, parent1) 
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population
    
    return best_assignments, calculate_total_time(best_assignments, repair_times, travel_times)


# Test with file
if __name__=="__main__": 
    #inp = ['data_50_5.txt','data_50_7.txt','data_50_10.txt','data_50_20.txt','data_50_25.txt']
    inp = ['data_10_2.txt']
    for s in inp: 
        path_inp = './data/'+s 
        path_out = './result/result_local_search_GA/'+s
        fi = open(path_inp,'r') 
        output = open(path_out,'w')
        num_customers, num_employees = fi.readline().split(' ') 
        num_customers, num_employees = int(num_customers), int(num_employees) 
        customers = [i+1 for i in range(num_customers)]
        d = fi.readline().split(' ') 
        repair_times = { i+1: int(d[i]) for i in range(num_customers)}
        
        travel_times = [[] for i in range(num_customers+1)]
        for i in range(num_customers+1): 
            tmp = fi.readline().split(' ')
            travel_times[i] = [int(tmp[i]) for i in range(num_customers+1)]
        
        starttime = time() 
        population_size = 5  # Size of the population
        num_generations = 20  # Number of generations
        mutation_rate = 0.2  # Probability of mutation
        
        assignments, best_time = local_search_with_ga(
            customers,
            repair_times,
            travel_times,
            num_employees,
            population_size,
            num_generations,
            mutation_rate
        )
        endtime = time() 
        output.write("Objective value: "+str(best_time)+'\n')
        print("Running time "+str(endtime-starttime))
        output.write("Running time "+str(endtime-starttime)+'\n') 
        print("Minimum Total Time:", best_time)
        output.write("Solution"+'\n')
        print(num_employees)
        for emp in assignments.keys(): 
            print(len(assignments[emp]))
            print(0,end=' ') 
            output.write(str(0)+' ') 
            for task in assignments[emp]: 
                print(task,end=' ') 
                output.write(str(task)+' ')
            print(0)
            output.write(str(0)+'\n')
        output.close()
        print("Best Assignments:", assignments)
#Test with IO standard
'''

if __name__=="__main__": 

    num_customers, num_employees = input().split(' ')
    num_customers, num_employees = int(num_customers), int(num_employees) 
    customers = [i+1 for i in range(num_customers)]
    #d = fi.readline().split(' ') 
    d = input().split(' ') 
    repair_times = { i+1: int(d[i]) for i in range(num_customers)}
    
    travel_times = [[] for i in range(num_customers+1)]
    for i in range(num_customers+1): 
        #tmp = fi.readline().split(' ')
        tmp = input().split(' ')
        travel_times[i] = [int(tmp[i]) for i in range(num_customers+1)]
    population_size = 50  # Size of the population
    num_generations = 100  # Number of generations
    mutation_rate = 0.2  # Probability of mutation
    
    assignments, best_time = local_search_with_ga(
        customers,
        repair_times,
        travel_times,
        num_employees,
        population_size,
        num_generations,
        mutation_rate
    )
    print(num_employees)
    for emp in assignments.keys(): 
        print(len(assignments[emp])+2)
        print(0,end=' ') 
        for task in assignments[emp]: 
            print(task,end=' ') 
        print(0)
'''