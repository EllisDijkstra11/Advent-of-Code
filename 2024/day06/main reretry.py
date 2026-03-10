from pathlib import Path
import timeit 
import numpy as np
import re
import pprint
import copy
import itertools
from collections import defaultdict

def preprocess(input_lines: list[int]):
    return [[n for n in line] for line in input_lines.split('\n')]

class Patrol:
    def __init__(self, input):
        self.floor = input
        self.loops = 0

        self.position = [(row.index("^"), r)
                         for r, row in enumerate(self.floor)
                         if "^" in row][0]
        self.next_position = self.position
        
        self.obstacles = list(itertools.chain(*[[(c, r) for c, column in enumerate(row) if column == '#'] for r, row in enumerate(self.floor)]))

        self.jump_map = dict()
        self.find_jump_map()

        self.visited = {
            0: [],              # up
            1: [],              # right
            2: [],              # down
            3: []               # left
        }

        self.direction_index = 0
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    def get_field(self, position):
        return [key for key, value in self.visited.items() if value == position]

    def get_loops(self):
        print(self.loops)
        return len(self.loops)
    
    def get_next_location(self, position, index):
        return (position[0] + self.directions[index][0], position[1] + self.directions[index][1])
    
    def get_visited_positions(self):
        total = set(itertools.chain(*[[value for value in values] for key, values in self.visited.items()]))
        return len(total)
    
    def position_exists(self, position):
        if not 0 <= position[0] < len(self.floor[0]):
            return False
        elif not 0 <= position[1] < len(self.floor):
            return False
        return True
    
    def find_jump_map(self):
        for r, row in enumerate(self.floor):
            for c, column in enumerate(row):
                self.jump_map[(c, r)] = [None, None, None, None]
        
        self.obstacles.sort(key=lambda p: p[1])
        for i in range(len(self.obstacles) - 1):
            fx, fy = self.obstacles[i]
            sx, sy = self.obstacles[i + 1]
            
            if fy == sy:
                for j in range(fx + 1, sx):
                    self.jump_map[(j, fy)][1] = (sx - 1, fy)
                    self.jump_map[(j, fy)][3] = (fx + 1, fy)

            else:
                for j in range(fx + 1, len(self.floor[0])):
                    self.jump_map[(j, fy)][3] = (fx + 1, fy)
                
                for j in range(0, sx - 1):
                    self.jump_map[(j, sy)][1] = (sx - 1, sy)

        self.obstacles.sort(key=lambda p: p[0])
        for i in range(len(self.obstacles) - 1):
            fx, fy = self.obstacles[i]
            sx, sy = self.obstacles[i + 1]

            if fx == sx:
                for j in range(fy + 1, sy):
                    self.jump_map[(fx, j)][0] = (fx, fy + 1)
                    self.jump_map[(fx, j)][2] = (fx, sy - 1)

            else:
                for j in range(fy + 1, len(self.floor)):
                    self.jump_map[(fx, j)][0] = (fx, fy + 1)
                
                for j in range(0, sy - 1):
                    self.jump_map[(sx, j)][2] = (sx, sy - 1)

    def patrol(self):
        self.next_position = self.get_next_location(self.position, self.direction_index)

        while self.position_exists(self.position):
            self.visited[self.direction_index].append(self.position)

            if not self.next_position in self.obstacles: 
                self.position = self.next_position
                self.next_position = self.get_next_location(self.position, self.direction_index)

            else:
                self.direction_index = (self.direction_index + 1) % len(self.directions)
                self.next_position = self.get_next_location(self.position, self.direction_index)

    def jump(self):
        self.next_position = self.jump_map[self.position][self.direction_index]

        while self.next_position:
            for position in range(self.position, self.next_position):
                direction_index = self.direction_index + 1
                next_position = self.jump_map[position][direction_index]

                while next_position:
                    direction_index = (direction_index + 1) % len(self.directions)
                    next_position = self.jump_map[position][direction_index]

                    if next_position in self.visited[direction_index]:
                        self.loops += 1
            
            self.position = self.next_position
            self.next_position = self.jump_map[self.position][self.direction_index]

def first(input):
    patrol = Patrol(input)
    patrol.patrol()
    return patrol.get_visited_positions()

def second(input):
    patrol = Patrol(input)
    patrol.jump()
    return patrol.get_loops()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day06"

    data_path_example = Path(path + '/example.txt')

    data_path_Franks_input = Path(path + '/input Frank.txt')
    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    Franks_data = data_path_Franks_input.read_text()
    data = data_path_input.read_text()

    print("Part 1 - Example input        (41):", first(preprocess(example_data)))

    # start = timeit.default_timer()
    # print("Part 1 - Actual input       (5516):", first(preprocess(data)))
    # print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input         (6):", second(preprocess(example_data)))
    

    # start = timeit.default_timer()
    # print("Part 2 - Frank's input      (1622):", second(preprocess(Franks_data)))
    # print(f"Time taken: {timeit.default_timer()-start}s")

    start = timeit.default_timer()
    # print("Part 2 - Actual input       (2008):", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")