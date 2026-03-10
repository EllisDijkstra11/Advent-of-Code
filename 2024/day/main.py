import timeit 
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [int(n) for n in input_lines.split('\n')]

def first(input):
    return None

def second(input):
    return None

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day0"

    example = Path(path + '/example.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    print("Part 1 - Example input          ():", first(preprocess(example)))

    # start = timeit.default_timer()
    # print("Part 1 - Actual input             :", first(preprocess(input)))
    # print(f"Time taken: {timeit.default_timer()-start}s\n")

    # print("Part 2 - Example input          ():", second(preprocess(example)))
    
    # start = timeit.default_timer()
    # print("Part 2 - Actual input             :", second(preprocess(input)))
    # print(f"Time taken: {timeit.default_timer()-start}s")