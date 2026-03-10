from pathlib import Path
from pprint import pprint
import re

def preprocess(input_lines: list[int]):
    instructions, coordinates = input_lines.split("\n\n")
    lines = coordinates.splitlines()

    coordinates = []
    for line in lines:
        coordinates.append(re.split("\W+", line))

    for coordinate in coordinates:
        while "" in coordinate:
            coordinate.remove("")

    return [instructions, coordinates]

def first(all_info):
    instructions = all_info[0]
    coordinates = all_info[1]

    index = 0
    steps = 0
    current_node = "AAA"

    while current_node != "ZZZ":
        for coordinate in coordinates:
            if coordinate[0] == current_node:
                if instructions[index] == "L":
                    current_node = coordinate[1]
                    break
                else:
                    current_node = coordinate[2]
                    break

        index += 1
        steps += 1

        if index >= len(instructions):
            index = 0

    return steps


def second(all_info):
    instructions = all_info[0]
    coordinates = all_info[1]

    start_nodes = []
    for coordinate in coordinates:
        if coordinate[0][2] == "A":
            start_nodes.append(coordinate[0])

    path_length = []

    for start_node in start_nodes:
        index = 0
        steps = 0
        last_z = 0
        found = False

        current_node = start_node
        passed_nodes = [current_node]

        while not found:
            for coordinate in coordinates:
                if coordinate[0] == current_node:
                    if instructions[index] == "L":
                        current_node = coordinate[1]
                        break
                    else:
                        current_node = coordinate[2]
                        break

            index += 1
            steps += 1
            
            if index >= len(instructions):
                index = 0
            
            if len(passed_nodes) > len(instructions) and current_node in passed_nodes and passed_nodes.index(current_node) % len(instructions) == 0:
                current_node_index = passed_nodes.index(current_node)
                path_length.append([len(passed_nodes) - current_node_index, last_z]) # path_length = length cycle, nodes before the cycle
                found = True
            else:
                passed_nodes.append(current_node)
                if current_node[2] == "Z":
                    last_z = len(passed_nodes) - 1

    path_length.sort()
    return lowest_common_multiple(path_length)


def lowest_common_multiple(paths):
    found = False

    while not found:
        index = 0

        paths[index][1] = paths[index][0] + paths[index][1]
        while paths[index][1] > paths[index + 1][1]:
            paths[index + 1][1] = paths[index + 1][0] + paths[index + 1][1]
            index += 1
            if index + 1 == len(paths):
                break

        found = True
        common_path_length = paths[0][1]
        for path in paths:
            if path[1] != common_path_length:
                found = False
                break
        
        if common_path_length > 13000000000000:
            print("nope")
            found = True

    return paths[0][1]


if __name__ == "__main__":
    path = "2023/day08"
    data_path_example_one = Path(path + '/example_one.txt')
    data_path_example_two = Path(path + '/example_two.txt')
    data_path_example_three = Path(path + '/example_three.txt')
    data_path_input = Path(path + '/input.txt')
    data_path_Jeroen = Path(path + '/inputJeroen.txt')

    example_data_one = data_path_example_one.read_text()
    example_data_two = data_path_example_two.read_text()
    example_data_three = data_path_example_three.read_text()
    Jeroens_data = data_path_Jeroen.read_text()

    data = data_path_input.read_text()
    print("Part 1 - Example one input   : ", first(preprocess(example_data_one)))
    print("Part 1 - Example two input   : ", first(preprocess(example_data_two)))
    print("Part 1 - Actual input        : ", first(preprocess(data)))

    print("Part 2 - Example three input : ", second(preprocess(example_data_three)))
    print("Part 2 - Actual answer is    :  12324145107121")
    print("Part 2 - Actual input        : ", second(preprocess(data)))
    print("Part 2 - Jeroen's answer is  :  7309459565207")
    print("Part 2 - Jeroen's input is   : ", second(preprocess(Jeroens_data)))