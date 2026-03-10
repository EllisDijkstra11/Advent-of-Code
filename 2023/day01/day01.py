from pathlib import Path
from pprint import pprint 


def preprocess(input_lines: list[int]):
    lines = input_lines.split("\n")
    return lines


def first(lines):
    total_sum = 0
    for line in lines:
        first_digit = -1
        second_digit = -1
        for character in line:
            if character.isnumeric() and first_digit is -1:
                first_digit = int(character)*10
                second_digit = int(character)
            elif character.isnumeric():
                second_digit = int(character)
        total_sum += first_digit + second_digit
    return total_sum


def second(lines):
    new_lines = []
    total_sum = 0
    numbers_text = "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
    numbers_number = "1", "2", "3", "4", "5", "6", "7", "8", "9"
    for line in lines:
        for number in numbers_text:
            index = line.find(number)
            while index is not -1:
                if index is not -1:
                    line = line[:index + 1] + numbers_number[numbers_text.index(number)] + line[index + 1:]
                index = line.find(number)

        print(line)
        new_lines.append(line)

    for line in new_lines:
        first_digit = -1
        second_digit = -1
        for character in line:
            if character.isnumeric() and first_digit is -1:
                first_digit = int(character)*10
                second_digit = int(character)
            elif character.isnumeric():
                second_digit = int(character)
        #print(first_digit + second_digit)
        total_sum += first_digit + second_digit
    return total_sum


if __name__ == "__main__":
    path = "2023/day01"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(example_data)))
    print(first(preprocess(data)))
    print(second(preprocess(example_data)))
    print(second(preprocess(data)))
    