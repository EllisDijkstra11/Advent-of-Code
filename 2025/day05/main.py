import os
import timeit 
from pathlib import Path

def preprocess(input_lines: list[int]):
    unsplit_ranges, ids = input_lines.split('\n\n')

    unsplit_ranges = [n for n in unsplit_ranges.split('\n')]
    ranges = [list(map(int, r.split("-"))) for r in unsplit_ranges]

    ids = set(int(n) for n in ids.split('\n'))
    return [ranges, ids]

def first(input):
    ranges, ids = input
    fresh = []
    fresh = [id for r in ranges for id in ids if r[0] <= id and id <= r[1]]
    print(fresh)
    return len(set(fresh))

def second(input):
    ranges, ids = input
    fresh = 0

    ranges = sorted(ranges, key = lambda x: x[1] - x[0])

    for i, [start, end] in enumerate(ranges):
        for [r_start, r_end] in ranges[i+1:]:
            
            # Range is entirely in another range
            if r_start <= start and end <= r_end:
                start, end = -1, -2

            # Start is in another range
            elif r_start <= start and start <= r_end:
                start = r_end + 1
            
            # End is in another range
            elif r_start <= end and end <= r_end:
                end = r_start - 1

        fresh += end - start + 1
            
    return fresh

if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))

    example = Path(path + '/example.txt').read_text()
    input = Path(path + '/input.txt').read_text()

    second_part = True
    debugging = not True
    low = [246869613824462]
    high = [359989952914616]
    unknown = []

    def string_format(part, example, input, prev_answers):
        print(f"{str('Part ' + part + ' - Example input').ljust(25)} {str('('+ str(example[0]) + ')').rjust(15)}: {example[1]}")

        if not debugging:
            low, high, unknown = prev_answers
            final_answer = input[0] is not None

            print(f"{str('Part ' + part + ' - Too low').ljust(41)}: {max(low)}") if low and not final_answer else False
            [print(f"{str('Part ' + part + ' - Wrong answer').ljust(41)}: {u}") for u in unknown] if unknown and not final_answer else False

            start = timeit.default_timer()
            print(f"{str('Part ' + part + ' - Actual input').ljust(23)} {str('('+ str(input[0]) + ')').rjust(17)}: {input[1]}") if final_answer \
                else print(f"{str('Part ' + part + ' - Actual input').ljust(41)}: {input[1]}") 
            print(f"Time taken: {timeit.default_timer()-start}s") if final_answer else False

            print(f"{str('Part ' + part + ' - Too high').ljust(41)}: {min(high)}") if high and not final_answer else False
            print("\n")

    f_example = [3, first(preprocess(example))]
    f_input = [None, None]
    if not debugging:
        f_input = [770, first(preprocess(input))]
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [14, second(preprocess(example))]
        s_input = [None, None]
        if not debugging:
            s_input = [357674099117260, second(preprocess(input))]
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
