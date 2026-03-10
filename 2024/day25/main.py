import regex as re
import timeit 
from pathlib import Path

def preprocess(input_lines):
    schematics = [[line for line in schematic.split('\n')] for schematic in input_lines.split('\n\n')]

    locks, keys = [], []
    for schematic in schematics:
        columns = [''.join(row[i] for row in schematic) for i in range(len(schematic[0]))]
        converted = [len(re.findall(r'#', column)) - 1 for column in columns]

        if schematic[0][0] == '#':
            locks.append(converted)
        else:
            keys.append(converted)
    
    return [locks, keys]

class Locks:
    def __init__(self, input):
        self.locks, self.keys = input

    def find_matches(self):
        fitting_keys = 0
        for lock in self.locks:
            for key in self.keys:
                if not any(l + k > 5 for l, k in zip(lock, key)):
                    fitting_keys += 1
        
        return fitting_keys

def first(input):
    locks = Locks(input)
    return locks.find_matches()

def second(input):
    return None

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day25"

    example = Path(path + '/example.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    print("Part 1 - Example input         (3):", first(preprocess(example)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    # print("Part 2 - Example input          ():", second(preprocess(example)))
    
    # start = timeit.default_timer()
    # print("Part 2 - Actual input             :", second(preprocess(input)))
    # print(f"Time taken: {timeit.default_timer()-start}s")