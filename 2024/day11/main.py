import timeit 
from pathlib import Path
from collections import defaultdict

def preprocess(input_lines: list[int]):
    return [n for n in input_lines.split(' ')]

class Stones:
    def __init__(self, input):
        self.stones = defaultdict(int)
        for stone in input:
            self.stones[stone] += 1
    
    def watch_stones(self, blinks):
        for _ in range(blinks):
            new_stones = defaultdict(int)
            for stone, number in self.stones.items():
                if stone == '0':
                    new_stones['1'] += number
                elif len(stone) % 2 == 0:
                    split = int(len(stone) / 2)
                    new_stones[stone[:split]] += number

                    while split < len(stone) - 1 and stone[split] == '0':
                        split += 1
                    
                    new_stones[stone[split:]] += number
                else:
                    new_stones[str(int(stone) * 2024)] += number
            
            self.stones = new_stones
        return sum(self.stones.values())

def first(input):
    stones = Stones(input)
    return stones.watch_stones(25)

def second(input):
    stones = Stones(input)
    return stones.watch_stones(75)

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day11"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input     (55312):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input          ():", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")