from pathlib import Path
import timeit 
import itertools

def preprocess(input_lines: list[int]):
    return [int(n) for n in input_lines]

class Amphipod:
    def __init__(self, input):
        self.input = input
        self.blocks = input[0::2]
        self.spaces = input[1::2]
        self.files = []

    def move_files(self):
        for index, (blocks, spaces) in enumerate(zip(self.blocks, self.spaces)):
            self.files += [index] * blocks
            self.blocks[index] = 0

            for second_index, block in enumerate(reversed(self.blocks)):
                if spaces > 0:
                    second_index = len(self.blocks) - second_index - 1
                    if 0 < block <= spaces:
                        self.files += [second_index] * block
                        self.blocks[second_index] = 0
                        spaces -= block
                    elif block > 0:
                        self.files += [second_index] * spaces
                        self.blocks[second_index] -= spaces
                        spaces = 0

    
    def move_blocks(self):
        for index, (blocks, spaces) in enumerate(zip(self.blocks, self.spaces)):
            if blocks > 0:
                self.files += [index] * blocks
            else:
                self.files += [0] * abs(blocks)
            self.blocks[index] = 0

            while spaces > 0:
                for second_index, block in enumerate(reversed(self.blocks)):
                    second_index = len(self.blocks) - second_index - 1
                    if 0 < block <= spaces:
                        self.files += [second_index] * block
                        spaces -= block
                        self.blocks[second_index] = -block
                        break
                else:
                    self.files += [0] * spaces
                    spaces = 0
    
    def calculate_blocks(self):
        sum = 0
        for index, number in enumerate(self.files):
            sum += index * number
        
        return sum

def first(input):
    amphipod = Amphipod(input)
    amphipod.move_files()
    return amphipod.calculate_blocks()

def second(input):
    amphipod = Amphipod(input)
    amphipod.move_blocks()
    return amphipod.calculate_blocks()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day09"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input      (1928):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input      (2858):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")