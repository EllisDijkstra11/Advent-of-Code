from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    input_commands = input_lines.split('\n')
    commands = []
    for command in input_commands:
        direction, distance = command.split(' ')
        commands.append([direction, int(distance)])
    return commands

def first(commands):
    horizontal = 0
    depth = 0

    for command in commands:
        direction, distance = command
        if direction == "up":
            depth -= distance
        elif direction == "down":
            depth += distance
        else:
            horizontal += distance
    return horizontal * depth

def second(commands):
    horizontal = 0
    depth = 0
    aim = 0

    for command in commands:
        direction, distance = command
        if direction == "up":
            aim -= distance
        elif direction == "down":
            aim += distance
        else:
            horizontal += distance
            depth += aim * distance
    return horizontal * depth

if __name__ == "__main__":
    path = "2021/day02"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input       (150):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input       (900):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")