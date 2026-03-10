from pathlib import Path
import timeit 
import numpy as np
import re
import pprint
import copy

def preprocess(input_lines: list[int]):
    return [[n for n in line] for line in input_lines.split('\n')]

class Patrol:
    def __init__(self, input):
        self.floor = input
        self.loops = set()
        self.position = [[row.index("^"), r]
                         for r, row in enumerate(self.floor)
                         if "^" in row][0]
        self.floor[self.position[1]][self.position[0]] = '.'
        self.direction_index = 0
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.direction_markers = ['^', '>', 'v', '<']
    
    def get_field(self, position):
        return self.floor[position[1]][position[0]]

    def set_field(self, position, character):
        if self.get_field(position) == ".":
            self.floor[position[1]][position[0]] = character
        else:
            self.floor[position[1]][position[0]] += character

    def get_loops(self):
        print(self.loops)
        return len(self.loops)
    
    def position_exists(self, position):
        if not 0 <= position[0] < len(self.floor[0]):
            return False
        elif not 0 <= position[1] < len(self.floor):
            return False
        return True

    def patrol(self, original_path):
        next_position = np.add(self.position, self.directions[self.direction_index])
        while self.position_exists(next_position):
            self.set_field(self.position, self.direction_markers[self.direction_index])
            
            if self.get_field(next_position) == "#":
                self.direction_index = (self.direction_index + 1) % len(self.directions)
            else:
                if original_path:# and self.get_field(next_position) in ['.', '#']:
                    self.find_loops()              
                self.position = next_position

            next_position = np.add(self.position, self.directions[self.direction_index])

        self.set_field(self.position, self.direction_markers[self.direction_index])

    def first(self):
        total = len(self.floor) * len(self.floor[0])
        total -= sum([row.count(".") for row in self.floor])
        total -= sum([row.count("#") for row in self.floor])
        return total
    
    def find_loops(self):
        current_floor = copy.deepcopy(self.floor)
        position = self.position
        direction_index = (self.direction_index + 1) % len(self.directions)
        direction_marker = self.direction_markers[direction_index]
        next_position = self.position

        while self.position_exists(next_position):
            self.set_field(position, self.direction_markers[direction_index])

            if self.find_marker(position, self.directions[direction_index], direction_marker):
                self.loops.add(tuple(np.add(self.position, self.directions[self.direction_index])))
                break
            
            if self.get_field(next_position) == "#":
                direction_index = (direction_index + 1) % len(self.directions)
                direction_marker = self.direction_markers[direction_index]
            else:
                position = next_position

            next_position = np.add(position, self.directions[direction_index])
        
        self.floor = copy.deepcopy(current_floor)


    # def find_loops(self, position):
    #     current_index = self.direction_markers.index(self.get_field(position)[-1])
    #     next_index = (current_index + 1) % 4
    #     next_marker = self.direction_markers[next_index]

    #     if self.find_marker(position, self.directions[next_index], next_marker):
    #         self.loops += 1
    
    def find_marker(self, position, direction, marker):
        position = np.add(position, direction)
        while self.position_exists(position) and self.get_field(position) != "#":
            if marker in self.get_field(position):
                return True
            
            position = np.add(position, direction)
        return False

def first(input):
    patrol = Patrol(input)
    patrol.patrol(False)
    return patrol.first()

def second(input):
    patrol = Patrol(input)
    patrol.patrol(True)
    return patrol.get_loops()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day06"

    data_path_example = Path(path + '/example.txt')

    data_path_Franks_input = Path(path + '/input Frank.txt')
    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    Franks_data = data_path_Franks_input.read_text()
    data = data_path_input.read_text()

    # print("Part 1 - Example input        (41):", first(preprocess(example_data)))

    # start = timeit.default_timer()
    # print("Part 1 - Actual input       (5516):", first(preprocess(data)))
    # print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input         (6):", second(preprocess(example_data)))
    

    # start = timeit.default_timer()
    # print("Part 2 - Frank's input      (1622):", second(preprocess(Franks_data)))
    # print(f"Time taken: {timeit.default_timer()-start}s")

    print("Part 2 - Too low                  : 998")
    print("Part 2 - Too low                  : 1102")
    print("Part 2 - Too low                  : 1500")
    start = timeit.default_timer()
    print("Part 2 - Actual input       (2008):", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")