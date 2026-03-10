from pathlib import Path
import timeit 
import re

def preprocess(input_lines: list[int]):
    coordinates = re.findall(r"-?\d+", input_lines)
    x_min, x_max, y_min, y_max = coordinates
    return [[int(x_min), int(x_max)], [int(y_min), int(y_max)]]

class Shot:
    def __init__(self, target):
        self.target = target
        print(self.target)
        self.start = [0, 0]
        self.max_height = 0
    
    def find_max_height(self):
        maximum_velocity = -self.target[1][0]
        return sum([height for height in range(maximum_velocity)])

    def find_all_velocities(self):
        possible_x_velocities = {}
        possible_y_velocities = {}
        stationary_x_velocities = []

        for x_velocity in range(1, self.target[0][1] + 1):
            steps = 0
            x_location = 0
            velocity = x_velocity

            while x_location <= self.target[0][1] and steps < 20:
                steps += 1
                x_location += velocity
                velocity = max(0, velocity - 1)

                if self.x_in_target(x_location):
                    # print("x_velocity:", x_velocity)
                    print("added -> steps:", steps, "x_velocity:", x_velocity)
                    possible_x_velocities[steps] = possible_x_velocities.get(steps, 0) + 1

        for y_velocity in range(self.target[1][0], -self.target[1][0] + 1):
            steps = 0
            y_location = 0
            velocity = y_velocity

            while y_location >= self.target[1][0]:
                steps += 1
                y_location += velocity
                velocity -= 1

                # print(y_location)
                if self.y_in_target(y_location):
                    # print("y_velocity:", y_velocity)
                    possible_y_velocities[steps] = possible_y_velocities.get(steps, 0) + 1
                    print("added -> steps:", steps, "y_velocity:", y_velocity)
        
        print("\n")
        print(possible_y_velocities)
        
        possibilities = 0
        for key, y_possibilities in possible_y_velocities.items():
            x_possibilities = possible_x_velocities.get(key, 0)
            # print(y_possibilities, x_possibilities)
            if x_possibilities != 0 and y_possibilities != 0:
                possibilities += x_possibilities * y_possibilities

        return possibilities

    def shoot_shots(self):
        min_x_velocity = round(self.target[0][0]*0.4)
        max_x_velocity = round(self.target[0][1]*0.5)
        start_velocity = [min_x_velocity, -200]
        possible_shot = True
        possible_shots = 0
        self.max_height = self.find_max_height()

        while possible_shot:
            location = self.start
            velocity = start_velocity

            while not self.past_target(location):
                location[0] += velocity[0]
                location[1] += velocity[1]

                if not velocity[0] == 0:
                    velocity[0] -= 1
                velocity[1] -= 1
                print(location, velocity)

                if self.in_target(location):
                    print(1)
                    location[0] += 1000
                    possible_shots += 1
                elif velocity[0] == 0 and location[0] < self.target[0][0]:
                    print(2)
                    start_velocity[0] += 1
                    start_velocity[1] = -200
                    location[0] += 1000

            if start_velocity[1] < self.max_height:
                # print(3)
                start_velocity[1] += 1
            elif start_velocity[0] > max_x_velocity:
                print(4)
                possible_shot = False
            else:
                print(5)
                start_velocity[0] += 1
                start_velocity[1] = -200
        
        return possible_shots

    
    def in_target(self, location):
        if self.x_in_target(location[0]) and self.y_in_target(location[1]):
            return True
        return False

    def x_in_target(self, location):
        if self.target[0][0] <= location <= self.target[0][1]:
            return True
        return False
    
    def y_in_target(self, location):
        if self.target[1][0] <= location <= self.target[1][1]:
            return True
        return False
        
    def past_target(self, location):
        if self.past_x_target(location[0]) and self.past_y_target(location[1]):
            return True
        return False
    
    def past_x_target(self, location):
        if location > self.target[0][1]:
            return True
        return False
    
    def past_y_target(self, location):
        if location < self.target[1][1]:
            return True
        return False
    
    def get_max_height(self):
        return self.max_height

def first(target):
    shot = Shot(target)
    return shot.find_max_height()

def second(target):
    shot = Shot(target)
    return shot.find_all_velocities()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day17"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (45):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input          ():", second(preprocess(example_data)))
    
    print("Part 2 - Too low            (3990):", second(preprocess(data)))
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")