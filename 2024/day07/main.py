from pathlib import Path
from operator import add, mul
import timeit 
import re

cat = lambda x, y: int(str(x) + str(y))

def preprocess(input_lines: list[int]):
    return [re.findall(r'\d{1,20}', n) for n in input_lines.split('\n')]

class Calculator:
    def __init__(self, input):
        self.input = input
        self.total = 0
    
    def get_total(self):
        return self.total
    
    def first_operations(self):
        for input in self.input:
            self.do_first_operations(input)

    def second_operations(self):
        for input in self.input:
            self.do_second_operations(input)
        
    def do_first_operations(self, input):
        self.operations = []
        total = int(input[0])
        current_totals = [int(input[1])]
        digits = input[2:]

        for digit in digits:
            current_totals = [operation(current_total, int(digit)) for current_total in current_totals for operation in (add, mul)]
        
        if total in current_totals:
            self.total += total

    def do_second_operations(self, input):
        self.operations = []
        total = int(input[0])
        current_totals = [int(input[1])]
        digits = input[2:]

        for digit in digits:
            current_totals = [operation(current_total, int(digit)) for current_total in current_totals for operation in (add, mul, cat)]
        
        if total in current_totals:
            self.total += total

def first(input):
    calculator = Calculator(input)
    calculator.first_operations()
    return calculator.get_total()

def second(input):
    calculator = Calculator(input)
    calculator.second_operations()
    return calculator.get_total()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day07"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input      (3749):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input     (11387):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")