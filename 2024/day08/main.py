import timeit 
import pprint
from operator import add, sub
from pathlib import Path
from collections import defaultdict

def preprocess(input_lines: list[int]):
    return [[place for place in row] for row in input_lines.split('\n')]

class Antennas:
    def __init__(self, input):
        self.rows = len(input)
        self.columns = len(input[0])
        self.antennas = defaultdict(list)
        self.anti_nodes = set()

        self.find_antennas(input)
    
    def get_anti_nodes(self):
        return len(self.anti_nodes)

    def find_antennas(self, input):
        for r, row in enumerate(input):
            for p, place in enumerate(row):
                self.antennas[place].append((p, r))

        del self.antennas["."]
    
    def position_exists(self, position):
        if not 0 <= position[0] < self.columns:
            return False
        
        elif not 0 <= position[1] < self.rows:
            return False
        
        return True
    
    def find_anti_nodes(self):
        for key, value in self.antennas.items():
            len_antennas = len(value)
            for i in range(len_antennas - 1):
                for j in range(i + 1, len_antennas):
                    distance = tuple(map(sub, value[j], value[i]))
                    first_antenna = tuple(map(sub, value[i], distance))
                    second_antenna = tuple(map(add, value[j], distance))
                    if self.position_exists(first_antenna):
                        self.anti_nodes.add(first_antenna)
                    if self.position_exists(second_antenna):
                        self.anti_nodes.add(second_antenna)

    def find_all_anti_nodes(self):
        for key, value in self.antennas.items():
            len_antennas = len(value)
            for i in range(len_antennas - 1):
                for j in range(i + 1, len_antennas):
                    distance = tuple(map(sub, value[j], value[i]))
                    
                    self.anti_nodes.add(value[i])
                    self.anti_nodes.add(value[j])
                    first_antenna = tuple(map(sub, value[i], distance))
                    while self.position_exists(first_antenna):
                        self.anti_nodes.add(first_antenna)
                        first_antenna = tuple(map(sub, first_antenna, distance))
                    
                    second_antenna = tuple(map(add, value[j], distance))
                    while self.position_exists(second_antenna):
                        self.anti_nodes.add(second_antenna)
                        second_antenna = tuple(map(add, second_antenna, distance))

def first(input):
    antennas = Antennas(input)
    antennas.find_anti_nodes()
    return antennas.get_anti_nodes()

def second(input):
    antennas = Antennas(input)
    antennas.find_all_anti_nodes()
    return antennas.get_anti_nodes()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day08"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (14):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")



    print("Part 2 - Example input        (34):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")