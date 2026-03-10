import os
import timeit 
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [[char for char in line] for line in input_lines.split('\n')]

def get_neighbours(input, current_x, current_y, max_x, max_y):
    x_pos = [current_x - 1, current_x, current_x + 1]
    y_pos = [current_y - 1, current_y, current_y + 1]

    neighbours = []
    for x in x_pos:
        for y in y_pos:
            if x == current_x and y == current_y:
                continue
            if x < 0 or x >= max_x:
                continue
            if y < 0 or y >= max_y:
                continue
            neighbours.append(input[y][x])
    # print(x, y, neighbours)
    return neighbours

def first(input):
    max_x = len(input[0])
    max_y = len(input)

    accessible = []

    for x in range(max_x):
        for y in range(max_y):
            if input[y][x] == "@":
                neighbours = get_neighbours(input, x, y, max_x, max_y)
                if neighbours.count("@") < 4:
                    accessible.append([x, y])

    return accessible

def second(input):
    accessible = first(input)
    total = len(accessible)

    while len(accessible) > 0:
        for [x, y] in accessible:
            input[y][x] = "."
        
        accessible = first(input)
        total += len(accessible)
        
    return total

if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))

    example = Path(path + '/example.txt').read_text()
    input = Path(path + '/input.txt').read_text()

    second_part = True
    debugging = False
    low = []
    high = []
    unknown = []

    def string_format(part, example, input, prev_answers):
        print(f"{str('Part ' + part + ' - Example input').ljust(25)} {str('('+ str(example[0]) + ')').rjust(15)}: {example[1]}")

        if not debugging:
            low, high, unknown = prev_answers
            final_answer = input[0] is not None

            print(f"{str('Part ' + part + ' - Too low').ljust(41)}: {max(low)}") if low and not final_answer else False
            [print(f"{str('Part ' + part + ' - Wrong answer').ljust(41)}: {u}") for u in unknown] if unknown and not final_answer else False

            start = timeit.default_timer()
            print(f"{str('Part ' + part + ' - Actual input').ljust(25)} {str('('+ str(input[0]) + ')').rjust(15)}: {input[1]}") if final_answer \
                else print(f"{str('Part ' + part + ' - Actual input').ljust(41)}: {input[1]}") 
            print(f"Time taken: {timeit.default_timer()-start}s") if final_answer else False

            print(f"{str('Part ' + part + ' - Too high').ljust(41)}: {min(high)}") if high and not final_answer else False
            print("\n")

    f_example = [13, len(first(preprocess(example)))]
    f_input = [None, None]
    if not debugging:
        f_input = [1626, len(first(preprocess(input)))]
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [43, second(preprocess(example))]
        s_input = [None, None]
        if not debugging:
            s_input = [9173, second(preprocess(input))]
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
