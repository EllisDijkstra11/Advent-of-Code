from pathlib import Path
import string
from tokenize import String

def preprocess(input_lines: list[int]):
    return input_lines

def first(string):
    for index in range(4, len(string)):
        if len(set(string[index - 4:index])) == 4:
            return index
   

def second(string):
    for index in range(14, len(string)):
        if len(set(string[index - 14:index])) == 14:
            return index

if __name__ == "__main__":
    data_path_example = Path('2022/day06/example.txt')
    data_path_input = Path('2022/day06/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(data)))
    print(second(preprocess(data)))
    