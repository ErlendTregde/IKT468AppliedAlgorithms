import random

class TSP:

    def __init__(self, num_cities):
        self.num_cities = num_cities
        self.distance_matrix = [[random.randint(3, 9) if i != j else 0 
                                for j in range(num_cities)] 
                               for i in range(num_cities)]
    

    def calculate_tour_length(self, tour):
        total = 0
        for i in range(len(tour) - 1):
            total += self.distance_matrix[tour[i]][tour[i + 1]]
        total += self.distance_matrix[tour[-1]][tour[0]]
        return total


class random_algorithm:    
    def __init__(self, tsp):
        self.tsp = tsp
    

    def construct_solution(self):
        tour = [random.randint(0, self.tsp.num_cities - 1)]
        visited = set(tour)
        
        while len(visited) < self.tsp.num_cities:
            city = random.randint(0, self.tsp.num_cities - 1)
            if city not in visited:
                visited.add(city)
                tour.append(city)
        
        return tour


class greedy_algorithm:
    
    def __init__(self, tsp):
        self.tsp = tsp
    

    def construct_solution(self):
        current = random.randint(0, self.tsp.num_cities - 1)
        tour = [current]
        visited = set(tour)
        
        while len(visited) < self.tsp.num_cities:
            min_dist = float('inf')
            closest = None
            
            for city in range(self.tsp.num_cities):
                if city not in visited:
                    dist = self.tsp.distance_matrix[current][city]
                    if dist < min_dist:
                        min_dist = dist
                        closest = city
            
            visited.add(closest)
            tour.append(closest)
            current = closest
        
        return tour


class local_search_algorithm:
    
    def __init__(self, tsp, max_iterations=1000):
        self.tsp = tsp
        self.max_iterations = max_iterations
    

    def optimize(self, tour):
        current_tour = tour.copy()
        current_length = self.tsp.calculate_tour_length(current_tour)
        no_improvement = 0
        
        for _ in range(self.max_iterations):
            i = random.randint(0, len(current_tour) - 2)
            k = random.randint(i + 1, len(current_tour) - 1)
            
            new_tour = current_tour.copy()
            new_tour[i:k+1] = reversed(new_tour[i:k+1])
            new_length = self.tsp.calculate_tour_length(new_tour)
            
            if new_length < current_length:
                current_tour = new_tour
                current_length = new_length
                no_improvement = 0
            else:
                no_improvement += 1
            
            if no_improvement >= 100:
                break
        
        return current_tour, current_length


if __name__ == "__main__":
    for num_cities in [100, 500, 1000]:
        print(f"\n{num_cities} cities:")
        print("-" * 40)
        
        tsp = TSP(num_cities)
        
        rm = random_algorithm(tsp)
        rm_tour = rm.construct_solution()
        rm_initial = tsp.calculate_tour_length(rm_tour)
        
        ls = local_search_algorithm(tsp)
        _, rm_final = ls.optimize(rm_tour)
        
        print(f"RM: {rm_initial} , {rm_final} (improved {rm_initial - rm_final})")
        
        gr = greedy_algorithm(tsp)
        gr_tour = gr.construct_solution()
        gr_initial = tsp.calculate_tour_length(gr_tour)
        
        ls = local_search_algorithm(tsp)
        _, gr_final = ls.optimize(gr_tour)
        
        print(f"GR: {gr_initial} , {gr_final} (improved {gr_initial - gr_final})")
        print(f"\nBest: {'GR' if gr_final < rm_final else 'RM'} ({min(gr_final, rm_final)})")