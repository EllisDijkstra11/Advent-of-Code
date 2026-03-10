import timeit 
import numpy as np
from pathlib import Path
from heapq import heappop, heappush
from collections import defaultdict

def preprocess(input_lines: list[int]):
    return [[n for n in line] for line in input_lines.split('\n')]

class Maze:
    def __init__(self, input):
        self.maze = [(c, r) for r, row in enumerate(input) for c, column in enumerate(row) if column != '#']

        self.start = [(row.index('S'), r)
                    for r, row in enumerate(input)
                    if 'S' in row][0]
        self.end = [(row.index('E'), r)
                    for r, row in enumerate(input)
                    if 'E' in row][0]
        
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        self.cost = np.inf
        self.seats = set()
    
    def get_cost(self):
        return self.cost
    
    def take_step(self, position, direction):
        return (position[0] + direction[0], position[1] + direction[1])

    def walk_maze(self):      
        found = []
        costs = defaultdict(lambda: np.inf)

        heappush(found, (0, 0, self.start, 1, [self.start]))

        while found:
            cost, _, current, direction, path = heappop(found)
            
            if cost > costs[current, direction]: continue
            else: costs[current, direction] = cost

            if current == self.end and cost <= self.cost:
                self.seats.update(path)
                self.cost = cost

            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                next_position, next_direction = neighbour

                if next_direction == direction:
                    new_cost = cost + 1
                else:
                    new_cost = cost + 1001
                
                heappush(found, (new_cost, self.distance_to_target(next_position), next_position, next_direction, path + [next_position]))

        return None

    def get_neighbours(self, current):      
        neighbours = []
        for index, direction in enumerate(self.directions):
            next_position = self.take_step(current, direction)

            if next_position in self.maze:
                neighbours.append((next_position, index))
        
        return neighbours

    def distance_to_target(self, current):
        dx = abs(current[0] - self.end[0])
        dy = abs(current[1] - self.end[1])
        if dx > 0 and dy > 0:
            return dx + dy + 1000
        
        return dx + dy

    def find_seats(self):
        return len(self.seats)

def first(input):
    maze = Maze(input)
    maze.walk_maze()
    return maze.get_cost()

def second(input):
    maze = Maze(input)
    maze.walk_maze()
    return maze.find_seats()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day16"

    example_one = Path(path + '/example_one.txt').read_text()
    example_two = Path(path + '/example_two.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    print("Part 1 - Example one input   (7036):", first(preprocess(example_one)))
    print("Part 1 - Example two input  (11048):", first(preprocess(example_two)))

    start = timeit.default_timer()
    print("Part 1 - Actual input      (102460):", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 1 - Example one input     (45):", second(preprocess(example_one)))
    print("Part 1 - Example two input     (64):", second(preprocess(example_two)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input         (527):", second(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s")