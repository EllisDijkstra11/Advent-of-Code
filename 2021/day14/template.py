from pathlib import Path
import timeit 
import numpy as np

def preprocess(input_lines: list[int]):
    polymer, changes = input_lines.split('\n\n')
    changes = changes.split('\n')

    insertions = []
    for change in changes:
        insertions.append(change.split(' -> '))
    return [polymer, insertions]

class Pair:
    def __init__(self, pair):
        self.pair = pair
        self.first_pair_string = ""
        self.second_pair_string = ""
        self.first_pair = None
        self.second_pair = None
        self.n_pairs = None

    def set_insertion(self, insertion):
        self.first_pair_string = self.pair[0] + insertion
        self.second_pair_string = insertion + self.pair[1]
    
    def find_class_pair(self, pairs):
        for pair in pairs:
            if pair.pair == self.first_pair_string:
                self.first_pair = pair
            elif pair.pair == self.second_pair_string:
                self.second_pair = pair
            
            if self.first_pair and self.second_pair:
                break

    def find_n_pairs(self, n):
        current_polymer = [self]
        for _ in range(n):
            new_polymer = []
            for pair in current_polymer:
                new_polymer.append(pair.first_pair)
                new_polymer.append(pair.second_pair)
            current_polymer = new_polymer
        self.n_pairs = current_polymer

    def return_n_pairs(self):
        return self.n_pairs

class Polymer:   
    def __init__(self, polymer, insertions):
        self.polymer = polymer
        self.class_polymer = []
        self.insertions = insertions
        self.possible_pairs = set()
        self.elements = set()
        self.class_pairs = []
    
    def execute_steps(self, n):
        for _ in range(n):
            self.alter_pairs()

    def find_pairs(self):
        for insertion in self.insertions:
            self.possible_pairs.add(insertion[0])
            self.elements.add(insertion[0][0])
            self.elements.add(insertion[0][1])
            pair = Pair(insertion[0])
            self.class_pairs.append(pair)
            pair.set_insertion(insertion[1])

        if len(self.possible_pairs) != len(self.class_pairs):
            print("Wow hier gaat iets mis")
        
        for pair in self.class_pairs:
            pair.find_class_pair(self.class_pairs)
        
        for index in range(len(self.polymer) - 1):
            current_pair = next((pair for pair in self.class_pairs if pair.pair == self.polymer[index:index + 2]))
            self.class_polymer.append(current_pair)

    def alter_pairs(self):
        # current_string = ""
        # for pair in self.class_polymer:
        #     current_string += pair.pair[0]
        # print(current_string)

        current_polymer = []
        for pair in self.class_polymer:
            current_polymer.append(pair.first_pair)
            current_polymer.append(pair.second_pair)
        self.class_polymer = current_polymer
        # print(len(self.class_polymer)/2)
        # current_string = ""
        # for pair in self.class_polymer:
        #     current_string += pair.pair[0]
        # print(current_string, "\n")
    
    def alter_pairs_in_sets(self, n, step):
        counts = {}
        for element in self.elements:
            counts[element] = 0

        for pair in self.class_pairs:
            pair.find_n_pairs(step)
        
        self.find_pairs_in_sets()
        for _ in range(int(n/step)):
            current_polymer = []
            for pair in self.class_polymer:
                current_polymer.extend(pair.n_pairs)
            self.class_polymer = current_polymer
    
    def find_pairs_in_sets(step):



    def find_strength(self):
        polymer = self.class_polymer[0].pair[0]
        for pair in self.class_polymer:
            polymer += pair.pair[1]
        

        minimal = np.Infinity
        maximal = 0
        for element in self.elements:
            current_count = int(polymer.count(element))
            minimal = min(current_count, minimal)
            maximal = max(current_count, maximal)
        return maximal - minimal

def first(input):
    polymer, insertions = input

    polymer = Polymer(polymer, insertions)
    polymer.find_pairs()
    polymer.execute_steps(10)
    return polymer.find_strength()

def second(input):
    polymer, insertions = input

    polymer = Polymer(polymer, insertions)
    polymer.find_pairs()
    polymer.alter_pairs_in_sets(40, 5)
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
    
    # start = timeit.default_timer()
    # print("Part 2 - Actual input                 :", second(preprocess(data)))
    # print(f"Time taken: {timeit.default_timer()-start}s")