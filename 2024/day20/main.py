import timeit 
import numpy as np
from pathlib import Path
from itertools import combinations
from collections import defaultdict

def preprocess(input_lines: list[int]):
    return [[n for n in line] for line in input_lines.split('\n')]

class Maze:
    def __init__(self, input):
        self.rows = len(input)
        self.columns = len(input[0])

        self.maze = [(c, r) for r, row in enumerate(input) for c, column in enumerate(row) if column != '#']

        self.start = [(row.index('S'), r)
                    for r, row in enumerate(input)
                    if 'S' in row][0]
        self.end = [(row.index('E'), r)
                    for r, row in enumerate(input)
                    if 'E' in row][0]
        
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        self.distance_to_target = {}
        self.shortcuts = defaultdict(int)

    def get_neighbours(self, current):      
        neighbours = []
        for index, direction in enumerate(self.directions):
            next_position = self.take_step(current, direction)

            if next_position in self.maze:
                neighbours.append(next_position)
        
        return neighbours
    
    def take_step(self, position, direction):
        return (position[0] + direction[0], position[1] + direction[1])

    def walk_maze(self): 
        found = [self.start]
        visited = set()
        parents = {}
        
        while found:
            current = found.pop(0)
            visited.add(current)

            if current == self.end:
                distance = 0
                while current in parents:
                    self.distance_to_target[current] = distance
                    current = parents[current]
                    distance += 1
                
                self.distance_to_target[self.start] = distance

                return True

            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                if neighbour in visited:
                    continue
                
                parents[neighbour] = current
                found.append(neighbour)

        return False
    
    def find_shortcuts(self, max_cheat):        
        for ((x1, y1), previous), ((x2, y2), next) in combinations(self.distance_to_target.items(), 2):
            distance = abs(x2 - x1) + abs(y2 - y1)
            if distance <= max_cheat:
                shortcut = abs(previous - next) - distance
                self.shortcuts[shortcut] += 1

    def get_shortcuts(self, cap):
        return sum([value for key, value in self.shortcuts.items() if key >= cap])

def first(input):
    maze = Maze(input)
    maze.walk_maze()
    maze.find_shortcuts(2)
    return maze.get_shortcuts(100)

def second(input):
    maze = Maze(input)
    maze.walk_maze()
    maze.find_shortcuts(20)
    return maze.get_shortcuts(100)

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day20"

    example = Path(path + '/example.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    print("Part 1 - Example input          ():", first(preprocess(example)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input          ():", second(preprocess(example)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s")