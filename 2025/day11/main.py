import os
import timeit 
from pprint import pprint
from pathlib import Path

def preprocess(input_lines: list[int]):
    devices = [[device for device in line.split(':')] for line in input_lines.split('\n')]

    dict = {}
    for device, output in devices:
        dict[device] = set(output[1:].split(' '))
    return dict

def first(devices):
    counts = {key: 1 for key, value in devices.items() if value == {'out'}}
    for key in counts.keys():
        del devices[key]

    while not 'you' in counts.keys():
        found = []
        for key, items in devices.items():
            if items <= counts.keys():
                counts[key] = sum([counts[item] for item in items])
                found += [key]
        
        for key in found:
            del devices[key]
    
    return counts['you']

def second(devices):
    counts = {key: {'neither': 1} for key, value in devices.items() if value == {'out'}}
    for key in counts.keys():
        del devices[key]

    while not 'svr' in counts.keys():
        found = []
        for key, items in devices.items():
            if items <= counts.keys():
                counts[key] = {}
                for fft_dac_pair in ['neither', 'fft', 'dac', 'both']:
                    counts[key][fft_dac_pair] = sum([counts[item].get(fft_dac_pair, 0) for item in items])

                if key in ['fft', 'dac']:
                    other = 'dac' if key == 'fft' else 'fft'
                    counts[key][key] += counts[key]['neither']
                    counts[key]['both'] += counts[key][other]
                    del counts[key]['neither']
                    del counts[key][other]
        
        for key in found:
            del devices[key]
    
    return counts['svr']['both']

if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))

    example = Path(path + '/example.txt').read_text()
    example_2 = Path(path + '/example_2.txt').read_text()
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

    f_example = [5, first(preprocess(example))]
    f_input = [None, None]
    if not debugging:
        start = timeit.default_timer()
        f_input = [786, first(preprocess(input))]
        print(f"Time taken: {timeit.default_timer()-start}s")
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [2, second(preprocess(example_2))]
        s_input = [None, None]
        if not debugging:
            start = timeit.default_timer()
            s_input = [495845045016588, second(preprocess(input))]
            print(f"Time taken: {timeit.default_timer()-start}s")
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
