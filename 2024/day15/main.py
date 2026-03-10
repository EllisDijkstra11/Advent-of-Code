import copy
import pprint
import timeit 
import itertools
from pathlib import Path

def preprocess(input_lines: list[int]):
    floor, movements = input_lines.split('\n\n')
    floor = [[n for n in line] for line in floor.split('\n')]
    movements = list(itertools.chain(*movements.split('\n')))
    return [floor, movements]

class Robots:
    def __init__(self, input):
        self.floor, self.movements = input

        self.position = [[row.index('@'), r]
                    for r, row in enumerate(self.floor)
                    if '@' in row][0]
        self.set_field(self.position, '.')

        self.directions = {'^': (0, -1), 
                           '>': (1, 0), 
                           'v': (0, 1),
                           '<': (-1, 0)}
    
    def get_field(self, position):
        return self.floor[position[1]][position[0]]

    def set_field(self, position, character):
        self.floor[position[1]][position[0]] = character

    def take_step(self, position, direction):
        return [position[0] + direction[0], position[1] + direction[1]]

    def find_score(self):
        total = 0

        for r, row in enumerate(self.floor):
            for c, column in enumerate(row):
                if column in 'O[':
                    total += 100 * r + c

        return total

    def move_robot(self):
        for move in self.movements:
            direction = self.directions[move]
            floor = copy.deepcopy(self.floor)
            if self.is_room(self.position, direction):
                self.position = self.take_step(self.position, direction)
            else:
                self.floor = floor
    
    def is_room(self, position, direction):
        next_position = self.take_step(position, direction)
        field = self.get_field(next_position)
        if field == '#':
            return False
        elif field == '.':
            return True

        # Part 1
        if field == 'O' and self.is_room(next_position, direction):
            self.set_field(next_position, '.')
            self.set_field(self.take_step(next_position, direction), 'O')
            return True
        
        # Part 2
        elif direction in [self.directions['^'], self.directions['v']]:
            valid = (field == '[' and self.is_room(next_position, direction) and self.is_room(self.take_step(next_position, self.directions['>']), direction))
            if valid:
                self.set_field(self.take_step(next_position, direction), self.get_field(next_position))
                self.set_field(next_position, '.')
                next_position = self.take_step(next_position, self.directions['>'])
                self.set_field(self.take_step(next_position, direction), self.get_field(next_position))
                self.set_field(next_position, '.')
                return True
            
            valid = (field == ']' and self.is_room(next_position, direction) and self.is_room(self.take_step(next_position, self.directions['<']), direction))
            if valid:
                self.set_field(self.take_step(next_position, direction), self.get_field(next_position))
                self.set_field(next_position, '.')
                next_position = self.take_step(next_position, self.directions['<'])
                self.set_field(self.take_step(next_position, direction), self.get_field(next_position))
                self.set_field(next_position, '.')
                return True
            
        elif field in '[]' and self.is_room(next_position, direction):
                self.set_field(self.take_step(next_position, direction), self.get_field(next_position))
                self.set_field(next_position, '.')
                return True

        return False

    
    def convert_warehouse(self):
        for r, row in enumerate(self.floor):
            for c, column in enumerate(row):
                if column == 'O':
                    self.set_field([c, r], ['[', ']'])
                elif column == '#':
                    self.set_field([c, r], ['#', '#'])
                elif column == '.':
                    self.set_field([c, r], ['.', '.'])

def convert_warehouse(input):
    new_field = []
    for row in input:
        new_row = []
        for column in row:
            if column == 'O':
                new_row.append('[')
                new_row.append(']')
            elif column == '#':
                new_row.append('#')
                new_row.append('#')
            elif column == '.':
                new_row.append('.')
                new_row.append('.')
            elif column == '@':
                new_row.append('@')
                new_row.append('.')
        new_field.append(new_row)
    return new_field

def first(input):
    robots = Robots(input)
    robots.move_robot()
    return robots.find_score()

def second(input):
    field, movements = input
    field = convert_warehouse(field)
    robots = Robots([field, movements])
    robots.move_robot()
    return robots.find_score()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day15"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input     (10092):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input      (9021):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")