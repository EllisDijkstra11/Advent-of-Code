import os
import re
import timeit 
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [[int(r) for r in range.split('-')] for range in input_lines.split(',')]

def first(ranges):
    invalid_ids = []

    for start, end in ranges:
        for pattern in range(start, end + 1):
            repeat = bool(re.fullmatch(r"(.+)\1{1}", str(pattern)))
            if repeat:
                invalid_ids.append(pattern)

    return sum(invalid_ids)

def second(ranges):
    invalid_ids = []

    for start, end in ranges:
        for pattern in range(start, end + 1):
            repeat = bool(re.fullmatch(r"(.+)\1+", str(pattern)))
            if repeat:
                invalid_ids.append(pattern)

    return sum(invalid_ids)

if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))

    example = Path(path + '/example.txt').read_text()
    input = Path(path + '/input.txt').read_text()

    second_part = True
    debugging = False
    low = [10991181061, 19386338244]
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

    f_example = [1227775554, first(preprocess(example))]
    f_input = [None, None]
    if not debugging:
        start = timeit.default_timer()
        f_input = [19386344315, first(preprocess(input))]
        print(f"Time taken: {timeit.default_timer()-start}s")
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [4174379265, second(preprocess(example))]
        s_input = [None, None]
        if not debugging:
            start = timeit.default_timer()
            s_input = [34421651192, second(preprocess(input))]
            print(f"Time taken: {timeit.default_timer()-start}s")
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
