import os
import timeit 
from math import prod
from pathlib import Path

def preprocess(input_lines: list[int]):
    lines = input_lines.split('\n')
    length = min(len(line) for line in lines)

    equations = []
    prev_i = 0
    for i in range(length):

        # The only columns which contain just one character, are the
        # columns with only spaces. Otherwise, it will contain either
        # the operator or a number in addition to spaces
        if len(set([line[i] for line in lines])) == 1:
            equations.append([line[prev_i:i] for line in lines])

            # No reason to add the column of spaces, so skip it
            prev_i = i + 1

    # Add the last equation
    equations.append([line[prev_i:] for line in lines])
    return equations

def first(equations):
    total = 0

    for eq in equations:
        op = eq[-1].replace(" ", "")

        if op == "+":
            total += sum(map(int, eq[:-1]))
        elif op == "*":
            total += prod(map(int, eq[:-1]))
        else:
            print("I'm special", eq)

    return total

def second(equations):
    new_equations = []
    for equation in equations:
        new_equation = [] * len(equation)
        for i in range(len(equation[0])):
            new_equation.append("".join([number[i] for number in equation[:-1]]))

        new_equation.append(equation[-1])
        new_equations.append(new_equation)
    return new_equations

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

    f_example = [4277556, first(preprocess(example))]
    f_input = [3785892992137, first(preprocess(input))]
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        s_example = [3263827, first(second(preprocess(example)))]
        s_input = [7669802156452, first(second(preprocess(input)))]
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
