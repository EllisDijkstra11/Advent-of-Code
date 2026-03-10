from pathlib import Path
import re
import timeit 

def preprocess(input_lines):
    return [n for n in input_lines.split('\n')]

class Xmas:
    def __init__(self, lines):
        self.lines = lines
        self.strings = []
    
    def find_different_strings(self):
        # Horizontal
        self.strings.append(self.lines)

        # Vertical
        current_strings = [""]
        for index in range(len(self.lines[0])):
            for line in self.lines:
                current_strings[-1] += line[index:index + 1]
            current_strings.append("")
        
        self.strings.append(current_strings)
        self.find_diagonals(self.lines.copy())

    def find_diagonals(self, lines):
        # Diagonal (/)
        current_strings = self.find_diagonal(lines.copy())
        self.strings.append(current_strings)

        # Diagonal (\)
        reversed_lines = lines.copy()
        reversed_lines.reverse()
        current_strings = self.find_diagonal(reversed_lines)
        self.strings.append(current_strings)


    def find_diagonal(self, lines):
        current_strings = [""]
        index = 0
        current_index = 0

        while lines:
            current_strings[-1] += lines[index][0]
            lines[index] = lines[index][1:]
            index -= 1

            if index < 0:
                if lines[0] == "":
                    lines = lines[1:]
                else:
                    current_index += 1

                if current_index >= len(lines):
                    current_index = len(lines) - 1
                index = current_index

                current_strings.append("")
        return current_strings
    
    def find_xmas(self):
        sum = 0
        for strings in self.strings:
            for string in strings:
                sum += len(re.findall(r'XMAS', string))
                sum += len(re.findall(r'SAMX', string))

        return sum
    
    def find_crosses(self):
        sum = 0
        for row in range(len(self.lines) - 2):
            for column in range(len(self.lines[0]) - 2):
                square = []
                for index in range(3):
                    square.append(self.lines[row + index][column:column + 3])
                self.strings = []
                self.find_diagonals(square)
                
                mas = 0
                sam = 0
                for diagonal in self.strings:
                    mas += len(re.findall(r'MAS', diagonal[2]))
                    sam += len(re.findall(r'SAM', diagonal[2]))
                
                if (sam == 1 and mas == 1) or sam == 2 or mas == 2:
                    sum += 1
        
        return sum

def first(input):
    xmas = Xmas(input)
    xmas.find_different_strings()
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
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")