from pathlib import Path
import timeit 
import numpy as np
from collections import Counter

def preprocess(input_lines: list[int]):
    polymer, changes = input_lines.split('\n\n')
    changes = changes.split('\n')

    insertions = []
    for change in changes:
        insertions.append(tuple(change.split(' -> ')))
    return [polymer, insertions]

class Polymer:   
    def __init__(self, polymer, insertions):
        self.elements = set()
        self.pairs = set()

        for insertion in insertions:
            self.pairs.add(insertion[0])
            self.elements.add(insertion[0][0])
            self.elements.add(insertion[0][1])

        self.insertions = {}
        for insertion in insertions:
            self.insertions[insertion[0]] = insertion[1]

        self.counter = Counter({pair: 0 for pair in self.pairs})
        self.character_counter = Counter({element: 0 for element in self.elements})

        for index in range(len(polymer)-1):
            self.counter[polymer[index:index + 2]] += 1

    def execute_steps(self, n):
        for _ in range(n):
            for (first, second), count in self.counter.copy().items():
                insertion = self.insertions[first + second]
                self.counter[first + second] -= count
                self.counter[first + insertion] += count
                self.counter[insertion + second] += count
                self.character_counter[insertion] += count

    def find_strength(self):
        return max(self.character_counter.values()) - min(self.character_counter.values()) + 1

def first(input):
    polymer, insertions = input

    polymer = Polymer(polymer, insertions)
    polymer.execute_steps(10)
    return polymer.find_strength()

def second(input):
    polymer, insertions = input

    polymer = Polymer(polymer, insertions)
    polymer.execute_steps(40)
    return polymer.find_strength()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day14"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input          (1588):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input                 :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input (2188189693529):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input                 :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")