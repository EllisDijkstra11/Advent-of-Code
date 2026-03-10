from pathlib import Path
from pprint import pprint 
import timeit

def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()     

    return lines

def first(lines):
    pass


def second(lines):
    pass


if __name__ == "__main__":
    path = "2023/day"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input       ():", first(preprocess(example_data)))

    # start = timeit.default_timer()
    # print("Part 1 - Actual input             :", first(preprocess(data)))
    # print(f"Time taken: {timeit.default_timer()-start}s\n")

    # print("Part 2 - Example input       ():", second(preprocess(example_data)))
    
    # start = timeit.default_timer()
    # print("Part 2 - Actual input             :", second(preprocess(data)))
    # print(f"Time taken: {timeit.default_timer()-start}s")
    