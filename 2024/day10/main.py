import timeit 
import itertools
import numpy as np
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [[int(n) for n in line] for line in input_lines.split('\n')]

class Paths:
    def __init__(self, input):
        self.map = input
        self.trailheads = [[(c, r) for c, column in enumerate(row) if column == 0] for r, row in enumerate(self.map)]
        self.trailheads = list(itertools.chain(*self.trailheads))
        self.paths = []
        self.distinct_paths = []
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    def get_field(self, postition):
        return self.map[postition[1]][postition[0]]
    
    def sum_paths(self):
        return sum(self.paths)

    def sum_distinct_paths(self):
        return sum(self.distinct_paths)
    
    def position_exists(self, position):
        if not 0 <= position[0] < len(self.map[0]):
            return False
        elif not 0 <= position[1] < len(self.map):
            return False
        return True
    
    def find_paths(self):
        for trailhead in self.trailheads:
            paths = set()
            distinct_paths = 0
            found = [trailhead]

            while found:
                current_position = found.pop(0)
                current_value = self.get_field(current_position)

                if current_value == 9:
                    distinct_paths += 1
                    paths.add(tuple(current_position))

                else:                 
                    for direction in self.directions:
                        next_position = np.add(current_position, direction)

                        if self.position_exists(next_position):
                            next_value = self.get_field(next_position)
                            
                            if next_value - current_value == 1:
                                found.append(next_position)
            
            self.paths.append(len(paths))
            self.distinct_paths.append(distinct_paths)

def first(input):
    paths = Paths(input)
    paths.find_paths()
    return paths.sum_paths()

def second(input):
    paths = Paths(input)
    paths.find_paths()
    return paths.sum_distinct_paths()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day10"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (36):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input        (81):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")