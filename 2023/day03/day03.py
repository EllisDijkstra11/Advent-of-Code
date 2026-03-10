from pathlib import Path
from pprint import pprint 

def preprocess(input_lines: list[int]):
    lines = input_lines.split("\n")
    return lines


def first(lines):
    total_sum = 0
    i = 0
    while i < len(lines):
        j = 0
        while j < len(lines[i]):
            current_number = ""
            while j < len(lines[i]) and lines[i][j].isnumeric():
                current_number += (lines[i][j])
                j += 1

            if len(current_number) > 0:
                if j - len(current_number) - 1 >= 0 and not lines[i][j - len(current_number) - 1].isnumeric() and lines[i][j - len(current_number) - 1] != ".":
                    total_sum += int(current_number)

                elif j < len(lines[i]) and not lines[i][j].isnumeric() and lines[i][j] != ".":
                    total_sum += int(current_number)

                else:
                    k = 0
                    while k < len(current_number) + 2:
                        if j - k >= 0 and j - k < len(lines[i]):
                            if i - 1 > 0 and not lines[i - 1][j - k].isnumeric() and lines[i - 1][j - k] != ".":
                                total_sum += int(current_number)
                                break
                            elif i + 1 < len(lines) and not lines[i + 1][j - k].isnumeric() and lines[i + 1][j - k] != ".":
                                total_sum += int(current_number)
                                break
                        k += 1      
            j += 1
        i += 1
    return total_sum


def second(lines):
    total_sum = 0
    i = 0
    while i < len(lines):
        j = 0
        while j < len(lines[i]):
            gear_one = 0
            gear_two = 0
            if (lines[i][j] == "*"):
                y = -1
                while y < 2:
                    x = -1
                    while x < 2:

                        if lines[i + y][j + x].isnumeric():
                            if gear_one == 0:
                                gear_one = find_number(lines, i + y, j + x)
                            else:
                                gear_two = find_number(lines, i + y, j + x)

                        x += 1
                    y += 1
                

                if gear_one != gear_two and gear_two != 0:
                    total_sum += gear_one * gear_two
            j += 1
        i += 1
    return total_sum

def find_number(lines, i, j):
    x = 0
    current_number = ""

    while j - x > 0 and lines[i][j - x].isnumeric():
        x += 1
    
    if not lines[i][j - x].isnumeric():
        x -= 1

    while j - x < len(lines[i]) and lines[i][j - x].isnumeric():
        current_number += (lines[i][j - x])
        x -= 1

    if len(current_number) == 0:
        current_number = 0

    return int(current_number)


if __name__ == "__main__":
    path = "2023/day03"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print("Part 1 - Example: ", first(preprocess(example_data)))
    print("Part 1 - Actual:  ", first(preprocess(data)))
    print("Part 2 - Example: ", second(preprocess(example_data)))
    print("Part 2 - Actual:  ", second(preprocess(data)))
    