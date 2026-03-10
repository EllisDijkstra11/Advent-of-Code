from pathlib import Path
from pprint import pprint 
import timeit

def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()     
    
    directions = []
    metres = []
    colours = []
    for line in lines:
        direction, metre, colour = line.split(" ")
        directions.append(direction)
        metres.append(int(metre))
        colours.append(colour)
        #all_info.append(line.split(" "))
    return [directions, metres, colours]#all_info

def first(all_info):
    directions, metres, colours = all_info
    
    numerical_directions = [0, -1], [1, 0], [0, 1], [-1, 0]
    letter_directions = "U", "R", "D", "L"

    all_points = find_trench(directions, metres, numerical_directions, letter_directions)
    #print_field(all_points)
    total_sum = find_lagoon_size(all_points)

    return total_sum


def second(all_info):
    pass


def find_trench(directions, metres, numerical_directions, letter_directions):
    current_point = [0, 0]
    all_points = []

    for index in range(len(directions)):
        current_direction = numerical_directions[letter_directions.index(directions[index])]
        for _ in range(metres[index]):
            current_point = [sum(i) for i in zip(current_point, current_direction)]
            all_points.append([current_point[1], current_point[0]])
    
    if all_points[-1][0] == 0 and all_points[-1][1] > 0:
        current_direction = [0, -1]
    elif all_points[-1][0] == 0:
        current_direction = [0, 1]
    elif all_points[-1][1] > 0:
        current_direction = [1, -1]
    else:
        current_direction = [1, 1]

    while current_point != [0, 0]:
        current_point = [sum(i) for i in zip(current_point, current_direction)]
        all_points.append(current_point)

    all_points.sort()
    return all_points


def find_lagoon_size(all_points):
    last_corner = []

    while pos_y < len(all_points):
        current_pipe = all_points[pos_y][pos_x]

        if current_pipe == "|":
            enclosed = not enclosed
        elif enclosed and current_pipe == ".":
            enclosed_points += 1
            all_points[pos_y][pos_x] = "O"
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
        if pos_x >= len(all_points[0]):
            pos_x = 0
            pos_y += 1
            enclosed = False
            last_corner = []

    return enclosed_points


def find_lagoon_sizes(all_points):
    total_sum = 0
    pos_x_min = 0
    pos_x_last = 0
    pos_x_max = 0
    pos_y = 0
    inside = True

    for point in all_points:
        if point[0] == pos_y:
            pos_x_max = point[1]
            if pos_x_max - pos_x_last == 1:
                pos_x_last = point[1]
            elif inside and [point[0], point[1] + 1] not in all_points:
                total_sum += pos_x_max - pos_x_min + 1
                print("total_sum:", total_sum)
                inside = False
            elif not inside and point[1] - pos_x_min != 1:
                pos_x_min = point[1]
                pos_x_last = pos_x_min
                print("pos x min:", pos_x_min)
                inside = True
            print("point:", point, ", total sum:", total_sum, ", pos x min:", pos_x_min, ", pos x last:", pos_x_last, ", pos x max:", pos_x_max)
        else:
            if pos_x_max - pos_x_last == 1:
                total_sum += pos_x_max - pos_x_min + 1

            pos_y = point[0]
            pos_x_min = point[1]
            pos_x_last = pos_x_min
            pos_x_max = point[1]
            inside = True
            print("point:", point, ", total sum:", total_sum, ", pos x min:", pos_x_min, ", pos x last:", pos_x_last, ", pos x max:", pos_x_max)


    total_sum += pos_x_max - pos_x_min + 1
    
    return total_sum


def print_field(all_points):
    field = []
    pos_x_min = 0
    pos_x_max = 0
    pos_y_min = 0
    pos_y_max = 0

    for point in all_points:
        if point[0] < pos_y_min:
            pos_y_min = point[0]
        elif point[0] > pos_y_max:
            pos_y_max = point[0]
        
        if point[1] < pos_x_min:
            pos_x_min = point[1]
        elif point[1] > pos_x_max:
            pos_x_max = point[1]

    for row in range(pos_y_max - pos_y_min + 1):
        field_row = ""
        for column in range(pos_x_max - pos_x_min + 1):
            if [row + pos_y_min, column + pos_x_min] in all_points:
                field_row += "#"
            else:
                field_row += "."
        field.append(field_row)
    
    pprint(field)


if __name__ == "__main__":
    path = "2023/day18"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (62):", first(preprocess(example_data)))
    print("Part 1 - Too high                 : 134065")

    start = timeit.default_timer()
    #print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    # print("Part 2 - Example input       ():", second(preprocess(example_data)))
    
    # start = timeit.default_timer()
    # print("Part 2 - Actual input             :", second(preprocess(data)))
    # print(f"Time taken: {timeit.default_timer()-start}s")
    