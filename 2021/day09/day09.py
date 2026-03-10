from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    return [[int(n) for n in line] for line in input_lines.split('\n')]

class Smoke:
    def __init__(self, smoke):
        self.smoke = smoke
        self.low_points = []
        self.basins = []
    
    def findLowPoints(self):
        x = 0
        y = 0

        for y in range(len(self.smoke)):
            for x in range(len(self.smoke[0])):
                neighbours = []

                if x != 0:
                    neighbours.append(self.smoke[y][x - 1])
                if x != len(self.smoke[0]) - 1:
                    neighbours.append(self.smoke[y][x + 1])

                if y != 0:
                    neighbours.append(self.smoke[y - 1][x])
                if y != len(self.smoke) - 1:
                    neighbours.append(self.smoke[y + 1][x])

                lower_neighbours = list(filter(lambda n: (n <= self.smoke[y][x]), neighbours))

                if len(lower_neighbours) == 0:
                    self.low_points.append([x, y])
        
    def findRiskLevels(self):
        sum = 0

        for point in self.low_points:
            x, y = point
            sum += self.smoke[y][x] + 1

        return sum

    def findBasins(self):
        for point in self.low_points:
            visited = []
            found = [point]
            directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]

            while found:
                current_point = found.pop(0)
                x, y = current_point

                for direction in directions:
                    step_x, step_y = direction
                    next_x = x + step_x
                    next_y = y + step_y
                    
                    if 0 <= next_x < len(self.smoke[0]) and 0 <= next_y < len(self.smoke):
                        next_point = [next_x, next_y]
                        next_point_depth = self.smoke[next_y][next_x]
                        if not next_point_depth == 9 and next_point not in found and next_point not in visited:
                            found.append(next_point)
                    
                visited.append(current_point)
        
            self.basins.append(len(visited))
            
    def findBiggestBasins(self):
        self.basins.sort(reverse = True)
        return self.basins[0] * self.basins[1] * self.basins[2]

def first(smoke):
    smoke = Smoke(smoke)
    smoke.findLowPoints()
    return smoke.findRiskLevels()

def second(smoke):
    smoke = Smoke(smoke)
    smoke.findLowPoints()
    smoke.findBasins()
    return smoke.findBiggestBasins()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day09/"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (15):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input      (1134):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")