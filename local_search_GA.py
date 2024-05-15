import random

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
    for old_emp in assignments.keys():
        for old_cust in assignments[old_emp]: 
            for new_emp in range(num_employees):
                #if old_emp != new_emp:
                new_assignments ={emp :assignments[emp].copy() for emp in assignments.keys()} 
                new_assignments[old_emp].remove(old_cust)
                new_assignments[new_emp].append(old_cust)
                neighbors.append(new_assignments)
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


def local_search_with_ga(customers, repair_times, travel_times, num_employees, population_size, num_generations, mutation_rate):
    population = generate_initial_population(customers, num_employees, population_size)

    best_fitness = 0
    best_assignments = None

    for _ in range(num_generations):
        fitness_scores = []
        new_population = []

        for assignments in population:
            # Perform local search on each individual
            for _ in range(1000):  # Local search iterations
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
            child1, child2 = parent1.copy(), parent2.copy()
            mutation(child1, mutation_rate)
            mutation(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population
    
    return best_assignments, calculate_total_time(best_assignments, repair_times, travel_times)

# Example usage
fi = open('./data/data_10_5.txt','r') 
num_customers, num_employees = fi.readline().split(' ') 
num_customers, num_employees = int(num_customers), int(num_employees) 
customers = [i+1 for i in range(num_customers)]
d = fi.readline().split(' ') 
repair_times = { i+1: int(d[i]) for i in range(num_customers)}
travel_times = [[] for i in range(num_customers+1)]
for i in range(num_customers+1): 
    tmp = fi.readline().split(' ')
    travel_times[i] = [int(tmp[i]) for i in range(num_customers+1)]
population_size = 50  # Size of the population
num_generations = 100  # Number of generations
mutation_rate = 0.2  # Probability of mutation

best_assignments, best_time = local_search_with_ga(
    customers,
    repair_times,
    travel_times,
    num_employees,
    population_size,
    num_generations,
    mutation_rate
)

print("Best Assignments:", best_assignments)
print("Minimum Total Time:", best_time)