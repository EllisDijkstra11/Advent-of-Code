from pathlib import Path
import re
import timeit 

def preprocess(input_lines: list[int]):
    return [n for n in input_lines.split('\n')]

class Multiplications:
    def __init__(self, lines):
        self.lines = lines
    
    def find_multiplications(self):
        multiplications = []
        for line in self.lines:
            multiplication = re.findall(r'mul\(\d{1,3},\d{1,3}\)', line)
            multiplications.extend(multiplication)
        
        sum = 0
        for multiplication in multiplications:
            digits = re.findall(r'\d{1,3}', multiplication)
            sum += int(digits[0]) * int(digits[1])

        return sum
    
    def find_active_multiplications(self):
        multiplications = []
        for line in self.lines:
            multiplication = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", line)
            multiplications.extend(multiplication)
        
        sum = 0
        check = True
        for multiplication in multiplications:
            if multiplication == 'do()':
                check = True
            elif multiplication == 'don\'t()': 
                check = False
            elif check:
                digits = re.findall(r'\d{1,3}', multiplication)
                sum += int(digits[0]) * int(digits[1])

        return sum

def first(lines):
    multiplications = Multiplications(lines)
    return multiplications.find_multiplications()

def second(lines):
    multiplications = Multiplications(lines)
    return multiplications.find_active_multiplications()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day03"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input       (161):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input        (48):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")