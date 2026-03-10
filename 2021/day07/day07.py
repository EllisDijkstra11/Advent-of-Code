from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    return [int(n) for n in input_lines.split(',')]

class Crabs:
    def __init__(self, crabs):
        self.locations = crabs
        self.locationsSum = sum(self.locations)
        self.locationsLength = len(self.locations)
        self.mean = round(self.locationsSum / self.locationsLength)

    def findConstantFuel(self):
        smallest_cost = float('inf')
        min_value = min(self.locations)
        max_value = max(self.locations)

        for line in range(min_value, max_value):
            smaller_locations = list(filter(lambda x: (x < line), self.locations))
            bigger_locations = list(filter(lambda x: (x > line), self.locations))
            current_cost = line * len(smaller_locations) - sum(smaller_locations) + sum(bigger_locations) - line * len(bigger_locations)
            smallest_cost = min(smallest_cost, current_cost)

        return smallest_cost

    def findExponentialFuel(self):
        current_cost = self.findCost(self.mean)
        cost_smaller_mean = self.findCost(self.mean - 1)
        step = 1
        if cost_smaller_mean < current_cost:
            step = -1

        return self.recursiveFindExponentialFuel(current_cost, self.mean, step)
    
    def recursiveFindExponentialFuel(self, smallest_cost, mean, step):
        current_cost = self.findCost(mean + step)

        if current_cost < smallest_cost:
            self.recursiveFindExponentialFuel(current_cost, mean + step, step)

        return int(current_cost)

    def findCost(self, mean):
        current_cost = 0
        differences = []
        for location in self.locations:
            differences.append(abs(mean - location))
        
        for difference in differences:
            current_cost += (difference * (difference + 1) / 2)
        
        return current_cost

def first(crabs):
    crabs = Crabs(crabs)
    return crabs.findConstantFuel()

def second(crabs):
    crabs = Crabs(crabs)
    return crabs.findExponentialFuel()

if __name__ == "__main__":
    path = "2021/day07"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (37):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input       (168):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")