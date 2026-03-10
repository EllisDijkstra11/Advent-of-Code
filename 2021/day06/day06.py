from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    return [int(n) for n in input_lines.split(',')]

class Fishes:
    def __init__(self, fishes):
        self.singleFishes = fishes
        self.fishes = [0] * 9

        self.countFishes()
    
    def countFishes(self):
        for index in range(len(self.fishes)):
            countFishes = self.singleFishes.count(index)
            self.fishes[index] = countFishes
    
    def procreateFishes(self, n):
        for _ in range(n):
            newFishes = [0] * 9

            for index in range(1, len(self.fishes)):
                newFishes[index-1] = self.fishes[index]
            
            newFishes[6] += self.fishes[0]
            newFishes[8] = self.fishes[0]
            self.fishes = newFishes
    
    def returnFishes(self):
        return sum(self.fishes)

def first(fishes):
    fishes = Fishes(fishes)
    fishes.procreateFishes(80)
    return fishes.returnFishes()

def second(fishes):
    fishes = Fishes(fishes)
    fishes.procreateFishes(256)
    return fishes.returnFishes()

if __name__ == "__main__":
    path = "2021/day06"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (5934):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input               :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input (26984457539):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input               :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")