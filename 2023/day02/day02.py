from pathlib import Path
from pprint import pprint 

def preprocess(input_lines: list[int]):
    lines = input_lines.split("\n")
    loose_lines = []
    for line in lines:
        loose_lines.append(line.split(" "))
    return loose_lines


def first(lines):
    maximum_red = 12
    maximum_green = 13
    maximum_blue = 14
    total_sum = 0
    for line in lines:
        index = 3
        possible = True
        while index in range(len(line)):
            if "red" in line[index] and int(line[index - 1]) > maximum_red:
                possible = False
            elif "green" in line[index] and int(line[index - 1]) > maximum_green:
                possible = False
            elif "blue" in line[index] and int(line[index - 1]) > maximum_blue:
                possible = False
            index += 2

        if possible:
            total_sum += int(line[1][:- 1])
    return total_sum


def second(lines):
    total_sum = 0
    for line in lines:
        maximum_red = 0
        maximum_green = 0
        maximum_blue = 0
        index = 3
        while index in range(len(line)):
            if "red" in line[index] and int(line[index - 1]) > maximum_red:
                maximum_red = int(line[index - 1])
            elif "green" in line[index] and int(line[index - 1]) > maximum_green:
                maximum_green = int(line[index - 1])
            elif "blue" in line[index] and int(line[index - 1]) > maximum_blue:
                maximum_blue = int(line[index - 1])
            index += 2

        power = maximum_red * maximum_blue * maximum_green
        total_sum += power
    return total_sum


if __name__ == "__main__":
    path = "2023/day02"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print("Part 1 - Example: ", first(preprocess(example_data)))
    print("Part 1 - Actual:  ", first(preprocess(data)))
    print("Part 2 - Example: ", second(preprocess(example_data)))
    print("Part 2 - Actual:  ", second(preprocess(data)))
    