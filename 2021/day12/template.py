import timeit 
from pathlib import Path
from itertools import chain
import pprint

def preprocess(input_lines: list[int]):
    return [[n for n in line.split('-')] for line in input_lines.split('\n')]

class Caves:
    def __init__(self, passages):
        self.passages = passages
        self.paths = []
        self.caves = set(chain.from_iterable(self.passages))
    
    def find_connections(self, revisit):
        temporary_paths = [["start"]]
        # while not all(path[-1] == "end" for path in temporary_paths):
        while temporary_paths:
            current_path = temporary_paths.pop(0)
            last_cave = current_path[-1]

            if not last_cave == "end":
                # print("\n", current_path, "\nCurrent paths:")
                current_paths = []

                for cave in self.caves:
                    if not cave == "start":
                        if [last_cave, cave] in self.passages or [cave, last_cave] in self.passages:
                            current_paths.append(current_path + [cave])

                # pprint.pprint(current_paths)
                valid_paths = []
                for path in current_paths:
                    if not revisit and self.is_valid_path(path):
                        valid_paths.append(path)
                    elif revisit and self.is_valid_revisit_path(path):
                        valid_paths.append(path)

                temporary_paths.extend(valid_paths)
                
            elif not current_path in self.paths:
                self.paths.append(current_path)
            # pprint.pprint(self.paths) 

    def is_valid_path(self, path):
        for cave in self.caves:
            if cave.islower() and path.count(cave) > 1:
                return False
        
        return True

    def is_valid_revisit_path(self, path):
        revisit = False

        for cave in self.caves:
            if cave.islower() and path.count(cave) == 2 and not revisit:
                revisit = True
            elif cave.islower() and path.count(cave) > 1:
                return False
        
        return True

    def get_number_of_paths(self):
        # pprint.pprint(self.paths)
        return len(self.paths)




def first(passages):
    caves = Caves(passages)
    caves.find_connections(False)
    return caves.get_number_of_paths()

def second(passages):
    caves = Caves(passages)
    caves.find_connections(True)
    return caves.get_number_of_paths()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day12"

    data_path_example_one = Path(path + '/example_one.txt')
    data_path_example_two = Path(path + '/example_two.txt')
    data_path_example_three = Path(path + '/example_three.txt')

    data_path_input = Path(path + '/input.txt')

    example_data_one = data_path_example_one.read_text()
    example_data_two = data_path_example_two.read_text()
    example_data_three = data_path_example_three.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (10):", first(preprocess(example_data_one)))
    print("Part 1 - Example input        (19):", first(preprocess(example_data_two)))
    print("Part 1 - Example input       (226):", first(preprocess(example_data_three)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input        (36):", second(preprocess(example_data_one)))
    print("Part 2 - Example input       (103):", second(preprocess(example_data_two)))
    print("Part 2 - Example input      (3509):", second(preprocess(example_data_three)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")