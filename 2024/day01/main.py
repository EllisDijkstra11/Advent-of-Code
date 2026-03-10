from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    ids = input_lines.split("\n")

    first_ids = []
    second_ids = []
    for id in ids:
        first_id, second_id = id.split("   ")

        first_ids.append(int(first_id))
        second_ids.append(int(second_id))

    return [first_ids, second_ids]

class IDs:
    def __init__(self, ids):
        self.first_ids, self.second_ids = ids

    def find_distance(self):
        self.first_ids.sort()
        self.second_ids.sort()

        distance = 0
        while len(self.first_ids) > 0:
            distance += abs(self.first_ids.pop() - self.second_ids.pop())
        
        return distance
    
    def find_difference(self):
        similarity = 0
        while len(self.first_ids) > 0:
            current_id = self.first_ids.pop()
            similarity += self.second_ids.count(current_id) * current_id
        
        return similarity


def first(ids):
    ids = IDs(ids)
    return ids.find_distance()

def second(ids):
    ids = IDs(ids)
    return ids.find_difference()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day01"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (11):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input        (31):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")