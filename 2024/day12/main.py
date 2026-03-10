import timeit 
from pathlib import Path
from collections import defaultdict

def preprocess(input_lines: list[int]):
    return [[field for field in line] for line in input_lines.split('\n')]

class Plants:
    def __init__(self, input):
        self.field = input
        self.plants = defaultdict(set)
        self.plots = []

        for r, row in enumerate(self.field):
            for c, column in enumerate(row):
                self.plants[column].add((c, r))
        
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def find_neighbours(self, plant):
        return set([(plant[0] + d[0], plant[1] + d[1]) for d in self.directions])

    def find_plots(self):
        for type, plants in self.plants.items():
            while plants:
                plant = plants.pop()
                plot = {plant}

                found = self.find_neighbours(plant).intersection(plants)
                plants = plants.difference(found)

                perimeter = 4

                while found:
                    plant = found.pop()
                    plot.add(plant)

                    neighbours = self.find_neighbours(plant)
                    perimeter += 4 - (2 * len(neighbours.intersection(plot)))

                    neighbours = neighbours.intersection(plants)
                    found = found.union(neighbours)
                    plants = plants.difference(neighbours)

                self.plots.append((plot, perimeter))
    
    def find_corners(self):
        fence = 0
        for plot in self.plots:
            corners = 0
            plot = plot[0]
            for plant in plot:
                for index in range(len(self.directions)):
                    directions = [self.directions[index], self.directions[(index + 1) % 4]]
                    plants = [(plant[0] + d[0], plant[1] + d[1]) for d in directions]
                    
                    if plants[0] not in plot and plants[1] not in plot:
                        corners += 1

                    diagonal = (directions[0][0] + directions[1][0], directions[0][1] + directions[1][1])
                    diagonal_plant = plant[0] + diagonal[0], plant[1] + diagonal[1]
                    
                    if plants[0] in plot and plants[1] in plot and diagonal_plant not in plot:
                        corners += 1

            fence += len(plot) * corners
        
        return fence
    
    def find_fence(self):
        return sum([len(plot[0]) * plot[1] for plot in self.plots])


def first(input):
    plants = Plants(input)
    plants.find_plots()
    return plants.find_fence()

def second(input):
    plants = Plants(input)
    plants.find_plots()
    return plants.find_corners()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day12"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input      (1930):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input      (1206):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")