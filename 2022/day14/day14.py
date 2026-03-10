from pathlib import Path
from pprint import pprint 
import math


def preprocess(input_lines: list[int]):
    rock_structures = input_lines.split("\n")
    all_rocks = []
    for rock_structure in rock_structures:
        index = 0
        rocks = rock_structure.split(" -> ")
        for index in range(len(rocks) - 1):
            first = rocks[index].split(",")
            second = rocks[index + 1].split(",")

            first = [eval(first[0]), eval(first[1])]
            second = [eval(second[0]), eval(second[1])]

            direction = int(math.copysign(1, second[0] - first[0]))
            for i in range(first[0], second[0] + direction, direction):
                if not [i, first[1]] in all_rocks:
                    all_rocks.append([i, first[1]])

            direction = int(math.copysign(1, second[1] - first[1]))
            for i in range(first[1], second[1] + direction, direction):
                if not [first[0], i] in all_rocks:
                    all_rocks.append([first[0], i])           

    return all_rocks


def drop_sand(all_rocks, boolean_first):
    left, right, lowest = get_outside_rocks(all_rocks)
    lowest += 2
    
    all_sand = []
    all_blocked = all_rocks.copy()
    sand_start = [500, 0]
    exit = False
    while not exit:
        sand_current = sand_start

        # Move sand down
        sand_next = [sand_current[0], sand_current[1] + 1]

        if sand_next not in all_blocked:
            sand_current = put_sand_down(sand_current, all_blocked, lowest)

        # Move sand left
        sand_next = [sand_current[0] - 1, sand_current[1] + 1]

        if sand_next not in all_blocked:
            sand_current = put_sand_left(sand_current, all_blocked, lowest)
        
        # Move sand right
        sand_next = [sand_current[0] + 1, sand_current[1] + 1]

        if sand_next not in all_blocked:
            sand_current = put_sand_right(sand_current, all_blocked, lowest)

        if boolean_first:
            if sand_current[1] < lowest - 1:
                all_sand.append(sand_current)
                all_blocked.append(sand_current)
            else:
                exit = True
        else:
            all_sand.append(sand_current)
            all_blocked.append(sand_current)
            if sand_current == sand_start:
                exit = True

    make_visualisation(all_rocks, all_sand)

    return len(all_sand)
    

def first(all_rocks):
    return drop_sand(all_rocks, True)


def second(all_rocks):
    return drop_sand(all_rocks, False)


def put_sand_down(sand_current, all_blocked, lowest):
    sand_next = [sand_current[0], sand_current[1] + 1]

    while sand_next not in all_blocked and sand_next[1] < lowest:
        sand_current = sand_next
        sand_next = [sand_current[0], sand_current[1] + 1]

    return sand_current


def put_sand_left(sand_current, all_blocked, lowest):
    sand_next = [sand_current[0] - 1, sand_current[1] + 1]

    while sand_next not in all_blocked and sand_next[1] < lowest:
        sand_current = put_sand_down(sand_next, all_blocked, lowest)
        sand_next = [sand_current[0] - 1, sand_current[1] + 1]
    
    return sand_current


def put_sand_right(sand_current, all_blocked, lowest):
    sand_next = [sand_current[0] + 1, sand_current[1] + 1]

    while sand_next not in all_blocked and sand_next[1] < lowest:
        sand_next = put_sand_down(sand_next, all_blocked, lowest)
        sand_current = put_sand_left(sand_next, all_blocked, lowest)
        sand_next = [sand_current[0] + 1, sand_current[1] + 1]

    return sand_current


def get_outside_rocks(all_rocks):
    left = 500
    right = 500
    lowest = 0
    for rock in all_rocks:
        if rock[0] < left:
            left = rock[0]
        elif rock[0] > right:
            right = rock[0]
        
        if rock[1] > lowest:
            lowest = rock[1]
    
    return left, right, lowest


def make_visualisation(all_rocks, all_sand):
    left, right, lowest = get_outside_rocks(all_sand)
    left -= 2
    right += 2
    lowest += 2
    visualisation = [""] * lowest
    for y in range(len(visualisation)):
        for x in range(right - left):
            if [left + x, y] in all_sand:
                visualisation[y] = visualisation[y] + "o"            
            elif [left + x, y] in all_rocks or y == lowest - 1:
                visualisation[y] = visualisation[y] + "#"
            else:
                visualisation[y] = visualisation[y] + "."

    pprint(visualisation)


if __name__ == "__main__":
    path = "2022/day14"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(example_data)))
    print(first(preprocess(data)))
    print(second(preprocess(example_data)))
    print(second(preprocess(data)))
    
