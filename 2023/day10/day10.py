from pathlib import Path
from pprint import pprint 

# characters that represent the pipes
pipes_characters = "|", "-", "L", "J", "7", "F", ".", "S"

# wind directions and coordinates the pipes connect to each other (north, east, south, west)
pipes_connections = (1, 0, 1, 0), (0, 1, 0, 1), (1, 1, 0, 0), (1, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 0), (1, 1, 1, 1), (1, 1, 1, 1)
pipes_coordinates = [[0, -1], [0, 1]], [[1, 0], [-1, 0]], [[0, -1], [1, 0]], [[0, -1], [-1, 0]], [[0, 1], [-1, 0]], [[0, 1], [1, 0]], [[1, 1], [1, 1]], [[1, 0], [-1, 0], [0 , 1], [0, -1]]

# wind directions (north, east, south, west)
wind_directions = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)

# direction of the coordinates based on the wind direction
wind_coordinates = [0, -1], [1, 0], [0, 1], [-1, 0]


def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()

    pipes = []
    for line in lines:
        pipes.append([*line])

    return pipes


def first(pipes):
    starting_point = find_starting_point(pipes)
    first_pipe, second_pipe = find_first_pipes(starting_point, pipes)
    
    steps = 1

    while first_pipe[0] != second_pipe[0]:
        first_pipe = find_next_pipe(first_pipe, pipes)
        second_pipe = find_next_pipe(second_pipe, pipes)
        steps += 1

    return steps


def second(pipes):
    starting_point = find_starting_point(pipes)
    pipe, second_pipe = find_first_pipes(starting_point, pipes)

    loop = pipes.copy()
    loop[starting_point[1]][starting_point[0]] = "F"

    loop_pipes = [starting_point]

    while pipe[0] != starting_point:
        loop_pipes.append(pipe[0])
        pipe = find_next_pipe(pipe, pipes)

    pos_x = 0
    pos_y = 0
    while pos_y < len(loop):
        if [pos_x, pos_y] not in loop_pipes:
            loop[pos_y][pos_x] = "."

        pos_x += 1
        if pos_x >= len(loop[0]):
            pos_x = 0
            pos_y += 1

    pos_x = 0
    pos_y = 0
    enclosed_points = 0
    enclosed = False

    last_corner = []
    pipe_sets = [["F", "7"], ["7", "F"], ["L", "J"], ["J", "L"]]
    consecutive_pipes = [["F", "J"], ["L", "7"]]

    while pos_y < len(loop):
        current_pipe = loop[pos_y][pos_x]

        if current_pipe == "|":
            enclosed = not enclosed
        elif enclosed and current_pipe == ".":
            enclosed_points += 1
            loop[pos_y][pos_x] = "O"
        elif current_pipe != "-":
            found = False
            for consecutive_pipe in consecutive_pipes:
                if current_pipe == consecutive_pipe[1]:
                    if len(last_corner) > 0 and last_corner[-1] == consecutive_pipe[0]:
                        last_corner.append(current_pipe)
                        found = True
            if not found:
                for pipe_set in pipe_sets:
                    if current_pipe == pipe_set[0]:
                        last_corner.append(current_pipe)
                        enclosed = not enclosed

        pos_x += 1
        if pos_x >= len(loop[0]):
            pos_x = 0
            pos_y += 1
            enclosed = False
            last_corner = []

    return enclosed_points


def find_starting_point(pipes):
    pos_x = 0
    pos_y = 0
    while pipes[pos_y][pos_x] != "S":
        pos_x += 1
        if pos_x >= len(pipes[0]):
            pos_x = 0
            pos_y += 1
    return [pos_x, pos_y]


def find_first_pipes(starting_point, pipes):
    first_pipe = 0
    second_pipe = 0

    for wind_coordinate in wind_coordinates:
        checked_point = [sum(i) for i in zip(starting_point, wind_coordinate)]

        if checked_point[0] >= 0 and checked_point[0] < len(pipes[0]) and checked_point[1] >= 0 and checked_point[1] < len(pipes):
            pipes_coordinate = pipes_coordinates[pipes_characters.index(pipes[checked_point[1]][checked_point[0]])].copy()
            opposite_wind_coordinate = [wind_coordinate[0] * -1, wind_coordinate[1] * -1]

            if opposite_wind_coordinate in pipes_coordinate and first_pipe == 0:
                pipes_coordinate.remove(opposite_wind_coordinate)
                first_pipe = [checked_point, pipes_coordinate[0]]
            elif opposite_wind_coordinate in pipes_coordinate:
                pipes_coordinate.remove(opposite_wind_coordinate)
                second_pipe = [checked_point, pipes_coordinate[0]]
    
    return [first_pipe, second_pipe]
            

def find_next_pipe(pipe, pipes):
    checked_point = [sum(i) for i in zip(pipe[0], pipe[1])]

    pipes_coordinate = pipes_coordinates[pipes_characters.index(pipes[checked_point[1]][checked_point[0]])].copy()
    opposite_wind_coordinate = [pipe[1][0] * -1, pipe[1][1] * -1]

    pipes_coordinate.remove(opposite_wind_coordinate)
    return [checked_point, pipes_coordinate[0]]


if __name__ == "__main__":
    path = "2023/day10"
    data_path_example_one = Path(path + '/example_one.txt')
    data_path_example_two = Path(path + '/example_two.txt')
    data_path_example_three = Path(path + '/example_three.txt')
    data_path_example_four = Path(path + '/example_four.txt')
    data_path_example_five = Path(path + '/example_five.txt')

    data_path_input = Path(path + '/input.txt')
    data_path_Jeroen = Path(path + '/inputJeroen.txt')

    example_data_one = data_path_example_one.read_text()
    example_data_two = data_path_example_two.read_text()
    example_data_three = data_path_example_three.read_text()
    example_data_four = data_path_example_four.read_text()
    example_data_five = data_path_example_five.read_text()
    
    data = data_path_input.read_text()
    Jeroens_data = data_path_Jeroen.read_text()

    print("Part 1 - Example one input        (4): ", first(preprocess(example_data_one)))
    print("Part 1 - Example two input        (8): ", first(preprocess(example_data_two)))
    print("Part 1 - Actual input          (6846): ", first(preprocess(data)))

    print("Part 2 - Example three input      (4): ", second(preprocess(example_data_three)))
    print("Part 2 - Example four input       (8): ", second(preprocess(example_data_four)))
    print("Part 2 - Example five input      (10): ", second(preprocess(example_data_five)))
    print("Part 2 - Actual input           (325): ", second(preprocess(data)))
    print("Part 2 - Jeroen's input         (285): ", second(preprocess(Jeroens_data)))