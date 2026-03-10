import os
import timeit 
from math import floor
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [int(n.replace("L", "-").replace("R", "")) for n in input_lines.split('\n')]

def first(input):
    dial = 50
    count = 0

    for turn in input:
        dial += turn

        while dial > 99:
            dial -= 100

        while dial < 0:
            dial += 100
        
        if dial == 0:
            count += 1

    return count

def second(input):
    dial = 50
    count = 0

    for turn in input:
        left = False
        is_zero = False

        if turn < 0:
            left = True
            turn *= -1
        if dial == 0:
            is_zero = True

        move = turn % 100
        count += turn // 100

        if left:
            dial -= move
            if dial < 0:
                dial += 100
                if not is_zero:
                    count += 1
        else:
            dial += move
            if dial > 99:
                dial -= 100
                if dial != 0:
                    count += 1

        if dial == 0:
            count += 1

    return count

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

    f_example = [3, first(preprocess(example))]
    f_input = [1180, first(preprocess(input))]
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [6, second(preprocess(example))]
        s_input = [6892, second(preprocess(input))]
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
