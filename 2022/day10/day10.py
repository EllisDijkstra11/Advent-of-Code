from pathlib import Path
from pprint import pprint 

def preprocess(input_lines: list[int]):
    commands = input_lines.split("\n")
    return commands


def first(commands):
    register_values = get_register_values(commands)
    sum = 0

    for index in range(20, 260, 40):
        sum += int(register_values[index - 1] * index)
            
    return sum
    

def second(commands):
    register_values = get_register_values(commands)
    for y in range(6):
        current_line = ""
        for x in range(40):
            current_pixel = x + y * 40
            current_register_value = register_values[current_pixel]
            current_sprite_location = [current_register_value - 1, current_register_value, current_register_value + 1]
            # print(current_pixel, current_sprite_location)
            if x in current_sprite_location:
                current_line = current_line + "#"
            else:
                current_line = current_line + "."
        print(current_line)


def get_register_values(commands):
    register = [1]
    for command in commands:
        if "addx" in command:
            new_value = int(command.split(" ")[1]) + int(register[-1])
            register.extend([register[-1], new_value])
        else:
            register.append(register[-1])
    return register


if __name__ == "__main__":
    data_path_example = Path('2022/day10/example.txt')
    data_path_input = Path('2022/day10/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(example_data)))
    print(first(preprocess(data)))
    print(second(preprocess(example_data)))
    print(second(preprocess(data)))
    