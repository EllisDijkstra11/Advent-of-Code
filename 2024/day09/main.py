from pathlib import Path
import timeit 
import itertools

def preprocess(input_lines: list[int]):
    return [int(n) for n in input_lines]

class Amphipod:
    def __init__(self, input):
        self.input = input
        self.files = []
        self.blocks = []

    
    def find_blocks(self):
        index = 0
        while self.input:
            current_file = self.input.pop(0)
            current_block = []

            for _ in range(current_file):
                current_block.append(index)

            if current_block:
                self.files.extend(current_block)
                self.blocks.append(current_block)
            
            index += 1
            
            if self.input:
                current_space = self.input.pop(0)
                current_block = []

                for _ in range(current_space):
                    current_block.append('.')

                if current_block:
                    self.files.extend(current_block)
                    self.blocks.append(current_block)

    def move_files(self):
        index = 0
        while '.' in self.files:# and index < len(self.files):
            if self.files[index] == '.':
                last_block = self.files.pop()

                while last_block == '.':
                    last_block = self.files.pop()
                
                self.files[index] = last_block
            
            index += 1
    
    def move_blocks(self):
        for i in range(len(self.blocks) - 1, -1, -1):
            last_block = self.blocks[i].copy()
            # print("\n", last_block)
            if last_block[0] != ".":
                len_last_block = len(last_block)

                for j in range(0, i):
                    if len(self.blocks[j]) >= len_last_block and self.blocks[j][0] == '.':
                        
                        for k in range(len_last_block):
                            self.blocks[i][k] = '.'

                        len_space_block = len(self.blocks[j])
                        len_space = len_space_block - len_last_block
                        self.blocks[j] = last_block

                        # print(i, j, last_block, len_last_block, len_space_block)
                        if len_space > 0:
                            self.blocks.insert(j + 1, ['.'] * len_space)

                            # print("\n", last_block, self.blocks[j], len_space_block, self.blocks[j+1], self.blocks[i])
                        break
        self.blocks = list(itertools.chain(*self.blocks))
    
    def calculate_blocks(self, files):
        sum = 0
        for index, number in enumerate(files):
            if number != '.':
                sum += index * number
        
        return sum

def first(input):
    amphipod = Amphipod(input)
    amphipod.find_blocks()
    amphipod.move_files()
    return amphipod.calculate_blocks(amphipod.files)

def second(input):
    amphipod = Amphipod(input)
    amphipod.find_blocks()
    amphipod.move_blocks()
    return amphipod.calculate_blocks(amphipod.blocks)

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day09"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input      (1928):", first(preprocess(example_data)))

    start = timeit.default_timer()
    #print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input      (2858):", second(preprocess(example_data)))
    
    print("Part 2 - Too high                 : 6509444792719")
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")