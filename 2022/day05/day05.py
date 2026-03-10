from pathlib import Path
from pprint import pprint


def preprocess(input_lines: list[int], x, y):
    crates, steps = input_lines.split('\n\n')
    crate_rows = crates.split('\n')
    crate_stack = []
    number_horizontal = x
    number_vertical = y
    
    for index in range(number_horizontal):
        crate_stack.append([index])

    x = 0
    y = 0
    while y < number_vertical:
        while x < number_horizontal:
            if crate_rows[y][x * 4 + 1] != " ":
                crate_stack[x].insert(1, "[" + crate_rows[y][x * 4 + 1] + "]")
            x += 1
        y += 1
        x = 0

    split_steps = []
    for step in steps.split("\n"):
        step = step.split(" ")
        step.remove("move")
        step.remove("from")
        step.remove("to")
        step_tuple = (int(step[0]), int(step[1]), int(step[2]))
        split_steps.append(step_tuple)
        [int(n) for n in steps if n in "0123456789"]
    crates_and_steps = [crate_stack, split_steps]
    return crates_and_steps


def first(crates_and_steps):
    return move_crates(crates_and_steps, False)


def second(crates_and_steps):
    return move_crates(crates_and_steps, True)


def move_crates(crates_and_steps, multiple_crates):
    crates, steps = crates_and_steps

    for step in steps:
        amount_of_crates, first_stack, second_stack = step
        first_stack -= 1
        second_stack -= 1
        for index in range(amount_of_crates):
            if multiple_crates:
                offset = amount_of_crates - index 
            else:
                offset = 1     
            crate = crates[first_stack][-offset]
            crates[second_stack].append(crate)
            del crates[first_stack][-offset]

    top_crates = ""
    for crate_stack in range(len(crates)):
        top_crate = crates[crate_stack][-1][1]
        top_crates = top_crates + top_crate

    return top_crates


if __name__ == "__main__":
    data_path_example = Path('2022/day05/example05.txt')
    data_path_input = Path('2022/day05/inputJeroen05.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()

    print(first(preprocess(example_data, 3, 3)))
    print(first(preprocess(data, 9, 8)))
    print(second(preprocess(example_data, 3, 3)))
    print(second(preprocess(data, 9, 8)))
    