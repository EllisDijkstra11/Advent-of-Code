import os
import numpy as np
import timeit 
from math import prod
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [[int(pos) for pos in line.split(',')] for line in input_lines.split('\n')]

def first(input, n):
    boxes = {i: np.array(line) for i, line in enumerate(input)}
    distances = [[i, j, np.linalg.norm(boxes[i] - boxes[j])] for i in range(len(boxes) - 1) for j in range(i + 1, len(boxes))]
    min_distances = sorted(distances, key=lambda d: d[-1])
    circuits = [[i] for i in range(len(boxes))]

    for _ in range(n):
        f, s, _ = min_distances.pop(0)
        f_index = next((i for i, circuit in enumerate(circuits) if f in circuit), None)
        s_index = next((i for i, circuit in enumerate(circuits) if s in circuit), None)

        if f_index == None and s_index == None:
            circuits.append([f, s])

        elif f_index == None:
            circuits[s_index].append(f)

        elif s_index == None:
            circuits[f_index].append(s)

        elif f_index != s_index:
            new_circuits = [circuit for circuit in circuits if f not in circuit and s not in circuit]
            f_circuit = circuits[f_index]
            s_circuit = circuits[s_index]

            new_circuits.append(f_circuit + s_circuit)

            circuits = new_circuits.copy()

    lengths = [len(circuit) for circuit in circuits]
    lengths.sort(reverse=True)
    return prod(lengths[:3])

def second(input):
    boxes = {i: np.array(line) for i, line in enumerate(input)}
    distances = [[i, j, np.linalg.norm(boxes[i] - boxes[j])] for i in range(len(boxes) - 1) for j in range(i + 1, len(boxes))]
    min_distances = sorted(distances, key=lambda d: d[-1])
    circuits = [set([i]) for i in range(len(boxes))]

    while len(circuits) != 1:
        f, s, _ = min_distances.pop(0)
        f_index = next((i for i, circuit in enumerate(circuits) if f in circuit and s not in circuit), None)

        if f_index != None:
            f_set = circuits.pop(f_index)
            s_set = circuits.pop(next((i for i, circuit in enumerate(circuits) if s in circuit), None))

            circuits.append(f_set.union(s_set))

    f_x, _, _ = boxes[f]
    s_x, _, _ = boxes[s]

    return f_x * s_x

if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))

    example = Path(path + '/example.txt').read_text()
    input = Path(path + '/input.txt').read_text()

    second_part = True
    debugging = not True
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

            print(f"{str('Part ' + part + ' - Actual input').ljust(25)} {str('('+ str(input[0]) + ')').rjust(15)}: {input[1]}") if final_answer \
                else print(f"{str('Part ' + part + ' - Actual input').ljust(41)}: {input[1]}") 

            print(f"{str('Part ' + part + ' - Too high').ljust(41)}: {min(high)}") if high and not final_answer else False
            print("\n")

    f_example = [40, first(preprocess(example), 10)]
    f_input = [None, None]
    if not debugging:
        start = timeit.default_timer()
        f_input = [181584, first(preprocess(input), 1000)]
        print(f"Time taken: {timeit.default_timer()-start}s")
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [25272, second(preprocess(example))]
        s_input = [None, None]
        if not debugging:
            start = timeit.default_timer()
            s_input = [8465902405, second(preprocess(input))]
            print(f"Time taken: {timeit.default_timer()-start}s")
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
