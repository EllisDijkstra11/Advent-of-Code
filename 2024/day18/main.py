import timeit 
import numpy as np
from pathlib import Path
from heapq import heappush, heappop

def preprocess(input_lines: list[int]):
    return [(int(x), int(y)) for line in input_lines.split('\n') for x, y in [line.split(',')]]

class Maze:
    def __init__(self, input):
        self.obstacles = self.capped_obstacles = input
        self.start = (0, 0)
        self.end = (70, 70)
        self.path = []
    
    def cap_obstacles(self, cap):
        self.capped_obstacles = self.obstacles[: cap]

    def print_field(self, obstacle):
        for y in range(self.end[1] + 1):
            row = ''
            for x in range(self.end[0] + 1):
                if(x, y) == obstacle:
                    row += 'X'
                elif (x, y) in self.path:
                    row += 'O'
                elif (x, y) in self.capped_obstacles:
                    row += '#'
                else:
                    row += '.'
            print(row)
        print('\n')

    def get_path(self):
        if self.path:
            return len(self.path)
        return None
    
    def find_blocked_coordinate(self):
        for index, obstacle in enumerate(self.obstacles):
            if obstacle in self.path:
                self.cap_obstacles(index + 1)
                self.path = []
                if not self.find_shortest_path():
                    return obstacle
        return False

    def find_shortest_path(self):
        found = []
        visited = set()
        parents = {}
        cost = {}

        for x in range(self.end[0] + 1):
            for y in range(self.end[1] + 1):
                cost[(x, y)] = np.inf
        
        cost[(self.start)] = 0
        heappush(found, (self.distance_to_target(self.start), self.start))

        while found:
            _, current = heappop(found)
            visited.add(current)

            if current == self.end:
                while current in parents:
                    x, y = current

                    self.path.append((x, y))
                    current = parents[current]

                return True

            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                if neighbour in visited:
                    continue
                
                x, y = neighbour
                new_cost = cost[current] + 1

                if new_cost < cost[neighbour]:
                    cost[neighbour] = new_cost
                    parents[neighbour] = current
                    current_distance = self.distance_to_target(neighbour) + new_cost
                    heappush(found, (current_distance, neighbour))

        return False

    def get_neighbours(self, current):
        x, y = current
        directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        
        neighbours = []
        for step_x, step_y in directions:
            next_x = x + step_x
            next_y = y + step_y
            next_position = (next_x, next_y)

            if 0 <= next_x <= self.end[0] and 0 <= next_y <= self.end[1] and (next_x, next_y) not in self.capped_obstacles:
                neighbours.append(next_position)
        
        return neighbours

    def distance_to_target(self, current):
        return abs(current[0] - self.end[0]) + abs(current[1] - self.end[1])

def first(input):
    maze = Maze(input)
    maze.cap_obstacles(1024)
    maze.find_shortest_path()
    return maze.get_path()

def second(input):
    maze = Maze(input)
    maze.cap_obstacles(1024)
    maze.find_shortest_path()
    return maze.find_blocked_coordinate()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day18"

    example = Path(path + '/example.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s")