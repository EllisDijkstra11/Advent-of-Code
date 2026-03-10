import os
import timeit 
from itertools import combinations
from pprint import pprint
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [tuple([int(number) for number in line.split(',')]) for line in input_lines.split('\n')]

def find_rect(first, second):
    return (abs(first[0] - second[0]) + 1) * (abs(first[1] - second[1]) + 1)

def find_coloured_rect(outline, first, second):
    min_x, max_x = min(first[0], second[0]), max(first[0], second[0])
    min_y, max_y = min(first[1], second[1]), max(first[1], second[1])
    
    for x, y in outline:
        if (min_x < x < max_x) and (min_y < y < max_y):
            return False
    
    return True
    
def first(input): 
    return max([find_rect(input[i], input[j]) for i in range(len(input) - 1) for j in range(i, len(input))])

def second(input):
    outline = set(input.copy())

    prev_x, prev_y = input[-1]
    for x, y in input:
        outline |= set((i, j) for i in range(min(x, prev_x), max(x, prev_x) + 1) for j in range(min(y, prev_y), max(y, prev_y) + 1))
        prev_x, prev_y = x, y   

    areas = [[f, s, find_rect(f, s)] for f, s in combinations(input, 2)]
    areas.sort(key=lambda s: s[-1], reverse=True)

    for area in areas:
        f, s, size = area
        if find_coloured_rect(outline, f, s):
            return size
        
    return 0

if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))

    example = Path(path + '/example.txt').read_text()
    input = Path(path + '/input.txt').read_text()

    second_part = True
    debugging = not True
    low = [140937420]
    high = []
    unknown = []

    def string_format(part, example, input, prev_answers):
        print(f"{str('Part ' + part + ' - Example input').ljust(25)} {str('('+ str(example[0]) + ')').rjust(15)}: {example[1]}")

        if not debugging:
            low, high, unknown = prev_answers
            final_answer = input[0] is not None

            print(f"{str('Part ' + part + ' - Too low').ljust(41)}: {max(low)}") if low and not final_answer else False
            [print(f"{str('Part ' + part + ' - Wrong answer').ljust(41)}: {u}") for u in unknown] if unknown and not final_answer else False

            print(f"{str('Part ' + part + ' - Actual input').ljust(25)} {str('('+ str(input[0]) + ')').rjust(15)}: {input[1]}") if final_answer \
                else print(f"{str('Part ' + part + ' - Actual input').ljust(41)}: {input[1]}") 

            print(f"{str('Part ' + part + ' - Too high').ljust(41)}: {min(high)}") if high and not final_answer else False
            print("\n")

    f_example = [50, first(preprocess(example))]
    f_input = [None, None]
    if not debugging:
        start = timeit.default_timer()
        f_input = [4776487744, first(preprocess(input))]
        print(f"Time taken: {timeit.default_timer()-start}s")
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [24, second(preprocess(example))]
        s_input = [None, None]
        if not debugging:
            start = timeit.default_timer()
            s_input = [1560299548, second(preprocess(input))]
            print(f"Time taken: {timeit.default_timer()-start}s")
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
