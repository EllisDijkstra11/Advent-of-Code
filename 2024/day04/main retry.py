from pathlib import Path
import regex as re
import timeit 

def preprocess(input_lines):
    return [n for n in input_lines.split('\n')]

class Xmas:
    def __init__(self, lines):
        self.lines = ".".join(lines)

        # The delimiter adds one in length, but excluding the necessary character removes one
        self.length = len(lines[0])
    
    def find_xmas(self):
        sum = 0
        # Horizontal
        sum += len(re.findall(r'XMAS|SAMX', self.lines, overlapped=True))

        # Vertical
        sum += len(re.findall(rf'X.{{{self.length}}}M.{{{self.length}}}A.{{{self.length}}}S', self.lines, overlapped=True))
        sum += len(re.findall(rf'S.{{{self.length}}}A.{{{self.length}}}M.{{{self.length}}}X', self.lines, overlapped=True))

        # Diagonal (/)
        sum += len(re.findall(rf'X.{{{self.length - 1}}}M.{{{self.length - 1}}}A.{{{self.length - 1}}}S', self.lines, overlapped=True))
        sum += len(re.findall(rf'S.{{{self.length - 1}}}A.{{{self.length - 1}}}M.{{{self.length - 1}}}X', self.lines, overlapped=True))

        # Diagonal (\)
        sum += len(re.findall(rf'X.{{{self.length + 1}}}M.{{{self.length + 1}}}A.{{{self.length + 1}}}S', self.lines, overlapped=True))
        sum += len(re.findall(rf'S.{{{self.length + 1}}}A.{{{self.length + 1}}}M.{{{self.length + 1}}}X', self.lines, overlapped=True))

        return sum
    
    def find_crosses(self):
        sum = 0

        sum += len(re.findall(rf'M.M.{{{self.length - 1}}}A.{{{self.length - 1}}}S.S', self.lines, overlapped=True))
        sum += len(re.findall(rf'S.S.{{{self.length - 1}}}A.{{{self.length - 1}}}M.M', self.lines, overlapped=True))
        sum += len(re.findall(rf'M.S.{{{self.length - 1}}}A.{{{self.length - 1}}}M.S', self.lines, overlapped=True))
        sum += len(re.findall(rf'S.M.{{{self.length - 1}}}A.{{{self.length - 1}}}S.M', self.lines, overlapped=True))

        return sum


def first(input):
    xmas = Xmas(input)
    return xmas.find_xmas()

def second(input):
    xmas = Xmas(input)
    return xmas.find_crosses()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day04"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (18):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input       (2644):", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input         (9):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input       (1952):", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")