from pathlib import Path
import timeit 
import numpy as np
import heapq

def preprocess(input_lines: list[int]):
    return [[int(n) for n in row] for row in input_lines.split('\n')]

class AStar:
    def __init__(self, cavern):
        self.cavern = cavern
        self.nodes = []
    
    def scale_map(self, n):
        height = len(self.cavern)
        width = len(self.cavern[0])
        expanded_map = []

        for new_y in range(n):
            for old_y in range(height):
                new_row = []
                for new_x in range(n):
                    for old_x in range(width):
                        value = self.cavern[old_y][old_x]

                        new_value = value + new_x + new_y

                        if new_value > 9:
                            new_value = new_value % 9 if new_value % 9 != 0 else 9

                        new_row.append(new_value)
                expanded_map.append(new_row)
        
        self.cavern = expanded_map

    def find_shortest_path(self):
        start = (0, 0)
        target = (len(self.cavern[0]) - 1, len(self.cavern) - 1)
        
        found = []
        visited = set()
        parents = {}
        cost = {}

        for y in range(len(self.cavern)):
            for x in range(len(self.cavern[0])):
                cost[(x, y)] = np.Infinity
        
        cost[(start)] = 0
        heapq.heappush(found, (self.distance_to_target(start, target), start))

        while found:
            _, current = heapq.heappop(found)
            visited.add(current)

            if current == target:
                total_cost = 0

                while current in parents:
                    x, y = current

                    total_cost += self.cavern[y][x]
                    current = parents[current]

                return total_cost

            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                if neighbour in visited:
                    continue
                
                x, y = neighbour
                new_cost = self.cavern[y][x] + cost[current]

                if new_cost < cost[neighbour]:
                    cost[neighbour] = new_cost
                    parents[neighbour] = current
                    current_distance = self.distance_to_target(neighbour, target) + new_cost
                    heapq.heappush(found, (current_distance, neighbour))
        
        return None

    def get_neighbours(self, current):
        x, y = current
        directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        
        neighbours = []
        for step_x, step_y in directions:
            next_x = x + step_x
            next_y = y + step_y
            next_position = (next_x, next_y)

            if (0 <= next_x < len(self.cavern[0]) and
                0 <= next_y < len(self.cavern)):

                neighbours.append(next_position)
        
        return neighbours

    def distance_to_target(self, current, target):
        return abs(current[0] - target[0]) + abs(current[1] - target[1])

def first(input):
    a_star = AStar(input)
    return a_star.find_shortest_path()

def second(input):
    a_star = AStar(input)
    a_star.scale_map(5)
    return a_star.find_shortest_path()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day15"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (40):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input       (315):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")