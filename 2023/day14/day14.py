from pathlib import Path
from pprint import pprint 
import array as arr
import timeit

def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()     
    
    rows = []
    for line in lines:
        rows.append(tuple(line))
    return tuple(rows)


def first(rows):
    total_sum = 0
    tuple_columns = rows_to_columns(rows)

    columns = []
    for column in tuple_columns:
        columns.append([list(column)])

    for column in columns:
        last_rock = -1
        for rock in range(len(column)):
            if column[rock] == "O":
                column[rock] = "."
                column[last_rock + 1] = "O"

                total_sum += len(column) - last_rock - 1
                last_rock += 1
            elif column[rock] == "#":
                last_rock = rock
    
    return total_sum


def second(rows):
    total_sum = 0
    total_cycles = 1000000000
    columns = rows_to_columns(rows)

    execute_cycles(columns, total_cycles)
 
    for column in columns:
        total_rocks = column.count("O")
        total_sum += (len(column) - 1) * total_rocks
        print(len(column) - 1, "*", total_rocks, "=", total_sum)

    return total_sum


def rows_to_columns(rows):
    columns = [[]] * len(rows[0])

    for index in range(len(rows[0])):
        column = []

        for line in range(len(rows)):
            column.append(rows[line][index])

        columns[index] = tuple(column)

    return tuple(columns)


def first_cycle(columns):
    columns = move_rocks(columns)

    for _ in range(3):
        rows = change_direction(columns)
        columns = move_rocks(rows)
    
    return columns


def execute_cycles(columns, total_cycles):
    columns = first_cycle(columns)

    cycle_count = 1
    states = {}

    while cycle_count < total_cycles:
        field_key = columns
        print(type(columns), type(columns[0]))


        if field_key in states:
            cycle_period = cycle_count - states[field_key]
            remaining_cycles = (total_cycles - cycle_count) % cycle_period
            print(cycle_count)
            return execute_cycles(columns, remaining_cycles)
        
        states[field_key] = cycle_count
        columns = cycle(columns)
        cycle_count += 1
    
    return columns

def cycle(columns):
    for _ in range(4):
        rows = change_direction(columns)
        columns = move_rocks(rows)
    
    return columns


def change_direction(columns):
    length_columns = len(columns[0])
    rows = [[]] * length_columns

    for index in range(length_columns):
        row = []

        for line in range(len(rows)):
            row.append(columns[line][length_columns - index - 1])
        
        rows[index] = tuple(row)

    return tuple(rows)


def move_rocks(tuple_columns):
    columns = []
    for column in tuple_columns:
        columns.append([list(column)])

    for column in columns:
        last_rock = -1

        for rock in range(len(column)):

            if column[rock] == "O":
                column[rock] = "."
                column[last_rock + 1] = "O"
                last_rock += 1

            elif column[rock] == "#":
                last_rock = rock
    
    tuple_columns = []
    for column in columns:
        columns.append(tuple(column))

    return tuple(tuple_columns)

# def e_to_s_and_w_to_n(rows):

#     length_rows = len(rows)
#     columns = [[]] * length_rows

#     for row in range(length_rows):
#         columns[row] = list(reversed(rows[row]))
#         #print(list(reversed(rows[row])))

#     print("\n\nColumns:")
#     pprint(columns)


if __name__ == "__main__":
    path = "2023/day14"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example one input   (136):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")

    start = timeit.default_timer()
    print("Part 2 - Example one input    (64):", second(preprocess(example_data)))
    print(f"Time taken: {timeit.default_timer()-start}s")

    start = timeit.default_timer()
    # print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")
    