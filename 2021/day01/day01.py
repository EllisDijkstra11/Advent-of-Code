from pathlib import Path
import timeit 


def preprocess(input_lines: list[int]):
    return [int(n) for n in input_lines.split('\n')]


def first(depths):
    increases = 0
    for index in range(1, len(depths)):
        if (depths[index] - depths[index - 1]) > 0:
            increases += 1
    return increases


def second(depths):
    increases = 0
    for index in range(0, len(depths) - 3):
        first_window = sum(depths[index:index+3])
        second_window = sum(depths[index+1:index+4])
        if second_window > first_window:
            increases += 1
    return increases

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day01"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input         (7):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input         (5):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")

    