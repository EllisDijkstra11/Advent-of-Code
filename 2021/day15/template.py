from pathlib import Path
import timeit 
import numpy as np

def preprocess(input_lines: list[int]):
    return [[int(n) for n in row] for row in input_lines.split('\n')]

class Node:
    def __init__(self, pos, cost):
        self.position = pos
        self.x = self.position[0]
        self.y = self.position[1]
        self.cost = cost
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def set_cost(self, cost):
        self.cost = cost

class AStar:
    def __init__(self, cavern):
        self.cavern = cavern
        self.nodes = []
        self.initialize_nodes()

    def initialize_nodes(self):
        for y in range(len(self.cavern)):
            for x in range(len(self.cavern[0])):
                node = Node((x, y), np.Infinity)
                self.nodes.append(node)
        
        self.nodes[0].set_cost(0)
    
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
        self.initialize_nodes()

    def find_shortest_path(self):
        found = [self.nodes[0]]
        visited = set()
        target = (len(self.cavern[0]) - 1, len(self.cavern) - 1)

        while found:
            # print(found, visited)
            found.sort()
            current = found.pop(0)
            visited.add(current)

            if current.position == target:
                return current.cost
            
            neighbours = self.get_neighbours(current)
            for neighbour_position in neighbours:
                neighbour = next((node for node in self.nodes if node.position == neighbour_position), None)

                if neighbour in visited or neighbour is None:
                    continue

                cost = current.cost + self.cavern[neighbour.y][neighbour.x]

                if neighbour.cost > cost:
                    neighbour.set_cost(cost)
                    if neighbour not in found:
                        found.append(neighbour)
        
        return None

    def get_neighbours(self, current):
        directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        
        neighbours = []
        for step_x, step_y in directions:
            next_x = current.x + step_x
            next_y = current.y + step_y
            next_position = (next_x, next_y)

            if (0 <= next_x < len(self.cavern[0]) and
                0 <= next_y < len(self.cavern)):

                neighbours.append(next_position)
        
        return neighbours

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