import os
import timeit 
from pathlib import Path
from collections import defaultdict

def preprocess(input_lines: list[int]):
    towels, designs = input_lines.split('\n\n')

    return [towels.split(', '), designs.split('\n')]

class Towels:
    def __init__(self, input):
        self.start_towels, self.designs = input
        self.towels = {}
        self.matches = []
    
    def get_possible_matches(self):
        return len(self.matches)
    
    def get_matches(self):
        return sum(self.matches)
    
    def match_designs(self):
        for design in self.designs:
            matches = self.match_design(design)
            if matches > 0:
                self.matches.append(matches)

    def match_design(self, design):
        if design in self.towels:
            return self.towels[design]

        if len(design) == 0:
            return 1

        ways = 0

        for towel in self.start_towels:
            if design.startswith(towel):
                ways += self.match_design(design[len(towel):])
        
        self.towels[design] = ways
        return ways

def first(input):
    towels = Towels(input)
    towels.match_designs()
    return towels.get_possible_matches()

def second(input):
    towels = Towels(input)
    towels.match_designs()
    return towels.get_matches()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day19"

    example = Path(path + '/example.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    print("Part 1 - Example input         (6):", first(preprocess(example)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input        (16):", second(preprocess(example)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s")