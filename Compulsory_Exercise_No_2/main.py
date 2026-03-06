"""
In this assignment , we are going to compare 2 local search methods used to solve the knapsack problem covered in the lecture.

 1- Generate a set of objects. Each object has a value and a weight. the weight is a random value between 1 and 5. The

      value of an object is a random value between 10 and 20. The capacity of the knapsack is set to 35.

  2- Choose one algorithm to generate a starting solution. You can choose algorithms based on sorting the objects

        according to their values or according to their weights.

 3.  Compare the local search algorithm version 2 with the local search algorithm version 5.

 4.   Compare the two algorithm using number of objects 500, 1500, 2000. The capacity remains the same (35 kg) 
"""

import random
import time

def generate_objects(num_objects):
    objects = []
    for _ in range(num_objects):
        weight = random.randint(1, 5)
        value = random.randint(10, 20)
        objects.append((weight, value))
    return objects

def sorting_algorithm(objects):
    return sorted(objects, key=lambda x: x[1] / x[0], reverse=True)



def local_search_greedy_improvement_version_2(objects, capacity, max_iterations=1000):
    sorted_indices = sorted(range(len(objects)), key=lambda i: objects[i][0])

    knapsack = set()
    old_weight = 0
    old_value = 0

    for i in sorted_indices:
        w, v = objects[i]
        if old_weight + w <= capacity:
            knapsack.add(i)
            old_weight += w
            old_value += v

    outside = set(range(len(objects))) - knapsack

    for _ in range(max_iterations):
        choice = random.randint(0, 1)

        if choice == 0:
            if knapsack and outside:
                x = random.choice(list(knapsack))
                y = random.choice(list(outside))

                new_weight = old_weight - objects[x][0] + objects[y][0]
                new_value = old_value - objects[x][1] + objects[y][1]
                diff = new_value - old_value

                if new_weight <= capacity and diff > 0:
                    old_value = new_value
                    knapsack.remove(x)
                    knapsack.add(y)
                    outside.remove(y)
                    outside.add(x)
                    old_weight = new_weight
                else:
                    if outside:
                        x = random.choice(list(outside))
                        new_weight = old_weight + objects[x][0]
                        if new_weight <= capacity:
                            knapsack.add(x)
                            outside.remove(x)
                            old_weight = new_weight
                            old_value = old_value + objects[x][1]


    return knapsack, old_value, old_weight


def local_search_greedy_improvement_version_5(objects, capacity, max_iterations=1000):
    sorted_indices = sorted(range(len(objects)), key=lambda i: objects[i][0])

    knapsack = set()
    current_weight = 0
    previous_total_value = 0

    for i in sorted_indices:
        w, v = objects[i]
        if current_weight + w <= capacity:
            knapsack.add(i)
            current_weight += w
            previous_total_value += v

    outside = set(range(len(objects))) - knapsack

    for _ in range(max_iterations):
        if not knapsack or not outside:
            break

        best_outside = max(outside, key=lambda i: objects[i][1] / objects[i][0])

        worst_inside = min(knapsack, key=lambda i: objects[i][1] / objects[i][0])

        new_weight = current_weight - objects[worst_inside][0] + objects[best_outside][0]
        new_total_value = previous_total_value - objects[worst_inside][1] + objects[best_outside][1]

        if new_weight <= capacity and new_total_value > previous_total_value:
            knapsack.remove(worst_inside)
            knapsack.add(best_outside)
            outside.remove(best_outside)
            outside.add(worst_inside)
            current_weight = new_weight
            previous_total_value = new_total_value

    return knapsack, previous_total_value, current_weight


if __name__ == "__main__":
    num_objects_list = [500, 1500, 2000]
    capacity = 35

    for num_objects in num_objects_list:
        objects = generate_objects(num_objects)

        start = time.time()
        knapsack_v2, value_v2, weight_v2 = local_search_greedy_improvement_version_2(objects, capacity)
        time_v2 = time.time() - start

        start = time.time()
        knapsack_v5, value_v5, weight_v5 = local_search_greedy_improvement_version_5(objects, capacity)
        time_v5 = time.time() - start

        print("\n")
        print(f"Number of objects: {num_objects}")
        print(f"Local search algorithm version 2 - Value: {value_v2}, Weight: {weight_v2}, Time: {time_v2:.4f}s")
        print(f"Local search algorithm version 5 - Value: {value_v5}, Weight: {weight_v5}, Time: {time_v5:.4f}s")

        print("\n")