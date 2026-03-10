import re
import timeit 
from pathlib import Path

def preprocess(input_lines):
    claw_machines = input_lines.split('\n\n')
    return [[int(n) for n in re.findall(r'\d{1,6}', machine)] for machine in claw_machines]

class Machine:
    def __init__(self, input):
        self.claw_machines = input
        self.solutions = []
    
    def win_prizes(self, error):
        for machine in self.claw_machines:
            a_x, a_y, b_x, b_y, t_x, t_y = machine
            t_x = t_x + error
            t_y = t_y + error

            b = (t_y * a_x - a_y * t_x) // (b_y * a_x - b_x * a_y)
            a = (t_x - b_x * b) // a_x

            if a_x * a + b_x * b == t_x and a_y * a + b_y * b == t_y:
                self.solutions.append(a * 3 + b)
            else:
                self.solutions.append(0)

    def find_coins(self):
        return sum(self.solutions)


def first(input):
    machine = Machine(input)
    machine.win_prizes(0)
    return machine.find_coins()

def second(input):
    machine = Machine(input)
    machine.win_prizes(10000000000000)
    return machine.find_coins()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day13"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input       (480):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")