from pathlib import Path
import timeit 
import numpy as np
import re
import pprint

def preprocess(input_lines: list[int]):
    return [[n for n in line] for line in input_lines.split('\n')]

class Patrol:
    def __init__(self, input):
        self.floor = input
        self.loops = []
        self.position = [[row.index("^"), r]
                         for r, row in enumerate(self.floor)
                         if "^" in row][0]
        self.direction_index = 0
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.direction_markers = ['^', '>', 'v', '<']
    
    def get_field(self, place):
        return self.floor[place[1]][place[0]]

    def set_field(self, place, character):
        self.floor[place[1]][place[0]] = character
    
    def get_loops(self):
        print(self.loops)
        return len(self.loops)

    def patrol(self):
        next_position = np.add(self.position, self.directions[self.direction_index])
        while 0 <= next_position[0] < len(self.floor[0]) and 0 <= next_position[1] < len(self.floor):
            if self.get_field(next_position) == "#":
                self.direction_index = (self.direction_index + 1) % len(self.directions)
            else:
                self.set_field(self.position, self.direction_markers[self.direction_index])
                self.second(self.position)              
                self.position = next_position
            next_position = np.add(self.position, self.directions[self.direction_index])

        self.set_field(self.position, self.direction_markers[self.direction_index])

    def first(self):
        total = sum([row.count("^") for row in self.floor])
        total += sum([row.count(">") for row in self.floor])
        total += sum([row.count("v") for row in self.floor])
        total += sum([row.count("<") for row in self.floor])
        return total

    def second(self, place):
        current_index = self.direction_markers.index(self.get_field(place))
        next_index = (current_index + 1) % 4
        next_marker = self.direction_markers[next_index]
        next_position = np.add(place, self.directions[next_index])
        if next_marker == '^' or next_marker == "v":
            if any(row[place[0]] == next_marker for row in self.floor):
                self.loops.append(np.add(place, self.directions[current_index]))
                print(self.loops[-1])
        elif next_marker in self.floor[place[1]]:
            self.loops.append(np.add(place, self.directions[current_index]))
            print(self.loops[-1])

def first(input):
    patrol = Patrol(input)
    patrol.patrol()
    return patrol.first()

def second(input):
    patrol = Patrol(input)
    patrol.patrol()
    return patrol.get_loops()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day06"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (41):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input         (6):", second(preprocess(example_data)))
    
    print("Part 2 - Too low                  : 998")
    print("Part 2 - Too low                  : 1102")
    print("Part 2 - Too low                  : 1500")
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")