from pathlib import Path
import timeit 
import pprint

def preprocess(input_lines: list[int]):
    return [[int(n) for n in line] for line in input_lines.split('\n')]

class Octopuses:

    def __init__(self, octopuses):
        self.flashes = 0
        self.octopuses = octopuses
        self.flash_direction = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not (x == 0 and y == 0):
                    self.flash_direction.append([x, y])
    
    def update_energy(self):
        for y, row in enumerate(self.octopuses):
            for x, octopus in enumerate(row):
                self.octopuses[y][x] += 1
    
    def update_flashes(self):
        updated = True

        while updated:
            updated = False
            for y, row in enumerate(self.octopuses):
                for x, octopus in enumerate(row):
                    if octopus > 9:
                        updated = True
                        self.flashes += 1
                        self.flash(x, y)

    def flash(self, x, y):
        for direction in self.flash_direction:
            diff_x, diff_y = direction
            update = True

            new_x = x + diff_x
            new_y = y + diff_y

            if not 0 <= new_x < len(self.octopuses[0]):
                update = False
            elif not 0 <= new_y < len(self.octopuses):
                update = False
            elif self.octopuses[new_y][new_x] == 0:
                update = False
            
            if update:
                self.octopuses[new_y][new_x] += 1
        
        self.octopuses[y][x] = 0
    
    def do_steps(self, n):
        for _ in range(n):
            self.update_energy()
            self.update_flashes()
        
        return self.flashes
    
    def find_synchronised_step(self):
        n = 0

        while not all(all(octopus == 0 for octopus in row) for row in self.octopuses):
            n += 1
            self.update_energy()
            self.update_flashes()

        return n


def first(octopuses):
    octopuses = Octopuses(octopuses)
    return octopuses.do_steps(100)

def second(octopuses):
    octopuses = Octopuses(octopuses)
    return octopuses.find_synchronised_step()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day11"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input      (1656):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input       (195):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")