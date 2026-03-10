import re
import timeit 
from pathlib import Path
from operator import mul
from functools import reduce

def preprocess(input_lines: list[int]):
    return [[int(n) for n in re.findall(r'\-?\d{1,3}', line)] for line in input_lines.split('\n')]

class Robots:
    def __init__(self, input):
        self.robots = input
        self.positions = []
        self.quadrants = [0, 0, 0, 0]
        self.width = 101
        self.height = 103
    
    def move_robots(self, step):
        for robot in self.robots:
            x, y, dx, dy = robot
        
            pos_x = (x + dx * step) % self.width
            pos_y = (y + dy * step) % self.height
            self.positions.append((pos_x, pos_y))

    def find_safety_factor(self):
        for position in self.positions:
            pos_x, pos_y = position
            sep_x = self.width//2
            sep_y = self.height//2
            index = 0
            if pos_x == sep_x or pos_y == sep_y:
                continue
            
            if pos_x > sep_x:
                index += 1
            if pos_y > sep_y:
                index += 2

            self.quadrants[index] += 1
    
        return reduce(mul, self.quadrants)

    def find_easter_egg(self):
        step = 0
        while True:
            self.positions = []
            self.move_robots(step)
            
            if len(self.positions) == len(set(self.positions)):
                return step
            
            step += 1

def first(input):
    robots = Robots(input)
    robots.move_robots(100)
    return robots.find_safety_factor()

def second(input):
    robots = Robots(input)
    return robots.find_easter_egg()


if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day14"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input          ():", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")