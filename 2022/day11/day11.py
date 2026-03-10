from pathlib import Path
from pprint import pprint 

class Monkey:
    id: int
    items: list[int]
    division_value: int
    true_monkey: int
    false_monkey: int
    worry_operation: str
    total_inspections: int

    def __post_init__(self):
        


def preprocess(input_lines: list[int]):
    monkeys = input_lines.split("\n\n")
    for monkey in monkeys:
        monkey_actions = monkey.split("\n")

    return commands


def first(commands):
    register_values = get_register_values(commands)
    sum = 0

    for index in range(20, 260, 40):
        sum += int(register_values[index - 1] * index)
            
    return sum
    

def second(commands):
    pass

if __name__ == "__main__":
    path = "2022/day11"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(example_data)))
    print(first(preprocess(data)))
    print(second(preprocess(example_data)))
    print(second(preprocess(data)))
    