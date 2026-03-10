import os
import timeit 
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [[int(number) for number in line] for line in input_lines.split('\n')]

def first(banks):
    total = 0
    for bank in banks:
        highest = max(bank)

        if bank.count(highest) == 2:
            total += highest * 10 + highest

        else:
            index = bank.index(highest)
            remainder = bank[index + 1:]
            if len(remainder) == 0:
                total += max(bank[:-1]) * 10 + highest
            else:
                total += highest * 10 + max(remainder)
    
    return total

def second(banks):
    total = 0

    for bank in banks:
        outputs = list(str(bank.pop(0)))
        
        while len(bank) >= 1:
            new_number = bank.pop(0)
            new_outputs = [str(max(int(outputs[0]), new_number))]

            for i in range(0, len(outputs) - 1):
                new_output = outputs[i] + str(new_number)
                new_outputs.append(str(max(int(new_output), int(outputs[i + 1]))))

            new_outputs.append(outputs[-1] + str(new_number))
            outputs = new_outputs.copy()

        maximum = max([int(output) for output in list(outputs) if len(output) == 12])
        total += maximum

    return total

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

            start = timeit.default_timer()
            print(f"{str('Part ' + part + ' - Actual input').ljust(25)} {str('('+ str(input[0]) + ')').rjust(15)}: {input[1]}") if final_answer \
                else print(f"{str('Part ' + part + ' - Actual input').ljust(41)}: {input[1]}") 
            print(f"Time taken: {timeit.default_timer()-start}s") if final_answer else False

            print(f"{str('Part ' + part + ' - Too high').ljust(41)}: {min(high)}") if high and not final_answer else False
            print("\n")

    f_example = [357, first(preprocess(example))]
    f_input = [None, None]
    if not debugging:
        f_input = [17144, first(preprocess(input))]
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [3121910778619, second(preprocess(example))]
        s_input = [None, None]
        if not debugging:
            s_input = [170371185255900, second(preprocess(input))]
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
