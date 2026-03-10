import os
import timeit 
from pathlib import Path

def preprocess(input_lines: list[int]):
    lines = input_lines.split('\n')
    return lines

def first(input):
    start = [(row.index('S'), r)
        for r, row in enumerate(input)
        if 'S' in row][0]

    splits = 0
    beams = set([start[0]])

    for i in range(len(input[0])):
        current = input[i]
        splitters = set([i for i, char in enumerate(current) if char == "^"])

        split_beams = beams.intersection(splitters)
        new_beams = set(beam + movement for beam in split_beams for movement in [-1, 1])
        splits += len(split_beams)

        beams = beams.difference(split_beams).union(new_beams)

    return splits

def second(input):
    start = [(row.index('S'), r)
        for r, row in enumerate(input)
        if 'S' in row][0]

    timelines = {start[0]: 1}

    for i in range(len(input[0])):
        current = input[i]
        splitters = set([i for i, char in enumerate(current) if char == "^"])

        split_timelines = {timeline: value for timeline, value in timelines.items() if timeline in splitters and value > 0}
        
        if len(split_timelines) >= 1:
            new_timelines = [[timeline + movement, value] for timeline, value in split_timelines.items() for movement in [-1, 1]]

            for key in split_timelines.keys():
                timelines[key] = 0
            
            for [key, value] in new_timelines:
                timelines[key] = timelines.get(key, 0) + value

    return sum(timelines.values())

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

    f_example = [21, first(preprocess(example))]
    f_input = [None, None]
    if not debugging:
        f_input = [1592, first(preprocess(input))]
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [40, second(preprocess(example))]
        s_input = [None, None]
        if not debugging:
            s_input = [17921968177009, second(preprocess(input))]
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
