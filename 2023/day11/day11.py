from pathlib import Path
from pprint import pprint 
import itertools

def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()

    return lines

def find_galaxies(lines):
    pos_x = 0
    pos_y = 0
    galaxies = []

    while pos_y < len(lines):
        if lines[pos_y][pos_x] == "#":
            galaxies.append([pos_x, pos_y])
        
        pos_x += 1
        if pos_x >= len(lines[0]):
            pos_x = 0
            pos_y += 1

    return galaxies


def find_rows_without_galaxies(lines, galaxies):
    no_galaxies = []

    pos_y = 0
    while pos_y < len(lines):
        no_galaxy = True
        for galaxy in galaxies:
            if pos_y == galaxy[1]:
                no_galaxy = False
        
        if no_galaxy:
            no_galaxies.append(pos_y)
        
        pos_y += 1

    return no_galaxies


def find_columns_without_galaxies(lines, galaxies):
    no_galaxies = []

    pos_x = 0
    while pos_x < len(lines[0]):
        no_galaxy = True
        for galaxy in galaxies:
            if pos_x == galaxy[0]:
                no_galaxy = False
        
        if no_galaxy:
            no_galaxies.append(pos_x)
        
        pos_x += 1

    return no_galaxies


def first(lines):
    galaxies = find_galaxies(lines)
    rows_without_galaxies = find_rows_without_galaxies(lines, galaxies)
    columns_without_galaxies = find_columns_without_galaxies(lines, galaxies)

    for galaxy in galaxies:
        for row in reversed(rows_without_galaxies):
            if galaxy[1] > row:
                galaxy[1] = galaxy[1] + 1
        
        for column in reversed(columns_without_galaxies):
            if galaxy[0] > column:
                galaxy[0] = galaxy[0] + 1

    total_sum = find_distance_between_galaxies(galaxies)

    return total_sum



def second(lines):
    galaxies = find_galaxies(lines)
    rows_without_galaxies = find_rows_without_galaxies(lines, galaxies)
    columns_without_galaxies = find_columns_without_galaxies(lines, galaxies)

    for galaxy in galaxies:
        empty_rows = 0
        empty_columns = 0
        for row in reversed(rows_without_galaxies):
            if galaxy[1] > row:
                empty_rows += 1
        
        for column in reversed(columns_without_galaxies):
            if galaxy[0] > column:
                empty_columns += 1

        galaxy[0] = galaxy[0] + empty_columns * 999999
        galaxy[1] = galaxy[1] + empty_rows * 999999


    total_sum = find_distance_between_galaxies(galaxies)

    return total_sum


def find_distance_between_galaxies(galaxies):
    total_sum = 0

    for first_galaxy, second_galaxy in itertools.combinations(galaxies, 2):
        distance = abs(second_galaxy[0] - first_galaxy[0]) + abs(second_galaxy[1] - first_galaxy[1])
        total_sum += abs(distance)

    return total_sum

if __name__ == "__main__":
    path = "2023/day11"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print("Part 1 - Example input : ", first(preprocess(example_data)))
    print("Part 1 - Actual input  : ", first(preprocess(data)))
    print("Part 1 - Answer        :  9509330\n")

    print("Part 2 - Example input : ", second(preprocess(example_data)))
    print("Part 2 - Actual input  : ", second(preprocess(data)))
    print("Part 2 - Answer        :  635832237682")
    